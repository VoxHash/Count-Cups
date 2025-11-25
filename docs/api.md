# API Reference

API documentation for Count-Cups developers.

## Overview

Count-Cups provides a Python API for programmatic access to core functionality.

## Core Modules

### `app.core.config`

Configuration management using Pydantic settings.

#### `Settings`

Application settings class.

```python
from app.core.config import settings

# Access settings
print(settings.app_name)
print(settings.detection_engine)
print(settings.default_theme)
```

**Key Attributes**:
- `app_name`: Application name
- `app_version`: Application version
- `detection_engine`: Detection engine (heuristics/mediapipe)
- `default_theme`: Default theme
- `camera_index`: Camera device index

### `app.core.db`

Database operations and data persistence.

#### `Database`

Database connection and operations.

```python
from app.core.db import Database

db = Database()

# Get daily stats
stats = db.get_daily_stats(date.today())

# Add sip event
db.add_sip_event(sip_event)

# Get cup profiles
profiles = db.get_cup_profiles()
```

**Key Methods**:
- `get_daily_stats(date)`: Get daily statistics
- `add_sip_event(event)`: Add sip event
- `get_cup_profiles()`: Get all cup profiles
- `create_cup_profile(profile)`: Create cup profile

### `app.core.models`

Data models and business entities.

#### `CupProfile`

Cup profile model.

```python
from app.core.models import CupProfile

profile = CupProfile(
    name="Coffee Mug",
    size_ml=250,
    sips_per_cup=10
)
```

#### `SipEvent`

Sip event model.

```python
from app.core.models import SipEvent, EventSource
from datetime import datetime

event = SipEvent(
    timestamp=datetime.now(),
    profile_id=1,
    ml_estimate=25.0,
    source=EventSource.AUTO
)
```

#### `DailyStats`

Daily statistics model.

```python
from app.core.models import DailyStats

stats = DailyStats(
    date=date.today(),
    total_ml=1500.0,
    total_cups=6.0,
    total_sips=60
)
```

### `app.core.sip_logic`

Sip tracking and aggregation logic.

#### `SipTracker`

Main sip tracking coordinator.

```python
from app.core.sip_logic import SipTracker

tracker = SipTracker()

# Process detection
tracker.process_detection(detection_result)

# Add manual sip
tracker.add_manual_sip(profile_id=1)

# Get daily stats
stats = tracker.get_daily_stats()
```

**Key Methods**:
- `process_detection(detection)`: Process detection result
- `add_manual_sip(profile_id)`: Add manual sip entry
- `get_daily_stats()`: Get daily statistics
- `get_weekly_stats()`: Get weekly statistics

#### `SipAggregator`

Aggregates detection results into sip events.

```python
from app.core.sip_logic import SipAggregator

aggregator = SipAggregator()
result = aggregator.process_detection(detection)
```

#### `CupConverter`

Converts between sips, milliliters, and cups.

```python
from app.core.sip_logic import CupConverter

converter = CupConverter()
cups = converter.sips_to_cups(sips=10, profile_id=1)
ml = converter.estimate_sip_ml(profile_id=1)
```

### `app.core.detection`

Detection engine interfaces.

#### `DetectionEngine`

Base class for detection engines.

```python
from app.core.detection.base import DetectionEngine

class CustomDetector(DetectionEngine):
    def detect(self, frame):
        # Custom detection logic
        return detection_result
```

#### `HeuristicDetector`

Heuristic-based detection engine.

```python
from app.core.detection.heuristics import AdvancedHeuristicDetector

detector = AdvancedHeuristicDetector()
result = detector.detect(frame)
```

#### `MediaPipeDetector`

MediaPipe-based detection engine.

```python
from app.core.detection.mediapipe_impl import AdvancedMediaPipeDetector

detector = AdvancedMediaPipeDetector()
result = detector.detect(frame)
```

### `app.core.exporter`

Data export functionality.

#### `Exporter`

Export data to various formats.

```python
from app.core.exporter import Exporter

exporter = Exporter()

# Export to CSV
exporter.export_to_csv(output_path="data.csv")

# Export to JSON
exporter.export_to_json(output_path="data.json")
```

## Usage Examples

### Basic Tracking

```python
from app.core.sip_logic import SipTracker
from app.core.db import Database

# Initialize
tracker = SipTracker()
db = Database()

# Process detection
detection = get_detection_from_camera()
tracker.process_detection(detection)

# Get stats
stats = tracker.get_daily_stats()
print(f"Today's intake: {stats.total_ml}ml")
```

### Custom Detection

```python
from app.core.detection.base import DetectionEngine
from app.core.models import DetectionResult

class MyDetector(DetectionEngine):
    def detect(self, frame):
        # Custom detection logic
        return DetectionResult(
            has_sip=True,
            confidence=0.85,
            face_detected=True,
            hand_detected=True
        )
```

### Data Export

```python
from app.core.exporter import Exporter
from datetime import date, timedelta

exporter = Exporter()

# Export last 7 days
start_date = date.today() - timedelta(days=7)
end_date = date.today()

exporter.export_to_csv(
    output_path="weekly_data.csv",
    start_date=start_date,
    end_date=end_date
)
```

## Error Handling

### Database Errors

```python
from app.core.db import Database, DatabaseError

try:
    db = Database()
    stats = db.get_daily_stats(date.today())
except DatabaseError as e:
    print(f"Database error: {e}")
```

### Detection Errors

```python
from app.core.detection.base import DetectionError

try:
    result = detector.detect(frame)
except DetectionError as e:
    print(f"Detection error: {e}")
```

## Type Hints

All functions and classes use type hints for better IDE support and documentation.

```python
from typing import Optional, List
from datetime import date
from app.core.models import SipEvent, DailyStats

def get_events(date: date) -> List[SipEvent]:
    """Get events for a specific date."""
    # Implementation
    pass
```

## Logging

Use the logging module for application logging.

```python
from app.core.logging import get_logger

logger = get_logger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

## Configuration

Access configuration through the settings object.

```python
from app.core.config import settings

# Read settings
engine = settings.detection_engine
theme = settings.default_theme

# Update settings (runtime)
settings.detection_engine = "mediapipe"
```

## Next Steps

- **Architecture**: See [Architecture](architecture.md) for system design
- **Examples**: Check [Examples](examples/) for code samples
- **Development**: See [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines

---

**API Reference complete!** Use the API to extend Count-Cups functionality.

