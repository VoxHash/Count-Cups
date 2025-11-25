"""Base detection interface and abstract classes."""

from abc import ABC, abstractmethod

import cv2
import numpy as np

from app.core.models import DetectionResult


class DetectionEngine(ABC):
    """Abstract base class for detection engines."""

    def __init__(self, **kwargs):
        """Initialize detection engine with configuration."""
        self.config = kwargs

    @abstractmethod
    def detect(self, frame: np.ndarray) -> DetectionResult | None:
        """Detect sip events in a frame.

        Args:
            frame: Input video frame (BGR format)

        Returns:
            DetectionResult if sip detected, None otherwise
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if detection engine is available.

        Returns:
            True if engine can be used, False otherwise
        """
        pass

    def cleanup(self) -> None:
        """Clean up resources."""
        pass


class HeuristicDetector(DetectionEngine):
    """Heuristic-based detection using OpenCV only."""

    def __init__(self, **kwargs):
        """Initialize heuristic detector."""
        super().__init__(**kwargs)

        # Detection parameters
        self.head_tilt_threshold = kwargs.get("head_tilt_threshold", 25.0)
        self.hand_face_distance_threshold = kwargs.get(
            "hand_face_distance_threshold", 100.0
        )
        self.sip_duration_min = kwargs.get("sip_duration_min", 0.8)
        self.sip_duration_max = kwargs.get("sip_duration_max", 3.5)

        # State tracking
        self.last_detection_time = 0.0
        self.sip_start_time = 0.0
        self.sip_in_progress = False
        self.detection_frames = []

        # Load face cascade
        self.face_cascade = cv2.CascadeClassifier(
            str(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        )

        # Skin color detection parameters
        self.lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    def detect(self, frame: np.ndarray) -> DetectionResult | None:
        """Detect sip events using heuristics."""
        import time

        current_time = time.time()

        # Check if we're in cooldown period
        if current_time - self.last_detection_time < 1.0:  # 1 second cooldown
            return None

        # Detect face
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) == 0:
            return None

        # Use the largest face
        face = max(faces, key=lambda x: x[2] * x[3])
        x, y, w, h = face
        face_center = (x + w // 2, y + h // 2)

        # Detect hand using skin color
        hand_center = self._detect_hand_by_skin_color(frame)

        if hand_center is None:
            return None

        # Calculate head tilt (simplified)
        head_tilt_angle = self._calculate_head_tilt(face)

        # Calculate hand-face distance
        hand_face_distance = np.sqrt(
            (hand_center[0] - face_center[0]) ** 2
            + (hand_center[1] - face_center[1]) ** 2
        )

        # Check if conditions are met for a sip
        has_sip = (
            hand_face_distance < self.hand_face_distance_threshold
            and abs(head_tilt_angle) > self.head_tilt_threshold
        )

        if has_sip:
            # Start or continue sip detection
            if not self.sip_in_progress:
                self.sip_in_progress = True
                self.sip_start_time = current_time
                self.detection_frames = []

            self.detection_frames.append(current_time)

            # Check if sip duration is sufficient
            sip_duration = current_time - self.sip_start_time
            if sip_duration >= self.sip_duration_min:
                # Complete the sip detection
                self.sip_in_progress = False
                self.last_detection_time = current_time
                self.detection_frames = []

                # Calculate confidence based on detection quality
                confidence = min(1.0, len(self.detection_frames) / 10.0)

                return DetectionResult(
                    has_sip=True,
                    confidence=confidence,
                    head_tilt_angle=head_tilt_angle,
                    hand_face_distance=hand_face_distance,
                    face_center=face_center,
                    hand_center=hand_center,
                    detection_data={
                        "sip_duration": sip_duration,
                        "detection_frames": len(self.detection_frames),
                    },
                )

        # Reset if sip duration exceeds maximum
        if self.sip_in_progress:
            sip_duration = current_time - self.sip_start_time
            if sip_duration > self.sip_duration_max:
                self.sip_in_progress = False
                self.detection_frames = []

        return None

    def _detect_hand_by_skin_color(self, frame: np.ndarray) -> tuple[int, int] | None:
        """Detect hand using skin color detection."""
        # Convert to HSV for better skin color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Create mask for skin color
        mask = cv2.inRange(hsv, self.lower_skin, self.upper_skin)

        # Apply morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return None

        # Get the largest contour (likely the hand)
        largest_contour = max(contours, key=cv2.contourArea)

        # Check if contour is large enough
        if cv2.contourArea(largest_contour) < 1000:
            return None

        # Get bounding rectangle and return center
        x, y, w, h = cv2.boundingRect(largest_contour)
        return (x + w // 2, y + h // 2)

    def _calculate_head_tilt(self, face: tuple[int, int, int, int]) -> float:
        """Calculate head tilt angle (simplified)."""
        x, y, w, h = face

        # Simple heuristic: compare width to height ratio
        aspect_ratio = w / h

        # Normal face has aspect ratio around 0.8
        # Tilted face will have different ratio
        tilt_factor = abs(aspect_ratio - 0.8) * 100

        # Convert to angle (rough approximation)
        angle = tilt_factor * 0.5

        return angle

    def is_available(self) -> bool:
        """Check if heuristic detector is available."""
        return self.face_cascade is not None

    def cleanup(self) -> None:
        """Clean up resources."""
        self.detection_frames = []


class MediaPipeDetector(DetectionEngine):
    """MediaPipe-based detection (optional)."""

    def __init__(self, **kwargs):
        """Initialize MediaPipe detector."""
        super().__init__(**kwargs)
        self.mp_hands = None
        self.mp_face_mesh = None
        self.hands = None
        self.face_mesh = None

        try:
            import mediapipe as mp

            self.mp_hands = mp.solutions.hands
            self.mp_face_mesh = mp.solutions.face_mesh
            self.hands = self.mp_hands.Hands(
                max_num_hands=1,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5,
            )
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5,
            )
        except ImportError:
            pass

    def detect(self, frame: np.ndarray) -> DetectionResult | None:
        """Detect sip events using MediaPipe."""
        if not self.is_available():
            return None

        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process hands
        hand_results = self.hands.process(rgb_frame)

        # Process face
        face_results = self.face_mesh.process(rgb_frame)

        if (
            not hand_results.multi_hand_landmarks
            or not face_results.multi_face_landmarks
        ):
            return None

        # Get hand landmarks
        hand_landmarks = hand_results.multi_hand_landmarks[0]
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        wrist_pos = (int(wrist.x * frame.shape[1]), int(wrist.y * frame.shape[0]))

        # Get face landmarks
        face_landmarks = face_results.multi_face_landmarks[0]

        # Get mouth center (simplified)
        mouth_center = self._get_mouth_center(face_landmarks, frame.shape)

        # Calculate distance between wrist and mouth
        distance = np.sqrt(
            (wrist_pos[0] - mouth_center[0]) ** 2
            + (wrist_pos[1] - mouth_center[1]) ** 2
        )

        # Calculate head tilt using face landmarks
        head_tilt = self._calculate_head_tilt_mediapipe(face_landmarks, frame.shape)

        # Check if conditions are met for a sip
        has_sip = distance < self.config.get(
            "hand_face_distance_threshold", 100.0
        ) and abs(head_tilt) > self.config.get("head_tilt_threshold", 25.0)

        if has_sip:
            confidence = min(
                1.0, 1.0 - (distance / 200.0)
            )  # Higher confidence for closer hand

            return DetectionResult(
                has_sip=True,
                confidence=confidence,
                head_tilt_angle=head_tilt,
                hand_face_distance=distance,
                face_center=mouth_center,
                hand_center=wrist_pos,
                detection_data={
                    "hand_landmarks": len(hand_landmarks.landmark),
                    "face_landmarks": len(face_landmarks.landmark),
                },
            )

        return None

    def _get_mouth_center(self, face_landmarks, frame_shape: tuple) -> tuple[int, int]:
        """Get mouth center from face landmarks."""
        # MediaPipe face mesh mouth landmarks (simplified)
        mouth_landmarks = [61, 84, 17, 314, 405, 320, 307, 375, 321, 308, 324, 318]

        x_coords = []
        y_coords = []

        for landmark_idx in mouth_landmarks:
            if landmark_idx < len(face_landmarks.landmark):
                landmark = face_landmarks.landmark[landmark_idx]
                x_coords.append(landmark.x * frame_shape[1])
                y_coords.append(landmark.y * frame_shape[0])

        if x_coords and y_coords:
            return (int(np.mean(x_coords)), int(np.mean(y_coords)))

        # Fallback to center of face
        return (frame_shape[1] // 2, frame_shape[0] // 2)

    def _calculate_head_tilt_mediapipe(
        self, face_landmarks, frame_shape: tuple
    ) -> float:
        """Calculate head tilt using MediaPipe face landmarks."""
        # Use eye landmarks to determine tilt
        left_eye = face_landmarks.landmark[33]  # Left eye corner
        right_eye = face_landmarks.landmark[362]  # Right eye corner

        # Calculate angle between eyes
        eye_angle = np.arctan2(right_eye.y - left_eye.y, right_eye.x - left_eye.x)

        # Convert to degrees
        return np.degrees(eye_angle)

    def is_available(self) -> bool:
        """Check if MediaPipe detector is available."""
        return (
            self.mp_hands is not None
            and self.mp_face_mesh is not None
            and self.hands is not None
            and self.face_mesh is not None
        )

    def cleanup(self) -> None:
        """Clean up MediaPipe resources."""
        if self.hands:
            self.hands.close()
        if self.face_mesh:
            self.face_mesh.close()
