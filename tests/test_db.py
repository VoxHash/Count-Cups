"""Tests for database operations."""

import tempfile
from datetime import date, datetime
from pathlib import Path

import pytest

from app.core.db import Database
from app.core.models import (
    CupProfile,
    DetectionEngine,
    EventSource,
    SipEvent,
    ThemeMode,
)


class TestDatabase:
    """Test database functionality."""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"
            db = Database(db_path)
            yield db
            db.close()

    def test_init(self, temp_db):
        """Test database initialization."""
        assert temp_db.db_path.exists()
        assert temp_db.connection is not None

    def test_create_cup_profile(self, temp_db):
        """Test creating cup profile."""
        profile = CupProfile(
            name="Test Cup",
            size_ml=300,
            sips_per_cup=8,
            color="#ff0000",
            is_default=True,
        )

        profile_id = temp_db.create_cup_profile(profile)
        assert profile_id is not None
        assert profile_id > 0

    def test_get_cup_profile(self, temp_db):
        """Test getting cup profile."""
        # Create profile
        profile = CupProfile(
            name="Test Cup",
            size_ml=300,
            sips_per_cup=8,
            color="#ff0000",
            is_default=True,
        )

        profile_id = temp_db.create_cup_profile(profile)

        # Get profile
        retrieved_profile = temp_db.get_cup_profile(profile_id)
        assert retrieved_profile is not None
        assert retrieved_profile.name == "Test Cup"
        assert retrieved_profile.size_ml == 300
        assert retrieved_profile.sips_per_cup == 8
        assert retrieved_profile.color == "#ff0000"
        assert retrieved_profile.is_default is True

    def test_get_all_cup_profiles(self, temp_db):
        """Test getting all cup profiles."""
        # Create multiple profiles
        profile1 = CupProfile(name="Cup 1", size_ml=250, sips_per_cup=10)
        profile2 = CupProfile(name="Cup 2", size_ml=500, sips_per_cup=5)

        temp_db.create_cup_profile(profile1)
        temp_db.create_cup_profile(profile2)

        # Get all profiles
        profiles = temp_db.get_all_cup_profiles()
        assert len(profiles) == 2
        assert any(p.name == "Cup 1" for p in profiles)
        assert any(p.name == "Cup 2" for p in profiles)

    def test_update_cup_profile(self, temp_db):
        """Test updating cup profile."""
        # Create profile
        profile = CupProfile(
            name="Test Cup",
            size_ml=300,
            sips_per_cup=8,
            color="#ff0000",
            is_default=True,
        )

        profile_id = temp_db.create_cup_profile(profile)
        profile.id = profile_id

        # Update profile
        profile.name = "Updated Cup"
        profile.size_ml = 400
        profile.sips_per_cup = 6

        success = temp_db.update_cup_profile(profile)
        assert success is True

        # Verify update
        updated_profile = temp_db.get_cup_profile(profile_id)
        assert updated_profile.name == "Updated Cup"
        assert updated_profile.size_ml == 400
        assert updated_profile.sips_per_cup == 6

    def test_delete_cup_profile(self, temp_db):
        """Test deleting cup profile."""
        # Create profile
        profile = CupProfile(name="Test Cup", size_ml=300, sips_per_cup=8)

        profile_id = temp_db.create_cup_profile(profile)

        # Delete profile
        success = temp_db.delete_cup_profile(profile_id)
        assert success is True

        # Verify deletion
        deleted_profile = temp_db.get_cup_profile(profile_id)
        assert deleted_profile is None

    def test_create_sip_event(self, temp_db):
        """Test creating sip event."""
        # Create cup profile first
        profile = CupProfile(name="Test Cup", size_ml=250, sips_per_cup=10)
        profile_id = temp_db.create_cup_profile(profile)

        # Create sip event
        sip_event = SipEvent(
            timestamp=datetime.now(),
            profile_id=profile_id,
            ml_estimate=25.0,
            source=EventSource.AUTO,
            confidence=0.8,
        )

        event_id = temp_db.create_sip_event(sip_event)
        assert event_id is not None
        assert event_id > 0

    def test_get_sip_events(self, temp_db):
        """Test getting sip events."""
        # Create cup profile
        profile = CupProfile(name="Test Cup", size_ml=250, sips_per_cup=10)
        profile_id = temp_db.create_cup_profile(profile)

        # Create sip events
        event1 = SipEvent(
            timestamp=datetime.now(),
            profile_id=profile_id,
            ml_estimate=25.0,
            source=EventSource.AUTO,
        )
        event2 = SipEvent(
            timestamp=datetime.now(),
            profile_id=profile_id,
            ml_estimate=30.0,
            source=EventSource.MANUAL,
        )

        temp_db.create_sip_event(event1)
        temp_db.create_sip_event(event2)

        # Get all events
        events = temp_db.get_sip_events()
        assert len(events) == 2

        # Get events by profile
        profile_events = temp_db.get_sip_events(profile_id=profile_id)
        assert len(profile_events) == 2

        # Get events by date range
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.now().replace(
            hour=23, minute=59, second=59, microsecond=999999
        )

        date_events = temp_db.get_sip_events(start_date=start_date, end_date=end_date)
        assert len(date_events) == 2

    def test_get_or_create_daily_goal(self, temp_db):
        """Test getting or creating daily goal."""
        target_date = date.today()
        target_ml = 2000

        # Create goal
        goal = temp_db.get_or_create_daily_goal(target_date, target_ml)

        assert goal.date.date() == target_date
        assert goal.target_ml == target_ml
        assert goal.achieved_ml == 0.0
        assert goal.is_achieved is False
        assert goal.streak_days == 0

        # Get existing goal
        existing_goal = temp_db.get_or_create_daily_goal(target_date, target_ml)
        assert existing_goal.id == goal.id

    def test_update_daily_goal(self, temp_db):
        """Test updating daily goal."""
        # Create goal
        target_date = date.today()
        goal = temp_db.get_or_create_daily_goal(target_date, 2000)

        # Update goal
        goal.achieved_ml = 1500.0
        goal.is_achieved = False
        goal.streak_days = 5

        success = temp_db.update_daily_goal(goal)
        assert success is True

        # Verify update
        updated_goal = temp_db.get_or_create_daily_goal(target_date, 2000)
        assert updated_goal.achieved_ml == 1500.0
        assert updated_goal.is_achieved is False
        assert updated_goal.streak_days == 5

    def test_get_daily_stats(self, temp_db):
        """Test getting daily statistics."""
        # Create cup profile
        profile = CupProfile(name="Test Cup", size_ml=250, sips_per_cup=10)
        profile_id = temp_db.create_cup_profile(profile)

        # Create sip events
        today = date.today()
        event1 = SipEvent(
            timestamp=datetime.combine(today, datetime.min.time()),
            profile_id=profile_id,
            ml_estimate=25.0,
            source=EventSource.AUTO,
        )
        event2 = SipEvent(
            timestamp=datetime.combine(today, datetime.min.time()),
            profile_id=profile_id,
            ml_estimate=30.0,
            source=EventSource.MANUAL,
        )

        temp_db.create_sip_event(event1)
        temp_db.create_sip_event(event2)

        # Get daily stats
        stats = temp_db.get_daily_stats(today)

        assert stats.total_ml == 55.0
        assert stats.total_sips == 2
        assert stats.total_cups == 0.22  # 55ml / 250ml per cup
        assert len(stats.events) == 2

    def test_get_user_settings(self, temp_db):
        """Test getting user settings."""
        settings = temp_db.get_user_settings()

        assert settings is not None
        assert settings.theme == ThemeMode.AUTO
        assert settings.detection_engine == DetectionEngine.HEURISTICS
        assert settings.enable_notifications is True
        assert settings.window_width == 1200
        assert settings.window_height == 800

    def test_update_user_settings(self, temp_db):
        """Test updating user settings."""
        # Get current settings
        settings = temp_db.get_user_settings()

        # Update settings
        settings.theme = ThemeMode.DARK
        settings.detection_engine = DetectionEngine.MEDIAPIPE
        settings.enable_notifications = False
        settings.window_width = 1600
        settings.window_height = 900

        success = temp_db.update_user_settings(settings)
        assert success is True

        # Verify update
        updated_settings = temp_db.get_user_settings()
        assert updated_settings.theme == ThemeMode.DARK
        assert updated_settings.detection_engine == DetectionEngine.MEDIAPIPE
        assert updated_settings.enable_notifications is False
        assert updated_settings.window_width == 1600
        assert updated_settings.window_height == 900
