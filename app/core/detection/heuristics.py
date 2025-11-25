"""Heuristic-based detection implementation."""

import cv2
import numpy as np

from app.core.detection.base import HeuristicDetector
from app.core.models import DetectionResult


class AdvancedHeuristicDetector(HeuristicDetector):
    """Advanced heuristic detector with improved algorithms."""

    def __init__(self, **kwargs):
        """Initialize advanced heuristic detector."""
        super().__init__(**kwargs)

        # Additional parameters
        self.motion_threshold = kwargs.get("motion_threshold", 30.0)
        self.contour_min_area = kwargs.get("contour_min_area", 1000)
        self.contour_max_area = kwargs.get("contour_max_area", 50000)

        # Motion detection
        self.prev_gray = None
        self.flow_threshold = 10.0

        # Optical flow parameters
        self.lk_params = {
            "winSize": (15, 15),
            "maxLevel": 2,
            "criteria": (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
        }

    def detect(self, frame: np.ndarray) -> DetectionResult | None:
        """Advanced sip detection with multiple heuristics."""
        import time

        current_time = time.time()

        # Check cooldown
        if current_time - self.last_detection_time < 1.0:
            return None

        # Convert to grayscale for motion detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect face
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces) == 0:
            return None

        # Use largest face
        face = max(faces, key=lambda x: x[2] * x[3])
        x, y, w, h = face
        face_center = (x + w // 2, y + h // 2)

        # Detect hand using multiple methods
        hand_center = self._detect_hand_advanced(frame, face)

        if hand_center is None:
            return None

        # Calculate head tilt with improved method
        head_tilt_angle = self._calculate_head_tilt_advanced(face, gray)

        # Calculate hand-face distance
        hand_face_distance = np.sqrt(
            (hand_center[0] - face_center[0]) ** 2
            + (hand_center[1] - face_center[1]) ** 2
        )

        # Detect motion in face region
        motion_detected = self._detect_motion_in_face_region(gray, face)

        # Check sip conditions
        has_sip = (
            hand_face_distance < self.hand_face_distance_threshold
            and abs(head_tilt_angle) > self.head_tilt_threshold
            and motion_detected
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

                # Calculate confidence based on multiple factors
                confidence = self._calculate_confidence(
                    hand_face_distance, head_tilt_angle, motion_detected, sip_duration
                )

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
                        "motion_detected": motion_detected,
                    },
                )

        # Reset if sip duration exceeds maximum
        if self.sip_in_progress:
            sip_duration = current_time - self.sip_start_time
            if sip_duration > self.sip_duration_max:
                self.sip_in_progress = False
                self.detection_frames = []

        # Update previous frame for motion detection
        self.prev_gray = gray.copy()

        return None

    def _detect_hand_advanced(
        self, frame: np.ndarray, face: tuple[int, int, int, int]
    ) -> tuple[int, int] | None:
        """Advanced hand detection using multiple methods."""
        x, y, w, h = face

        # Method 1: Skin color detection
        hand_center_skin = self._detect_hand_by_skin_color(frame)

        # Method 2: Contour detection in face region
        hand_center_contour = self._detect_hand_by_contours(frame, face)

        # Method 3: Edge detection
        hand_center_edge = self._detect_hand_by_edges(frame, face)

        # Combine results (prefer skin color detection)
        if hand_center_skin:
            return hand_center_skin
        elif hand_center_contour:
            return hand_center_contour
        elif hand_center_edge:
            return hand_center_edge

        return None

    def _detect_hand_by_contours(
        self, frame: np.ndarray, face: tuple[int, int, int, int]
    ) -> tuple[int, int] | None:
        """Detect hand using contour analysis."""
        x, y, w, h = face

        # Focus on the area around the face
        margin = 50
        roi_x = max(0, x - margin)
        roi_y = max(0, y - margin)
        roi_w = min(frame.shape[1] - roi_x, w + 2 * margin)
        roi_h = min(frame.shape[0] - roi_y, h + 2 * margin)

        roi = frame[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]

        # Convert to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray_roi, (5, 5), 0)

        # Apply Canny edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours
        contours, _ = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return None

        # Filter contours by area and aspect ratio
        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if self.contour_min_area < area < self.contour_max_area:
                # Check aspect ratio (hands are typically wider than tall)
                x_cont, y_cont, w_cont, h_cont = cv2.boundingRect(contour)
                aspect_ratio = w_cont / h_cont
                if 0.5 < aspect_ratio < 3.0:  # Reasonable hand aspect ratio
                    valid_contours.append(contour)

        if not valid_contours:
            return None

        # Get the largest valid contour
        largest_contour = max(valid_contours, key=cv2.contourArea)
        x_cont, y_cont, w_cont, h_cont = cv2.boundingRect(largest_contour)

        # Convert back to full frame coordinates
        center_x = roi_x + x_cont + w_cont // 2
        center_y = roi_y + y_cont + h_cont // 2

        return (center_x, center_y)

    def _detect_hand_by_edges(
        self, frame: np.ndarray, face: tuple[int, int, int, int]
    ) -> tuple[int, int] | None:
        """Detect hand using edge detection."""
        x, y, w, h = face

        # Focus on the area around the face
        margin = 100
        roi_x = max(0, x - margin)
        roi_y = max(0, y - margin)
        roi_w = min(frame.shape[1] - roi_x, w + 2 * margin)
        roi_h = min(frame.shape[0] - roi_y, h + 2 * margin)

        roi = frame[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]

        # Convert to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Apply bilateral filter to reduce noise
        filtered = cv2.bilateralFilter(gray_roi, 9, 75, 75)

        # Apply adaptive threshold
        thresh = cv2.adaptiveThreshold(
            filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Find contours
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return None

        # Find contours that could be hands
        hand_candidates = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Minimum area
                # Check if contour is roughly hand-shaped
                hull = cv2.convexHull(contour)
                hull_area = cv2.contourArea(hull)
                if hull_area > 0:
                    solidity = area / hull_area
                    if 0.7 < solidity < 0.95:  # Hand-like solidity
                        hand_candidates.append(contour)

        if not hand_candidates:
            return None

        # Get the largest candidate
        largest_contour = max(hand_candidates, key=cv2.contourArea)
        x_cont, y_cont, w_cont, h_cont = cv2.boundingRect(largest_contour)

        # Convert back to full frame coordinates
        center_x = roi_x + x_cont + w_cont // 2
        center_y = roi_y + y_cont + h_cont // 2

        return (center_x, center_y)

    def _calculate_head_tilt_advanced(
        self, face: tuple[int, int, int, int], gray: np.ndarray
    ) -> float:
        """Calculate head tilt using advanced methods."""
        x, y, w, h = face

        # Extract face region
        face_roi = gray[y : y + h, x : x + w]

        # Apply Hough line detection
        edges = cv2.Canny(face_roi, 50, 150)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=50)

        if lines is not None and len(lines) > 0:
            # Calculate average angle of detected lines
            angles = []
            for line in lines:
                rho, theta = line[0]
                angle = np.degrees(theta)
                # Normalize angle to -90 to 90 degrees
                if angle > 90:
                    angle -= 180
                angles.append(angle)

            if angles:
                avg_angle = np.mean(angles)
                return avg_angle

        # Fallback to simple method
        return self._calculate_head_tilt(face)

    def _detect_motion_in_face_region(
        self, gray: np.ndarray, face: tuple[int, int, int, int]
    ) -> bool:
        """Detect motion in the face region."""
        if self.prev_gray is None:
            return False

        x, y, w, h = face

        # Extract face region from current and previous frames
        face_roi = gray[y : y + h, x : x + w]
        prev_face_roi = self.prev_gray[y : y + h, x : x + w]

        # Calculate absolute difference
        diff = cv2.absdiff(face_roi, prev_face_roi)

        # Apply threshold
        _, thresh = cv2.threshold(diff, self.motion_threshold, 255, cv2.THRESH_BINARY)

        # Calculate motion percentage
        motion_pixels = np.sum(thresh > 0)
        total_pixels = thresh.size
        motion_percentage = motion_pixels / total_pixels

        # Return True if motion is significant
        return motion_percentage > 0.01  # 1% of face region moving

    def _calculate_confidence(
        self,
        hand_face_distance: float,
        head_tilt_angle: float,
        motion_detected: bool,
        sip_duration: float,
    ) -> float:
        """Calculate detection confidence based on multiple factors."""
        confidence = 0.0

        # Distance factor (closer is better)
        distance_factor = max(
            0, 1.0 - (hand_face_distance / self.hand_face_distance_threshold)
        )
        confidence += distance_factor * 0.3

        # Tilt factor (more tilt is better)
        tilt_factor = min(1.0, abs(head_tilt_angle) / self.head_tilt_threshold)
        confidence += tilt_factor * 0.3

        # Motion factor
        if motion_detected:
            confidence += 0.2

        # Duration factor (optimal duration is better)
        duration_factor = (
            1.0 - abs(sip_duration - 2.0) / 2.0
        )  # Optimal around 2 seconds
        duration_factor = max(0, duration_factor)
        confidence += duration_factor * 0.2

        return min(1.0, confidence)
