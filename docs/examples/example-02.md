# Example 2: Custom Detection Engine

Example of creating a custom detection engine.

## Overview

This example demonstrates how to:
- Create a custom detection engine
- Implement detection logic
- Integrate with Count-Cups

## Code

```python
"""Custom detection engine example."""

import cv2
import numpy as np
from app.core.detection.base import DetectionEngine
from app.core.models import DetectionResult

class CustomDetector(DetectionEngine):
    """Custom detection engine example."""
    
    def __init__(self):
        """Initialize custom detector."""
        super().__init__()
        # Initialize your detection models here
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    def detect(self, frame: np.ndarray) -> DetectionResult:
        """Detect sips in frame.
        
        Args:
            frame: Input frame from camera
            
        Returns:
            DetectionResult with detection information
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5
        )
        
        # Simple detection logic
        has_sip = len(faces) > 0
        confidence = 0.7 if has_sip else 0.0
        
        return DetectionResult(
            has_sip=has_sip,
            confidence=confidence,
            face_detected=len(faces) > 0,
            hand_detected=False  # Implement hand detection
        )
    
    def cleanup(self):
        """Clean up resources."""
        # Clean up any resources
        pass

# Usage
if __name__ == "__main__":
    # Initialize detector
    detector = CustomDetector()
    
    # Open camera
    cap = cv2.VideoCapture(0)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detect
            result = detector.detect(frame)
            
            # Process result
            if result.has_sip:
                print(f"Sip detected! Confidence: {result.confidence}")
            
    finally:
        cap.release()
        detector.cleanup()
```

## Explanation

1. **Inherit from DetectionEngine**: Create a class that inherits from `DetectionEngine`
2. **Implement detect()**: Implement the detection logic
3. **Return DetectionResult**: Return a `DetectionResult` object
4. **Cleanup**: Implement cleanup if needed

## Integration

To use your custom detector:

```python
from app.core.sip_logic import SipTracker

# Create custom detector
detector = CustomDetector()

# Use with tracker
tracker = SipTracker()
result = detector.detect(frame)
tracker.process_detection(result)
```

## Next Steps

- See [Example 1](example-01.md) for basic usage
- Check [API Reference](../api.md) for API details
- Review [Architecture](../architecture.md) for system design

