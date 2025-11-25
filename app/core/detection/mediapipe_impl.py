"""MediaPipe-based detection implementation."""

from typing import Optional

import cv2
import numpy as np

from app.core.detection.base import MediaPipeDetector
from app.core.models import DetectionResult


class AdvancedMediaPipeDetector(MediaPipeDetector):
    """Advanced MediaPipe detector with improved accuracy."""
    
    def __init__(self, **kwargs):
        """Initialize advanced MediaPipe detector."""
        super().__init__(**kwargs)
        
        # Additional parameters
        self.mouth_landmarks = [
            61, 84, 17, 314, 405, 320, 307, 375, 321, 308, 324, 318
        ]
        self.eye_landmarks = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        
        # Hand tracking parameters
        self.hand_confidence_threshold = kwargs.get('hand_confidence_threshold', 0.7)
        self.face_confidence_threshold = kwargs.get('face_confidence_threshold', 0.7)
        
        # Sip detection state
        self.sip_start_time = 0.0
        self.sip_in_progress = False
        self.last_detection_time = 0.0
        self.detection_frames = []
    
    def detect(self, frame: np.ndarray) -> Optional[DetectionResult]:
        """Advanced sip detection using MediaPipe."""
        import time
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_detection_time < 1.0:
            return None
        
        if not self.is_available():
            return None
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process hands
        hand_results = self.hands.process(rgb_frame)
        
        # Process face
        face_results = self.face_mesh.process(rgb_frame)
        
        if not hand_results.multi_hand_landmarks or not face_results.multi_face_landmarks:
            return None
        
        # Get hand landmarks
        hand_landmarks = hand_results.multi_hand_landmarks[0]
        hand_confidence = hand_results.multi_handedness[0].classification[0].score
        
        # Get face landmarks
        face_landmarks = face_results.multi_face_landmarks[0]
        
        # Check confidence thresholds
        if hand_confidence < self.hand_confidence_threshold:
            return None
        
        # Get key points
        wrist_pos = self._get_wrist_position(hand_landmarks, frame.shape)
        mouth_center = self._get_mouth_center_advanced(face_landmarks, frame.shape)
        head_tilt = self._calculate_head_tilt_advanced(face_landmarks, frame.shape)
        
        if wrist_pos is None or mouth_center is None:
            return None
        
        # Calculate distance between wrist and mouth
        distance = np.sqrt(
            (wrist_pos[0] - mouth_center[0]) ** 2 + 
            (wrist_pos[1] - mouth_center[1]) ** 2
        )
        
        # Check if hand is near mouth and head is tilted
        has_sip = (
            distance < self.config.get('hand_face_distance_threshold', 100.0) and
            abs(head_tilt) > self.config.get('head_tilt_threshold', 25.0)
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
            if sip_duration >= self.config.get('sip_duration_min', 0.8):
                # Complete the sip detection
                self.sip_in_progress = False
                self.last_detection_time = current_time
                self.detection_frames = []
                
                # Calculate confidence based on multiple factors
                confidence = self._calculate_confidence(
                    distance, head_tilt, hand_confidence, sip_duration
                )
                
                return DetectionResult(
                    has_sip=True,
                    confidence=confidence,
                    head_tilt_angle=head_tilt,
                    hand_face_distance=distance,
                    face_center=mouth_center,
                    hand_center=wrist_pos,
                    detection_data={
                        'sip_duration': sip_duration,
                        'detection_frames': len(self.detection_frames),
                        'hand_confidence': hand_confidence
                    }
                )
        
        # Reset if sip duration exceeds maximum
        if self.sip_in_progress:
            sip_duration = current_time - self.sip_start_time
            if sip_duration > self.config.get('sip_duration_max', 3.5):
                self.sip_in_progress = False
                self.detection_frames = []
        
        return None
    
    def _get_wrist_position(self, hand_landmarks, frame_shape: tuple) -> Optional[tuple[int, int]]:
        """Get wrist position from hand landmarks."""
        try:
            wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
            x = int(wrist.x * frame_shape[1])
            y = int(wrist.y * frame_shape[0])
            return (x, y)
        except (IndexError, AttributeError):
            return None
    
    def _get_mouth_center_advanced(self, face_landmarks, frame_shape: tuple) -> Optional[tuple[int, int]]:
        """Get mouth center using advanced landmark analysis."""
        try:
            x_coords = []
            y_coords = []
            
            for landmark_idx in self.mouth_landmarks:
                if landmark_idx < len(face_landmarks.landmark):
                    landmark = face_landmarks.landmark[landmark_idx]
                    x_coords.append(landmark.x * frame_shape[1])
                    y_coords.append(landmark.y * frame_shape[0])
            
            if x_coords and y_coords:
                return (int(np.mean(x_coords)), int(np.mean(y_coords)))
            
            return None
        except (IndexError, AttributeError):
            return None
    
    def _calculate_head_tilt_advanced(self, face_landmarks, frame_shape: tuple) -> float:
        """Calculate head tilt using advanced landmark analysis."""
        try:
            # Use multiple eye landmarks for better accuracy
            left_eye_points = []
            right_eye_points = []
            
            # Left eye landmarks
            left_eye_indices = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161]
            for idx in left_eye_indices:
                if idx < len(face_landmarks.landmark):
                    landmark = face_landmarks.landmark[idx]
                    left_eye_points.append((landmark.x, landmark.y))
            
            # Right eye landmarks
            right_eye_indices = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
            for idx in right_eye_indices:
                if idx < len(face_landmarks.landmark):
                    landmark = face_landmarks.landmark[idx]
                    right_eye_points.append((landmark.x, landmark.y))
            
            if len(left_eye_points) >= 3 and len(right_eye_points) >= 3:
                # Calculate center of each eye
                left_eye_center = np.mean(left_eye_points, axis=0)
                right_eye_center = np.mean(right_eye_points, axis=0)
                
                # Calculate angle between eyes
                eye_angle = np.arctan2(
                    right_eye_center[1] - left_eye_center[1],
                    right_eye_center[0] - left_eye_center[0]
                )
                
                # Convert to degrees
                return np.degrees(eye_angle)
            
            # Fallback to simple method
            return self._calculate_head_tilt_mediapipe(face_landmarks, frame_shape)
            
        except (IndexError, AttributeError):
            return 0.0
    
    def _calculate_confidence(
        self, 
        distance: float, 
        head_tilt: float, 
        hand_confidence: float, 
        sip_duration: float
    ) -> float:
        """Calculate detection confidence based on multiple factors."""
        confidence = 0.0
        
        # Distance factor (closer is better)
        max_distance = self.config.get('hand_face_distance_threshold', 100.0)
        distance_factor = max(0, 1.0 - (distance / max_distance))
        confidence += distance_factor * 0.3
        
        # Tilt factor (more tilt is better)
        min_tilt = self.config.get('head_tilt_threshold', 25.0)
        tilt_factor = min(1.0, abs(head_tilt) / min_tilt)
        confidence += tilt_factor * 0.2
        
        # Hand confidence factor
        confidence += hand_confidence * 0.3
        
        # Duration factor (optimal duration is better)
        optimal_duration = 2.0
        duration_factor = 1.0 - abs(sip_duration - optimal_duration) / optimal_duration
        duration_factor = max(0, duration_factor)
        confidence += duration_factor * 0.2
        
        return min(1.0, confidence)
    
    def _detect_hand_gesture(self, hand_landmarks) -> str:
        """Detect hand gesture (simplified)."""
        try:
            # Get key finger landmarks
            thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
            
            # Get finger MCP joints
            thumb_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP]
            index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
            middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
            ring_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP]
            pinky_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP]
            
            # Check if fingers are extended
            fingers_extended = []
            
            # Thumb (different logic)
            if thumb_tip.x > thumb_mcp.x:
                fingers_extended.append(1)
            else:
                fingers_extended.append(0)
            
            # Other fingers
            for tip, mcp in [(index_tip, index_mcp), (middle_tip, middle_mcp), 
                           (ring_tip, ring_mcp), (pinky_tip, pinky_mcp)]:
                if tip.y < mcp.y:
                    fingers_extended.append(1)
                else:
                    fingers_extended.append(0)
            
            # Determine gesture
            extended_count = sum(fingers_extended)
            
            if extended_count == 0:
                return "fist"
            elif extended_count == 1 and fingers_extended[1] == 1:  # Only index finger
                return "pointing"
            elif extended_count == 2 and fingers_extended[1] == 1 and fingers_extended[2] == 1:  # Index and middle
                return "peace"
            elif extended_count == 5:
                return "open_hand"
            else:
                return "partial"
                
        except (IndexError, AttributeError):
            return "unknown"
    
    def cleanup(self) -> None:
        """Clean up MediaPipe resources."""
        super().cleanup()
        self.detection_frames = []
