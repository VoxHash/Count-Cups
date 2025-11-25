"""Database operations and migrations."""

import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.core.logging import get_logger
from app.core.models import (
    CupProfile,
    DailyGoal,
    DailyStats,
    SipEvent,
    UserSettings,
    WeeklyStats,
)

logger = get_logger(__name__)


class Database:
    """Database operations for Count-Cups."""

    def __init__(self, db_path: Path | None = None):
        """Initialize database connection.

        Args:
            db_path: Path to database file (defaults to settings)
        """
        self.db_path = db_path or settings.get_database_path()
        self.connection: sqlite3.Connection | None = None
        self._ensure_database()

    @property
    def conn(self) -> sqlite3.Connection:
        """Get database connection, ensuring it exists."""
        if self.connection is None:
            self._ensure_database()
        assert self.connection is not None, "Database connection must be initialized"
        return self.connection

    def _ensure_database(self) -> None:
        """Ensure database file exists and run migrations."""
        # Ensure parent directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Connect to database
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row

        # Run migrations
        self._run_migrations()

    def _run_migrations(self) -> None:
        """Run database migrations."""
        cursor = self.conn.cursor()

        # Create migrations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                version INTEGER PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Get current version
        cursor.execute("SELECT MAX(version) as version FROM migrations")
        result = cursor.fetchone()
        current_version = result["version"] if result["version"] else 0

        # Run migrations
        migrations = [
            self._migration_001_initial_schema,
            self._migration_002_add_detection_data,
            self._migration_003_add_user_settings,
        ]

        for migration in migrations:
            # Extract version number from migration function name
            # e.g., "_migration_001_initial_schema" -> "001"
            parts = migration.__name__.split("_")
            if len(parts) >= 3 and parts[2].isdigit():
                version_num = int(parts[2])
            else:
                logger.warning(f"Invalid migration name format: {migration.__name__}")
                continue

            if version_num > current_version:
                logger.info(f"Running migration {version_num}")
                migration(cursor)
                cursor.execute(
                    "INSERT INTO migrations (version) VALUES (?)", (version_num,)
                )
                self.conn.commit()

    def _migration_001_initial_schema(self, cursor: sqlite3.Cursor) -> None:
        """Initial database schema."""
        # Cup profiles table
        cursor.execute("""
            CREATE TABLE cup_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                size_ml INTEGER NOT NULL CHECK (size_ml > 0),
                sips_per_cup INTEGER NOT NULL CHECK (sips_per_cup > 0),
                color TEXT CHECK (color LIKE '#%'),
                is_default BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Daily goals table
        cursor.execute("""
            CREATE TABLE daily_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL UNIQUE,
                target_ml INTEGER NOT NULL CHECK (target_ml > 0),
                achieved_ml REAL DEFAULT 0.0 CHECK (achieved_ml >= 0),
                is_achieved BOOLEAN DEFAULT FALSE,
                streak_days INTEGER DEFAULT 0 CHECK (streak_days >= 0),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Sip events table
        cursor.execute("""
            CREATE TABLE sip_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP NOT NULL,
                profile_id INTEGER NOT NULL,
                ml_estimate REAL NOT NULL CHECK (ml_estimate >= 0),
                source TEXT NOT NULL CHECK (source IN ('auto', 'manual')),
                confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
                detection_data TEXT,  -- JSON string
                FOREIGN KEY (profile_id) REFERENCES cup_profiles (id)
            )
        """)

        # Create indexes
        cursor.execute(
            "CREATE INDEX idx_sip_events_timestamp ON sip_events (timestamp)"
        )
        cursor.execute(
            "CREATE INDEX idx_sip_events_profile_id ON sip_events (profile_id)"
        )
        cursor.execute("CREATE INDEX idx_daily_goals_date ON daily_goals (date)")

    def _migration_002_add_detection_data(self, cursor: sqlite3.Cursor) -> None:
        """Add detection data column to sip_events."""
        try:
            cursor.execute("ALTER TABLE sip_events ADD COLUMN detection_data TEXT")
        except sqlite3.OperationalError:
            # Column already exists
            pass

    def _migration_003_add_user_settings(self, cursor: sqlite3.Cursor) -> None:
        """Add user settings table."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                id INTEGER PRIMARY KEY,
                theme TEXT DEFAULT 'auto' CHECK (theme IN ('auto', 'light', 'dark', 'dracula')),
                detection_engine TEXT DEFAULT 'heuristics' CHECK (detection_engine IN ('heuristics', 'mediapipe')),
                enable_notifications BOOLEAN DEFAULT TRUE,
                goal_reminder_hour INTEGER DEFAULT 20 CHECK (goal_reminder_hour >= 0 AND goal_reminder_hour <= 23),
                goal_reminder_minute INTEGER DEFAULT 0 CHECK (goal_reminder_minute >= 0 AND goal_reminder_minute <= 59),
                default_cup_profile_id INTEGER,
                window_width INTEGER DEFAULT 1200 CHECK (window_width >= 800),
                window_height INTEGER DEFAULT 800 CHECK (window_height >= 600),
                window_maximized BOOLEAN DEFAULT FALSE,
                camera_index INTEGER DEFAULT 0 CHECK (camera_index >= 0),
                camera_width INTEGER DEFAULT 640 CHECK (camera_width >= 320),
                camera_height INTEGER DEFAULT 480 CHECK (camera_height >= 240),
                camera_fps INTEGER DEFAULT 30 CHECK (camera_fps >= 15),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (default_cup_profile_id) REFERENCES cup_profiles (id)
            )
        """)

    def close(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def ensure_connection(self) -> bool:
        """Ensure database connection is valid.

        Returns:
            True if connection is valid, False otherwise
        """
        if not self.connection:
            try:
                self._ensure_database()
                return True
            except Exception as e:
                logger.error(f"Failed to reconnect to database: {e}")
                return False

        try:
            # Test connection
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1")
            return True
        except Exception as e:
            logger.warning(f"Database connection lost, attempting to reconnect: {e}")
            try:
                self.connection.close()
                self.connection = None
                self._ensure_database()
                return True
            except Exception as e2:
                logger.error(f"Failed to reconnect to database: {e2}")
                return False

    def __enter__(self) -> "Database":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()

    # Cup Profile Operations
    def create_cup_profile(self, profile: CupProfile) -> int:
        """Create a new cup profile."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO cup_profiles (name, size_ml, sips_per_cup, color, is_default, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                profile.name,
                profile.size_ml,
                profile.sips_per_cup,
                profile.color,
                profile.is_default,
                profile.created_at,
                profile.updated_at,
            ),
        )
        self.conn.commit()
        rowid = cursor.lastrowid
        assert rowid is not None, "Failed to get lastrowid"
        return rowid

    def get_cup_profile(self, profile_id: int) -> CupProfile | None:
        """Get cup profile by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cup_profiles WHERE id = ?", (profile_id,))
        row = cursor.fetchone()
        if row:
            return CupProfile(**dict(row))
        return None

    def get_all_cup_profiles(self) -> list[CupProfile]:
        """Get all cup profiles."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cup_profiles ORDER BY created_at DESC")
        return [CupProfile(**dict(row)) for row in cursor.fetchall()]

    def update_cup_profile(self, profile: CupProfile) -> bool:
        """Update cup profile."""
        if not profile.id:
            return False

        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE cup_profiles
            SET name = ?, size_ml = ?, sips_per_cup = ?, color = ?, is_default = ?, updated_at = ?
            WHERE id = ?
        """,
            (
                profile.name,
                profile.size_ml,
                profile.sips_per_cup,
                profile.color,
                profile.is_default,
                profile.updated_at,
                profile.id,
            ),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_cup_profile(self, profile_id: int) -> bool:
        """Delete cup profile."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM cup_profiles WHERE id = ?", (profile_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    # Sip Event Operations
    def create_sip_event(self, event: SipEvent) -> int:
        """Create a new sip event."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO sip_events (timestamp, profile_id, ml_estimate, source, confidence, detection_data)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                event.timestamp,
                event.profile_id,
                event.ml_estimate,
                str(event.source),
                event.confidence,
                event.detection_data,
            ),
        )
        self.conn.commit()
        rowid = cursor.lastrowid
        assert rowid is not None, "Failed to get lastrowid"
        return rowid

    def get_sip_events(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        profile_id: int | None = None,
    ) -> list[SipEvent]:
        """Get sip events with optional filters."""
        cursor = self.conn.cursor()

        query = "SELECT * FROM sip_events WHERE 1=1"
        params: list[datetime | int] = []

        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)

        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)

        if profile_id:
            query += " AND profile_id = ?"
            params.append(profile_id)

        query += " ORDER BY timestamp DESC"

        cursor.execute(query, params)
        return [SipEvent(**dict(row)) for row in cursor.fetchall()]

    # Daily Goal Operations
    def get_or_create_daily_goal(self, target_date: date, target_ml: int) -> DailyGoal:
        """Get or create daily goal for a date."""
        cursor = self.conn.cursor()

        # First try to get existing goal
        # Convert date to datetime for comparison (stored dates are datetime)
        target_datetime = datetime.combine(target_date, datetime.min.time())
        cursor.execute("SELECT * FROM daily_goals WHERE date = ?", (target_datetime,))
        row = cursor.fetchone()

        if row:
            return DailyGoal(**dict(row))

        # Create new goal using INSERT OR IGNORE to handle race conditions
        goal = DailyGoal(
            date=datetime.combine(target_date, datetime.min.time()),
            target_ml=target_ml,
            achieved_ml=0.0,
            is_achieved=False,
            streak_days=0,
        )

        cursor.execute(
            """
            INSERT OR IGNORE INTO daily_goals (date, target_ml, achieved_ml, is_achieved, streak_days, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                goal.date,
                goal.target_ml,
                goal.achieved_ml,
                goal.is_achieved,
                goal.streak_days,
                goal.created_at,
                goal.updated_at,
            ),
        )

        # Now get the goal (either newly created or existing)
        # Use the same target_datetime for consistency
        cursor.execute("SELECT * FROM daily_goals WHERE date = ?", (target_datetime,))
        row = cursor.fetchone()

        if row:
            self.conn.commit()
            return DailyGoal(**dict(row))
        else:
            # This shouldn't happen, but handle it gracefully
            self.conn.commit()
            goal.id = cursor.lastrowid
            return goal

    def update_daily_goal(self, goal: DailyGoal) -> bool:
        """Update daily goal."""
        if not goal.id:
            return False

        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE daily_goals
            SET target_ml = ?, achieved_ml = ?, is_achieved = ?, streak_days = ?, updated_at = ?
            WHERE id = ?
        """,
            (
                goal.target_ml,
                goal.achieved_ml,
                goal.is_achieved,
                goal.streak_days,
                goal.updated_at,
                goal.id,
            ),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    # Statistics Operations
    def get_daily_stats(self, target_date: date) -> DailyStats:
        """Get daily statistics for a date."""
        cursor = self.conn.cursor()

        # Get events for the day
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())

        cursor.execute(
            """
            SELECT * FROM sip_events
            WHERE timestamp >= ? AND timestamp <= ?
            ORDER BY timestamp
        """,
            (start_datetime, end_datetime),
        )

        events = [SipEvent(**dict(row)) for row in cursor.fetchall()]

        # Calculate totals
        total_ml = sum(event.ml_estimate for event in events)
        total_sips = len(events)
        total_cups = total_ml / 250.0  # Assuming 250ml per cup

        # Get daily goal
        goal = self.get_or_create_daily_goal(
            target_date, settings.default_cup_size_ml * 4
        )  # 4 cups default
        goal_achieved = total_ml >= goal.target_ml
        progress_percentage = (
            (total_ml / goal.target_ml * 100) if goal.target_ml > 0 else 0
        )

        return DailyStats(
            date=start_datetime,
            total_ml=total_ml,
            total_sips=total_sips,
            total_cups=total_cups,
            goal_ml=goal.target_ml,
            goal_achieved=goal_achieved,
            progress_percentage=progress_percentage,
            streak_days=goal.streak_days,
            events=events,
        )

    def get_weekly_stats(self, week_start: date) -> WeeklyStats:
        """Get weekly statistics starting from week_start."""
        # Calculate week end
        from datetime import timedelta

        week_end = week_start + timedelta(days=6)

        # Get daily stats for the week
        daily_stats = []
        total_ml = 0.0
        total_sips = 0
        goal_achieved_days = 0

        for i in range(7):
            current_date = week_start + timedelta(days=i)
            daily_stat = self.get_daily_stats(current_date)
            daily_stats.append(daily_stat)

            total_ml += daily_stat.total_ml
            total_sips += daily_stat.total_sips

            if daily_stat.goal_achieved:
                goal_achieved_days += 1

        total_cups = total_ml / 250.0
        average_daily_ml = total_ml / 7.0

        # Calculate streak (simplified)
        streak_days = 0
        for daily_stat in reversed(daily_stats):
            if daily_stat.goal_achieved:
                streak_days += 1
            else:
                break

        return WeeklyStats(
            week_start=datetime.combine(week_start, datetime.min.time()),
            week_end=datetime.combine(week_end, datetime.max.time()),
            total_ml=total_ml,
            total_sips=total_sips,
            total_cups=total_cups,
            average_daily_ml=average_daily_ml,
            goal_achieved_days=goal_achieved_days,
            streak_days=streak_days,
            daily_stats=daily_stats,
        )

    # User Settings Operations
    def get_user_settings(self) -> UserSettings:
        """Get user settings (creates default if not exists)."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user_settings WHERE id = 1")
        row = cursor.fetchone()

        if row:
            return UserSettings(**dict(row))

        # Create default settings
        settings_obj = UserSettings()
        cursor.execute(
            """
            INSERT INTO user_settings (
                id, theme, detection_engine, enable_notifications, goal_reminder_hour,
                goal_reminder_minute, default_cup_profile_id, window_width, window_height,
                window_maximized, camera_index, camera_width, camera_height, camera_fps,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                1,
                settings_obj.theme.value,
                settings_obj.detection_engine.value,
                settings_obj.enable_notifications,
                settings_obj.goal_reminder_hour,
                settings_obj.goal_reminder_minute,
                settings_obj.default_cup_profile_id,
                settings_obj.window_width,
                settings_obj.window_height,
                settings_obj.window_maximized,
                settings_obj.camera_index,
                settings_obj.camera_width,
                settings_obj.camera_height,
                settings_obj.camera_fps,
                settings_obj.created_at,
                settings_obj.updated_at,
            ),
        )
        self.conn.commit()

        settings_obj.id = 1
        return settings_obj

    def update_user_settings(self, settings_obj: UserSettings) -> bool:
        """Update user settings."""
        if not settings_obj.id:
            return False

        cursor = self.conn.cursor()
        # Handle theme and detection_engine as either enums or strings
        theme_value = (
            settings_obj.theme.value
            if hasattr(settings_obj.theme, "value")
            else str(settings_obj.theme)
        )
        engine_value = (
            settings_obj.detection_engine.value
            if hasattr(settings_obj.detection_engine, "value")
            else str(settings_obj.detection_engine)
        )

        cursor.execute(
            """
            UPDATE user_settings
            SET theme = ?, detection_engine = ?, enable_notifications = ?, goal_reminder_hour = ?,
                goal_reminder_minute = ?, default_cup_profile_id = ?, window_width = ?,
                window_height = ?, window_maximized = ?, camera_index = ?, camera_width = ?,
                camera_height = ?, camera_fps = ?, updated_at = ?
            WHERE id = ?
        """,
            (
                theme_value,
                engine_value,
                settings_obj.enable_notifications,
                settings_obj.goal_reminder_hour,
                settings_obj.goal_reminder_minute,
                settings_obj.default_cup_profile_id,
                settings_obj.window_width,
                settings_obj.window_height,
                settings_obj.window_maximized,
                settings_obj.camera_index,
                settings_obj.camera_width,
                settings_obj.camera_height,
                settings_obj.camera_fps,
                settings_obj.updated_at,
                settings_obj.id,
            ),
        )
        self.conn.commit()
        return cursor.rowcount > 0
