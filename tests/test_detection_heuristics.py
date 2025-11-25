"""Tests for heuristic detection."""

from unittest.mock import MagicMock, patch

import numpy as np

from app.core.detection.heuristics import AdvancedHeuristicDetector


class TestAdvancedHeuristicDetector:
    """Test advanced heuristic detector functionality."""

    def test_init(self):
        """Test detector initialization."""
        detector = AdvancedHeuristicDetector()

        assert detector.head_tilt_threshold == 25.0
        assert detector.hand_face_distance_threshold == 100.0
        assert detector.sip_duration_min == 0.8
        assert detector.sip_duration_max == 3.5
        assert detector.motion_threshold == 30.0
        assert detector.contour_min_area == 1000
        assert detector.contour_max_area == 50000

    def test_init_with_custom_params(self):
        """Test detector initialization with custom parameters."""
        detector = AdvancedHeuristicDetector(
            head_tilt_threshold=30.0,
            hand_face_distance_threshold=150.0,
            sip_duration_min=1.0,
            sip_duration_max=4.0,
            motion_threshold=40.0,
            contour_min_area=2000,
            contour_max_area=60000,
        )

        assert detector.head_tilt_threshold == 30.0
        assert detector.hand_face_distance_threshold == 150.0
        assert detector.sip_duration_min == 1.0
        assert detector.sip_duration_max == 4.0
        assert detector.motion_threshold == 40.0
        assert detector.contour_min_area == 2000
        assert detector.contour_max_area == 60000

    def test_is_available(self):
        """Test availability check."""
        detector = AdvancedHeuristicDetector()

        # Should be available if face cascade is loaded
        assert detector.is_available() is True

    @patch("cv2.CascadeClassifier")
    def test_is_available_false(self, mock_cascade):
        """Test availability check when cascade fails to load."""
        mock_cascade.return_value = None

        detector = AdvancedHeuristicDetector()
        assert detector.is_available() is False

    def test_detect_no_face(self):
        """Test detection when no face is detected."""
        detector = AdvancedHeuristicDetector()

        # Create a mock frame with no face
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Replace face_cascade with a mock
        mock_cascade = MagicMock()
        mock_cascade.detectMultiScale.return_value = []
        detector.face_cascade = mock_cascade

        result = detector.detect(frame)
        assert result is None

    def test_detect_no_hand(self):
        """Test detection when no hand is detected."""
        detector = AdvancedHeuristicDetector()

        # Create a mock frame with face but no hand
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Replace face_cascade with a mock
        mock_cascade = MagicMock()
        mock_cascade.detectMultiScale.return_value = [(100, 100, 200, 200)]
        detector.face_cascade = mock_cascade

        with patch.object(detector, "_detect_hand_advanced", return_value=None):
            result = detector.detect(frame)
            assert result is None

    def test_detect_hand_too_far(self):
        """Test detection when hand is too far from face."""
        detector = AdvancedHeuristicDetector()

        # Create a mock frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Replace face_cascade with a mock
        mock_cascade = MagicMock()
        mock_cascade.detectMultiScale.return_value = [(100, 100, 200, 200)]
        detector.face_cascade = mock_cascade

        with patch.object(
            detector, "_detect_hand_advanced", return_value=(500, 500)
        ):  # Far from face
            with patch.object(
                detector, "_detect_motion_in_face_region", return_value=False
            ):
                result = detector.detect(frame)
                assert result is None

    def test_detect_insufficient_tilt(self):
        """Test detection when head tilt is insufficient."""
        detector = AdvancedHeuristicDetector()

        # Create a mock frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Replace face_cascade with a mock
        mock_cascade = MagicMock()
        mock_cascade.detectMultiScale.return_value = [(100, 100, 200, 200)]
        detector.face_cascade = mock_cascade

        with patch.object(
            detector, "_detect_hand_advanced", return_value=(150, 150)
        ):  # Close to face
            with patch.object(
                detector, "_detect_motion_in_face_region", return_value=True
            ):
                with patch.object(
                    detector, "_calculate_head_tilt_advanced", return_value=10.0
                ):  # Low tilt
                    result = detector.detect(frame)
                    assert result is None

    def test_detect_no_motion(self):
        """Test detection when no motion is detected."""
        detector = AdvancedHeuristicDetector()

        # Create a mock frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Replace face_cascade with a mock
        mock_cascade = MagicMock()
        mock_cascade.detectMultiScale.return_value = [(100, 100, 200, 200)]
        detector.face_cascade = mock_cascade

        with patch.object(
            detector, "_detect_hand_advanced", return_value=(150, 150)
        ):  # Close to face
            with patch.object(
                detector, "_detect_motion_in_face_region", return_value=False
            ):  # No motion
                with patch.object(
                    detector, "_calculate_head_tilt_advanced", return_value=30.0
                ):  # Good tilt
                    result = detector.detect(frame)
                    assert result is None

    def test_detect_successful_sip(self):
        """Test successful sip detection."""
        detector = AdvancedHeuristicDetector()

        # Create a mock frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        mock_cascade = patch.object(detector, "face_cascade")
        with mock_cascade as mock_casc:
            mock_casc.detectMultiScale.return_value = [(100, 100, 200, 200)]
            with patch.object(
                detector, "_detect_hand_advanced", return_value=(150, 150)
            ):  # Close to face
                with patch.object(
                    detector, "_detect_motion_in_face_region", return_value=True
                ):  # Motion detected
                    with patch.object(
                        detector, "_calculate_head_tilt_advanced", return_value=30.0
                    ):  # Good tilt
                        with patch.object(
                            detector, "_calculate_confidence", return_value=0.8
                        ):
                            # Mock the sip duration check
                            detector.sip_start_time = 0
                            detector.sip_in_progress = True
                            detector.detection_frames = [
                                0,
                                1,
                                2,
                                3,
                                4,
                                5,
                                6,
                                7,
                                8,
                                9,
                            ]  # 10 frames

                            with patch(
                                "time.time", return_value=1.0
                            ):  # 1 second elapsed
                                result = detector.detect(frame)

                                assert result is not None
                                assert result.has_sip is True
                                assert result.confidence == 0.8
                                assert result.head_tilt_angle == 30.0
                                assert (
                                    result.hand_face_distance == 50.0
                                )  # Distance from (150,150) to (200,200)

    def test_detect_hand_by_skin_color(self):
        """Test hand detection by skin color."""
        detector = AdvancedHeuristicDetector()

        # Create a mock frame with skin-colored region
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        with patch("cv2.cvtColor") as mock_cvt:
            with patch("cv2.inRange") as mock_inrange:
                with patch("cv2.morphologyEx") as mock_morph:
                    with patch("cv2.findContours") as mock_contours:
                        with patch("cv2.contourArea") as mock_area:
                            with patch("cv2.boundingRect") as mock_rect:
                                # Mock the pipeline
                                mock_cvt.return_value = np.zeros(
                                    (480, 640, 3), dtype=np.uint8
                                )
                                mock_inrange.return_value = np.zeros(
                                    (480, 640), dtype=np.uint8
                                )
                                mock_morph.return_value = np.zeros(
                                    (480, 640), dtype=np.uint8
                                )
                                mock_contours.return_value = (
                                    [
                                        np.array(
                                            [
                                                [100, 100],
                                                [200, 100],
                                                [200, 200],
                                                [100, 200],
                                            ]
                                        )
                                    ],
                                    None,
                                )
                                mock_area.return_value = 2000  # Above minimum area
                                mock_rect.return_value = (100, 100, 100, 100)

                                result = detector._detect_hand_by_skin_color(frame)

                                assert result is not None
                                assert result == (150, 150)  # Center of bounding rect

    def test_detect_hand_by_contours(self):
        """Test hand detection by contours."""
        detector = AdvancedHeuristicDetector()

        # Create a mock frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        face = (100, 100, 200, 200)

        with patch("cv2.cvtColor") as mock_cvt:
            with patch("cv2.GaussianBlur") as mock_blur:
                with patch("cv2.Canny") as mock_canny:
                    with patch("cv2.findContours") as mock_contours:
                        with patch("cv2.contourArea") as mock_area:
                            with patch("cv2.boundingRect") as mock_rect:
                                # Mock the pipeline
                                mock_cvt.return_value = np.zeros(
                                    (480, 640), dtype=np.uint8
                                )
                                mock_blur.return_value = np.zeros(
                                    (480, 640), dtype=np.uint8
                                )
                                mock_canny.return_value = np.zeros(
                                    (480, 640), dtype=np.uint8
                                )
                                mock_contours.return_value = (
                                    [
                                        np.array(
                                            [
                                                [100, 100],
                                                [200, 100],
                                                [200, 200],
                                                [100, 200],
                                            ]
                                        )
                                    ],
                                    None,
                                )
                                mock_area.return_value = 2000  # Valid area
                                # boundingRect returns coordinates relative to ROI
                                # ROI starts at (50, 50) for face at (100, 100) with margin 50
                                # To get center at (150, 150) in full frame, we need:
                                # center = roi_x + x_cont + w_cont//2 = 50 + 50 + 50 = 150
                                mock_rect.return_value = (50, 50, 100, 100)

                                result = detector._detect_hand_by_contours(frame, face)

                                assert result is not None
                                assert result == (150, 150)  # Center of bounding rect

    def test_calculate_head_tilt_advanced(self):
        """Test advanced head tilt calculation."""
        detector = AdvancedHeuristicDetector()

        # Create mock face and gray frame
        face = (100, 100, 200, 200)
        gray = np.zeros((480, 640), dtype=np.uint8)

        with patch("cv2.Canny") as mock_canny:
            with patch("cv2.HoughLines") as mock_hough:
                # Mock Hough line detection
                mock_canny.return_value = np.zeros((480, 640), dtype=np.uint8)
                mock_hough.return_value = np.array(
                    [[[100, np.pi / 4]], [[200, np.pi / 6]]]
                )  # Some lines

                result = detector._calculate_head_tilt_advanced(face, gray)

                assert result is not None
                assert isinstance(result, float)

    def test_detect_motion_in_face_region(self):
        """Test motion detection in face region."""
        detector = AdvancedHeuristicDetector()

        # Create mock gray frame and face
        gray = np.zeros((480, 640), dtype=np.uint8)
        face = (100, 100, 200, 200)

        # Set up previous frame
        detector.prev_gray = np.zeros((480, 640), dtype=np.uint8)

        with patch("cv2.absdiff") as mock_absdiff:
            with patch("cv2.threshold") as mock_threshold:
                # Mock motion detection
                mock_absdiff.return_value = np.zeros((200, 200), dtype=np.uint8)
                mock_threshold.return_value = (
                    None,
                    np.zeros((200, 200), dtype=np.uint8),
                )

                result = detector._detect_motion_in_face_region(gray, face)

                assert result is False  # No motion detected

    def test_calculate_confidence(self):
        """Test confidence calculation."""
        detector = AdvancedHeuristicDetector()

        # Test with good parameters
        confidence = detector._calculate_confidence(
            hand_face_distance=50.0,
            head_tilt_angle=30.0,
            motion_detected=True,
            sip_duration=2.0,
        )

        assert 0.0 <= confidence <= 1.0
        assert confidence > 0.5  # Should be high with good parameters

        # Test with poor parameters
        confidence_poor = detector._calculate_confidence(
            hand_face_distance=150.0,
            head_tilt_angle=10.0,
            motion_detected=False,
            sip_duration=0.5,
        )

        assert 0.0 <= confidence_poor <= 1.0
        assert confidence_poor < confidence  # Should be lower than good parameters

    def test_cleanup(self):
        """Test cleanup method."""
        detector = AdvancedHeuristicDetector()

        # Set some state
        detector.detection_frames = [1, 2, 3]
        detector.sip_in_progress = True

        # Cleanup
        detector.cleanup()

        assert detector.detection_frames == []
        assert detector.sip_in_progress is False
