"""Data export and import functionality."""

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from app.core.logging import get_logger
from app.core.models import CupProfile, DailyStats, EventSource, ExportData, SipEvent

logger = get_logger(__name__)


class DataExporter:
    """Handles data export and import operations."""

    def __init__(self, output_dir: Path | None = None):
        """Initialize data exporter.

        Args:
            output_dir: Directory for export files (defaults to current directory)
        """
        self.output_dir = output_dir or Path.cwd()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_daily_stats_csv(
        self, daily_stats: list[DailyStats], filename: str | None = None
    ) -> Path:
        """Export daily statistics to CSV.

        Args:
            daily_stats: List of daily statistics
            filename: Output filename (defaults to auto-generated)

        Returns:
            Path to exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"daily_stats_{timestamp}.csv"

        filepath = self.output_dir / filename

        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "date",
                "total_ml",
                "total_sips",
                "total_cups",
                "goal_ml",
                "goal_achieved",
                "progress_percentage",
                "streak_days",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for stats in daily_stats:
                writer.writerow(
                    {
                        "date": stats.date.strftime("%Y-%m-%d"),
                        "total_ml": stats.total_ml,
                        "total_sips": stats.total_sips,
                        "total_cups": stats.total_cups,
                        "goal_ml": stats.goal_ml,
                        "goal_achieved": stats.goal_achieved,
                        "progress_percentage": stats.progress_percentage,
                        "streak_days": stats.streak_days,
                    }
                )

        logger.info(f"Daily stats exported to {filepath}")
        return filepath

    def export_sip_events_csv(
        self, sip_events: list[SipEvent], filename: str | None = None
    ) -> Path:
        """Export sip events to CSV.

        Args:
            sip_events: List of sip events
            filename: Output filename (defaults to auto-generated)

        Returns:
            Path to exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sip_events_{timestamp}.csv"

        filepath = self.output_dir / filename

        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "timestamp",
                "profile_id",
                "ml_estimate",
                "source",
                "confidence",
                "detection_data",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for event in sip_events:
                writer.writerow(
                    {
                        "timestamp": event.timestamp.isoformat(),
                        "profile_id": event.profile_id,
                        "ml_estimate": event.ml_estimate,
                        "source": event.source.value,
                        "confidence": event.confidence,
                        "detection_data": json.dumps(event.detection_data)
                        if event.detection_data
                        else "",
                    }
                )

        logger.info(f"Sip events exported to {filepath}")
        return filepath

    def export_cup_profiles_csv(
        self, cup_profiles: list[CupProfile], filename: str | None = None
    ) -> Path:
        """Export cup profiles to CSV.

        Args:
            cup_profiles: List of cup profiles
            filename: Output filename (defaults to auto-generated)

        Returns:
            Path to exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cup_profiles_{timestamp}.csv"

        filepath = self.output_dir / filename

        with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "id",
                "name",
                "size_ml",
                "sips_per_cup",
                "color",
                "is_default",
                "created_at",
                "updated_at",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for profile in cup_profiles:
                writer.writerow(
                    {
                        "id": profile.id,
                        "name": profile.name,
                        "size_ml": profile.size_ml,
                        "sips_per_cup": profile.sips_per_cup,
                        "color": profile.color or "",
                        "is_default": profile.is_default,
                        "created_at": profile.created_at.isoformat(),
                        "updated_at": profile.updated_at.isoformat(),
                    }
                )

        logger.info(f"Cup profiles exported to {filepath}")
        return filepath

    def export_complete_data(
        self, export_data: ExportData, filename: str | None = None
    ) -> Path:
        """Export complete dataset to JSON.

        Args:
            export_data: Complete export data
            filename: Output filename (defaults to auto-generated)

        Returns:
            Path to exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"count_cups_export_{timestamp}.json"

        filepath = self.output_dir / filename

        # Convert to dictionary for JSON serialization
        export_dict = {
            "export_timestamp": export_data.export_timestamp.isoformat(),
            "start_date": export_data.start_date.isoformat(),
            "end_date": export_data.end_date.isoformat(),
            "daily_stats": [
                {
                    "date": stats.date.isoformat(),
                    "total_ml": stats.total_ml,
                    "total_sips": stats.total_sips,
                    "total_cups": stats.total_cups,
                    "goal_ml": stats.goal_ml,
                    "goal_achieved": stats.goal_achieved,
                    "progress_percentage": stats.progress_percentage,
                    "streak_days": stats.streak_days,
                    "events": [
                        {
                            "timestamp": event.timestamp.isoformat(),
                            "profile_id": event.profile_id,
                            "ml_estimate": event.ml_estimate,
                            "source": event.source.value,
                            "confidence": event.confidence,
                            "detection_data": event.detection_data,
                        }
                        for event in stats.events
                    ],
                }
                for stats in export_data.daily_stats
            ],
            "cup_profiles": [
                {
                    "id": profile.id,
                    "name": profile.name,
                    "size_ml": profile.size_ml,
                    "sips_per_cup": profile.sips_per_cup,
                    "color": profile.color,
                    "is_default": profile.is_default,
                    "created_at": profile.created_at.isoformat(),
                    "updated_at": profile.updated_at.isoformat(),
                }
                for profile in export_data.cup_profiles
            ],
        }

        with open(filepath, "w", encoding="utf-8") as jsonfile:
            json.dump(export_dict, jsonfile, indent=2, ensure_ascii=False)

        logger.info(f"Complete data exported to {filepath}")
        return filepath

    def import_daily_stats_csv(self, filepath: Path) -> list[DailyStats]:
        """Import daily statistics from CSV.

        Args:
            filepath: Path to CSV file

        Returns:
            List of daily statistics
        """
        daily_stats = []

        with open(filepath, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Parse date
                date_obj = datetime.fromisoformat(row["date"]).date()

                # Create DailyStats object
                stats = DailyStats(
                    date=datetime.combine(date_obj, datetime.min.time()),
                    total_ml=float(row["total_ml"]),
                    total_sips=int(row["total_sips"]),
                    total_cups=float(row["total_cups"]),
                    goal_ml=int(row["goal_ml"]),
                    goal_achieved=row["goal_achieved"].lower() == "true",
                    progress_percentage=float(row["progress_percentage"]),
                    streak_days=int(row["streak_days"]),
                    events=[],  # Events not included in this import
                )
                daily_stats.append(stats)

        logger.info(f"Imported {len(daily_stats)} daily stats from {filepath}")
        return daily_stats

    def import_sip_events_csv(self, filepath: Path) -> list[SipEvent]:
        """Import sip events from CSV.

        Args:
            filepath: Path to CSV file

        Returns:
            List of sip events
        """
        sip_events = []

        with open(filepath, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Parse detection data
                detection_data = None
                if row["detection_data"]:
                    try:
                        detection_data = json.loads(row["detection_data"])
                    except json.JSONDecodeError:
                        logger.warning(
                            f"Failed to parse detection data for event at {row['timestamp']}"
                        )

                # Create SipEvent object
                # Convert source string to EventSource enum
                source_str = str(row["source"])
                source = EventSource.AUTO if source_str == "auto" else EventSource.MANUAL
                
                event = SipEvent(
                    timestamp=datetime.fromisoformat(row["timestamp"]),
                    profile_id=int(row["profile_id"]),
                    ml_estimate=float(row["ml_estimate"]),
                    source=source,
                    confidence=float(row["confidence"]) if row["confidence"] else None,
                    detection_data=detection_data,
                )
                sip_events.append(event)

        logger.info(f"Imported {len(sip_events)} sip events from {filepath}")
        return sip_events

    def import_cup_profiles_csv(self, filepath: Path) -> list[CupProfile]:
        """Import cup profiles from CSV.

        Args:
            filepath: Path to CSV file

        Returns:
            List of cup profiles
        """
        cup_profiles = []

        with open(filepath, encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Create CupProfile object
                profile = CupProfile(
                    id=int(row["id"]) if row["id"] else None,
                    name=row["name"],
                    size_ml=int(row["size_ml"]),
                    sips_per_cup=int(row["sips_per_cup"]),
                    color=row["color"] if row["color"] else None,
                    is_default=row["is_default"].lower() == "true",
                    created_at=datetime.fromisoformat(row["created_at"]),
                    updated_at=datetime.fromisoformat(row["updated_at"]),
                )
                cup_profiles.append(profile)

        logger.info(f"Imported {len(cup_profiles)} cup profiles from {filepath}")
        return cup_profiles

    def create_export_summary(self, export_data: ExportData) -> dict[str, Any]:
        """Create a summary of export data.

        Args:
            export_data: Export data to summarize

        Returns:
            Summary dictionary
        """
        total_days = len(export_data.daily_stats)
        total_ml = sum(stats.total_ml for stats in export_data.daily_stats)
        total_sips = sum(stats.total_sips for stats in export_data.daily_stats)
        goal_achieved_days = sum(
            1 for stats in export_data.daily_stats if stats.goal_achieved
        )

        return {
            "export_timestamp": export_data.export_timestamp.isoformat(),
            "date_range": {
                "start": export_data.start_date.isoformat(),
                "end": export_data.end_date.isoformat(),
            },
            "summary": {
                "total_days": total_days,
                "total_ml": total_ml,
                "total_sips": total_sips,
                "total_cups": total_ml / 250.0,  # Assuming 250ml per cup
                "goal_achievement_rate": (goal_achieved_days / total_days * 100)
                if total_days > 0
                else 0,
                "average_daily_ml": total_ml / total_days if total_days > 0 else 0,
                "average_daily_sips": total_sips / total_days if total_days > 0 else 0,
            },
            "cup_profiles_count": len(export_data.cup_profiles),
        }
