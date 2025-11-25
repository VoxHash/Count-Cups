# Example 1: Basic Usage

Basic example of using Count-Cups programmatically.

## Overview

This example demonstrates how to:
- Initialize Count-Cups components
- Process detection results
- Retrieve daily statistics
- Add manual sip entries

## Code

```python
"""Basic Count-Cups usage example."""

from datetime import date
from app.core.sip_logic import SipTracker
from app.core.db import Database
from app.core.models import DetectionResult, EventSource

# Initialize components
tracker = SipTracker()
db = Database()

# Simulate detection result
detection = DetectionResult(
    has_sip=True,
    confidence=0.85,
    face_detected=True,
    hand_detected=True
)

# Process detection
tracker.process_detection(detection)

# Get daily statistics
stats = tracker.get_daily_stats()
print(f"Today's intake: {stats.total_ml}ml")
print(f"Cups consumed: {stats.total_cups}")
print(f"Sips detected: {stats.total_sips}")

# Add manual sip entry
tracker.add_manual_sip(profile_id=1)

# Get updated stats
updated_stats = tracker.get_daily_stats()
print(f"Updated intake: {updated_stats.total_ml}ml")
```

## Explanation

1. **Initialize Components**: Create `SipTracker` and `Database` instances
2. **Process Detection**: Pass detection results to the tracker
3. **Retrieve Statistics**: Get daily statistics from the tracker
4. **Manual Entry**: Add manual sip entries when needed

## Running the Example

```bash
python examples/example_01_basic.py
```

## Expected Output

```
Today's intake: 25.0ml
Cups consumed: 0.1
Sips detected: 1
Updated intake: 50.0ml
```

## Next Steps

- See [Example 2](example-02.md) for advanced usage
- Check [API Reference](../api.md) for more details
- Review [Usage Guide](../usage.md) for user documentation

