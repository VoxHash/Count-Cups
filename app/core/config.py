"""Application configuration using Pydantic settings."""

from pathlib import Path
from typing import Any

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application
    app_name: str = Field(default="Count-Cups", env="APP_NAME")  # type: ignore[call-overload]
    app_version: str = Field(default="1.0.0", env="APP_VERSION")  # type: ignore[call-overload]
    debug: bool = Field(default=False, env="DEBUG")  # type: ignore[call-overload]
    log_level: str = Field(default="INFO", env="LOG_LEVEL")  # type: ignore[call-overload]

    # Database
    database_url: str = Field(default="sqlite:///count_cups.db", env="DATABASE_URL")  # type: ignore[call-overload]

    # Detection Settings
    detection_engine: str = Field(default="heuristics", env="DETECTION_ENGINE")  # type: ignore[call-overload]
    sip_duration_min: float = Field(default=0.8, env="SIP_DURATION_MIN")  # type: ignore[call-overload]
    sip_duration_max: float = Field(default=3.5, env="SIP_DURATION_MAX")  # type: ignore[call-overload]
    head_tilt_threshold: float = Field(default=25.0, env="HEAD_TILT_THRESHOLD")  # type: ignore[call-overload]
    hand_face_distance_threshold: float = Field(  # type: ignore[call-overload]
        default=100.0, env="HAND_FACE_DISTANCE_THRESHOLD"
    )

    # Calibration
    default_cup_size_ml: int = Field(default=250, env="DEFAULT_CUP_SIZE_ML")  # type: ignore[call-overload]
    default_sips_per_cup: int = Field(default=10, env="DEFAULT_SIPS_PER_CUP")  # type: ignore[call-overload]

    # Notifications
    enable_notifications: bool = Field(default=True, env="ENABLE_NOTIFICATIONS")  # type: ignore[call-overload]
    goal_reminder_hour: int = Field(default=20, env="GOAL_REMINDER_HOUR")  # type: ignore[call-overload]
    goal_reminder_minute: int = Field(default=0, env="GOAL_REMINDER_MINUTE")  # type: ignore[call-overload]

    # Telemetry
    enable_telemetry: bool = Field(default=False, env="ENABLE_TELEMETRY")  # type: ignore[call-overload]
    telemetry_endpoint: str = Field(default="", env="TELEMETRY_ENDPOINT")  # type: ignore[call-overload]

    # UI Settings
    default_theme: str = Field(default="auto", env="DEFAULT_THEME")  # type: ignore[call-overload]
    window_width: int = Field(default=1200, env="WINDOW_WIDTH")  # type: ignore[call-overload]
    window_height: int = Field(default=800, env="WINDOW_HEIGHT")  # type: ignore[call-overload]
    window_maximized: bool = Field(default=False, env="WINDOW_MAXIMIZED")  # type: ignore[call-overload]

    # Camera Settings
    camera_index: int = Field(default=0, env="CAMERA_INDEX")  # type: ignore[call-overload]
    camera_width: int = Field(default=640, env="CAMERA_WIDTH")  # type: ignore[call-overload]
    camera_height: int = Field(default=480, env="CAMERA_HEIGHT")  # type: ignore[call-overload]
    camera_fps: int = Field(default=30, env="CAMERA_FPS")  # type: ignore[call-overload]

    # Paths
    app_dir: Path = Field(default_factory=lambda: Path.home() / ".count-cups")
    data_dir: Path = Field(default_factory=lambda: Path.home() / ".count-cups" / "data")
    logs_dir: Path = Field(default_factory=lambda: Path.home() / ".count-cups" / "logs")
    assets_dir: Path = Field(
        default_factory=lambda: Path(__file__).parent.parent / "assets"
    )

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @validator("detection_engine")
    def validate_detection_engine(cls, v: str) -> str:
        """Validate detection engine selection."""
        valid_engines = ["heuristics", "mediapipe"]
        if v not in valid_engines:
            raise ValueError(f"detection_engine must be one of {valid_engines}")
        return v

    @validator("log_level")
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v.upper()

    @validator("default_theme")
    def validate_theme(cls, v: str) -> str:
        """Validate theme selection."""
        valid_themes = ["auto", "light", "dark", "dracula"]
        if v.lower() not in valid_themes:
            raise ValueError(f"default_theme must be one of {valid_themes}")
        return v.lower()

    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        self.app_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def get_database_path(self) -> Path:
        """Get the full path to the database file."""
        if self.database_url.startswith("sqlite:///"):
            db_name = self.database_url.replace("sqlite:///", "")
            return self.data_dir / db_name
        return Path(self.database_url)

    def to_dict(self) -> dict[str, Any]:
        """Convert settings to dictionary."""
        return self.dict()


# Global settings instance
settings = Settings()
