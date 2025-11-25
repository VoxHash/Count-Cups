"""Data models for the Count-Cups application."""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class EventSource(str, Enum):
    """Source of a sip event."""
    AUTO = "auto"
    MANUAL = "manual"


class ThemeMode(str, Enum):
    """Theme mode options."""
    AUTO = "auto"
    LIGHT = "light"
    DARK = "dark"
    DRACULA = "dracula"


class DetectionEngine(str, Enum):
    """Available detection engines."""
    HEURISTICS = "heuristics"
    MEDIAPIPE = "mediapipe"


class CupProfile(BaseModel):
    """Cup profile configuration."""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=50)
    size_ml: int = Field(..., gt=0, le=2000)
    sips_per_cup: int = Field(..., gt=0, le=100)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    is_default: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True


class SipEvent(BaseModel):
    """A single sip event."""
    id: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    profile_id: int
    ml_estimate: float = Field(..., ge=0.0, le=1000.0)
    source: EventSource = EventSource.AUTO
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    detection_data: Optional[dict] = None
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True


class DailyGoal(BaseModel):
    """Daily water intake goal."""
    id: Optional[int] = None
    date: datetime = Field(..., description="Date for this goal (time component ignored)")
    target_ml: int = Field(..., gt=0, le=10000)
    achieved_ml: float = Field(default=0.0, ge=0.0)
    is_achieved: bool = False
    streak_days: int = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @property
    def progress_percentage(self) -> float:
        """Calculate progress as percentage."""
        if self.target_ml == 0:
            return 0.0
        return min(100.0, (self.achieved_ml / self.target_ml) * 100.0)
    
    @property
    def remaining_ml(self) -> float:
        """Calculate remaining milliliters."""
        return max(0.0, self.target_ml - self.achieved_ml)
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True


class UserSettings(BaseModel):
    """User application settings."""
    id: Optional[int] = None
    theme: ThemeMode = ThemeMode.AUTO
    detection_engine: DetectionEngine = DetectionEngine.HEURISTICS
    enable_notifications: bool = True
    goal_reminder_hour: int = Field(default=20, ge=0, le=23)
    goal_reminder_minute: int = Field(default=0, ge=0, le=59)
    default_cup_profile_id: Optional[int] = None
    window_width: int = Field(default=1200, ge=800, le=3840)
    window_height: int = Field(default=800, ge=600, le=2160)
    window_maximized: bool = False
    camera_index: int = Field(default=0, ge=0, le=10)
    camera_width: int = Field(default=640, ge=320, le=1920)
    camera_height: int = Field(default=480, ge=240, le=1080)
    camera_fps: int = Field(default=30, ge=15, le=60)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True


class DetectionResult(BaseModel):
    """Result from detection engine."""
    has_sip: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    head_tilt_angle: Optional[float] = None
    hand_face_distance: Optional[float] = None
    face_center: Optional[tuple[int, int]] = None
    hand_center: Optional[tuple[int, int]] = None
    detection_data: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True


class DailyStats(BaseModel):
    """Daily statistics summary."""
    date: datetime
    total_ml: float
    total_sips: int
    total_cups: float
    goal_ml: int
    goal_achieved: bool
    progress_percentage: float
    streak_days: int
    events: List[SipEvent] = Field(default_factory=list)
    
    @property
    def remaining_ml(self) -> float:
        """Calculate remaining milliliters."""
        return max(0.0, self.goal_ml - self.total_ml)
    
    @property
    def cups_consumed(self) -> float:
        """Calculate cups consumed (assuming 250ml per cup)."""
        return self.total_ml / 250.0
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True


class WeeklyStats(BaseModel):
    """Weekly statistics summary."""
    week_start: datetime
    week_end: datetime
    total_ml: float
    total_sips: int
    total_cups: float
    average_daily_ml: float
    goal_achieved_days: int
    streak_days: int
    daily_stats: List[DailyStats] = Field(default_factory=list)
    
    @property
    def goal_achievement_rate(self) -> float:
        """Calculate goal achievement rate as percentage."""
        if not self.daily_stats:
            return 0.0
        return (self.goal_achieved_days / len(self.daily_stats)) * 100.0
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True


class ExportData(BaseModel):
    """Data structure for CSV export."""
    start_date: datetime
    end_date: datetime
    daily_stats: List[DailyStats]
    cup_profiles: List[CupProfile]
    export_timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
