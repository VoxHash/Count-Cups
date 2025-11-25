"""Live camera screen for Count-Cups."""

from typing import Optional

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap

from app.core.db import Database
from app.core.logging import get_logger

logger = get_logger(__name__)


class LiveCameraScreen(QWidget):
    """Live camera screen for real-time sip detection."""
    
    # Signals
    camera_status_changed = pyqtSignal(str)
    sip_detected = pyqtSignal(float)
    
    def __init__(self, database: Optional[Database], parent=None):
        """Initialize live camera screen.
        
        Args:
            database: Database instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.database = database
        self.parent_window = parent
        
        self._init_ui()
        self._init_camera()
    
    def _init_ui(self) -> None:
        """Initialize UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Live Camera")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        # Camera view
        self.camera_label = QLabel("Camera not available")
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_label.setMinimumSize(640, 480)
        self.camera_label.setStyleSheet("border: 2px solid #ccc; background-color: #f0f0f0;")
        layout.addWidget(self.camera_label)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("Start Detection")
        self.start_btn.clicked.connect(self._start_detection)
        controls_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Stop Detection")
        self.stop_btn.clicked.connect(self._stop_detection)
        self.stop_btn.setEnabled(False)
        controls_layout.addWidget(self.stop_btn)
        
        self.calibrate_btn = QPushButton("Calibrate")
        self.calibrate_btn.clicked.connect(self._calibrate)
        controls_layout.addWidget(self.calibrate_btn)
        
        layout.addLayout(controls_layout)
        
        # Status
        self.status_label = QLabel("Ready to start detection")
        self.status_label.setProperty("class", "secondary")
        layout.addWidget(self.status_label)
        
        # Detection info
        self.detection_info = QLabel("No detection data")
        self.detection_info.setProperty("class", "secondary")
        layout.addWidget(self.detection_info)
    
    def _init_camera(self) -> None:
        """Initialize camera."""
        self.cap = None
        try:
            import cv2
            
            # Try to find an available camera
            camera_index = None
            max_cameras = 5  # Check up to 5 cameras
            
            for i in range(max_cameras):
                try:
                    cap = cv2.VideoCapture(i)
                    if cap.isOpened():
                        # Test if we can read a frame
                        ret, frame = cap.read()
                        if ret and frame is not None:
                            camera_index = i
                            cap.release()
                            break
                    cap.release()
                except Exception:
                    # Skip this camera index if there's an error
                    continue
            
            if camera_index is not None:
                # Initialize with the found camera index
                self.cap = cv2.VideoCapture(camera_index)
                if self.cap.isOpened():
                    self.camera_status_changed.emit("Connected")
                    self.status_label.setText(f"Camera connected (index {camera_index})")
                else:
                    self.camera_status_changed.emit("Not Connected")
                    self.status_label.setText("Camera initialization failed")
                    self.cap.release()
                    self.cap = None
            else:
                # No cameras found
                self.camera_status_changed.emit("Not Available")
                self.status_label.setText("No cameras detected - using demo mode")
                self.camera_label.setText("No Camera Available\n\nDemo Mode:\n• Click 'Start Detection' to simulate\n• Manual sip/cup buttons work\n• All other features available")
                self.camera_label.setStyleSheet("border: 2px solid #666; background-color: #2a2a2a; color: #ccc; font-size: 14px; padding: 20px;")
                
        except ImportError:
            self.camera_status_changed.emit("Not Available")
            self.status_label.setText("OpenCV not available")
        except Exception as e:
            self.camera_status_changed.emit("Error")
            self.status_label.setText(f"Camera error: {e}")
            if self.cap:
                self.cap.release()
                self.cap = None
    
    def cleanup_camera(self) -> None:
        """Clean up camera resources."""
        if self.cap:
            self.cap.release()
            self.cap = None
            logger.info("Camera released")
    
    def closeEvent(self, event) -> None:
        """Handle close event."""
        self.cleanup_camera()
        super().closeEvent(event)
    
    def _start_detection(self) -> None:
        """Start sip detection."""
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        if self.cap and self.cap.isOpened():
            self.status_label.setText("Detection started")
            # Start camera timer
            self.timer = QTimer()
            self.timer.timeout.connect(self._update_frame)
            self.timer.start(33)  # ~30 FPS
        else:
            # Demo mode - simulate detection
            self.status_label.setText("Demo mode - simulating detection")
            self.timer = QTimer()
            self.timer.timeout.connect(self._simulate_detection)
            self.timer.start(1000)  # Simulate every second
    
    def _stop_detection(self) -> None:
        """Stop sip detection."""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Detection stopped")
        
        if hasattr(self, 'timer'):
            self.timer.stop()
    
    def _update_frame(self) -> None:
        """Update camera frame."""
        if not self.cap or not self.cap.isOpened():
            return
            
        try:
            import cv2
            ret, frame = self.cap.read()
            if ret and frame is not None:
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to QImage
                h, w, ch = rgb_frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                
                # Scale to fit label
                pixmap = QPixmap.fromImage(qt_image)
                scaled_pixmap = pixmap.scaled(
                    self.camera_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                
                self.camera_label.setPixmap(scaled_pixmap)
                
                # Simulate sip detection (placeholder)
                self._simulate_detection()
            else:
                # Camera disconnected, try to reconnect
                self._reconnect_camera()
        except Exception as e:
            logger.warning(f"Camera frame error: {e}")
            # Try to reconnect on error
            self._reconnect_camera()
    
    def _reconnect_camera(self) -> None:
        """Try to reconnect camera."""
        if hasattr(self, 'timer'):
            self.timer.stop()
        
        self.cleanup_camera()
        self._init_camera()
        
        if self.cap and self.cap.isOpened():
            if hasattr(self, 'timer'):
                self.timer.start(33)
            self.status_label.setText("Camera reconnected")
        else:
            self.status_label.setText("Camera reconnection failed")
    
    def _simulate_detection(self) -> None:
        """Simulate sip detection (placeholder)."""
        import random
        if random.random() < 0.01:  # 1% chance per frame
            ml_amount = random.uniform(15, 25)
            self.sip_detected.emit(ml_amount)
            self.detection_info.setText(f"Last sip: {ml_amount:.1f}ml")
    
    def _calibrate(self) -> None:
        """Open calibration dialog."""
        # This would open calibration dialog in a real implementation
        self.status_label.setText("Calibration not yet implemented")
    
    def cleanup(self) -> None:
        """Clean up resources."""
        if hasattr(self, 'timer'):
            self.timer.stop()
        
        if hasattr(self, 'cap') and self.cap is not None:
            self.cap.release()
