"""Settings screen for Count-Cups."""

from typing import Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QSpinBox, QLineEdit, QComboBox, QGroupBox, QFormLayout,
    QCheckBox, QSlider, QMessageBox, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal

from app.core.db import Database
from app.core.logging import get_logger

logger = get_logger(__name__)


class SettingsScreen(QWidget):
    """Settings screen for application configuration."""
    
    # Signals
    detection_engine_changed = pyqtSignal(str)
    theme_changed = pyqtSignal(str)
    
    def __init__(self, database: Optional[Database], parent=None):
        """Initialize settings screen.
        
        Args:
            database: Database instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.database = database
        self.parent_window = parent
        
        self._init_ui()
        self._load_settings()
    
    def _init_ui(self) -> None:
        """Initialize UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Settings")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # General Settings Tab
        self._create_general_tab()
        
        # Detection Settings Tab
        self._create_detection_tab()
        
        # Camera Settings Tab
        self._create_camera_tab()
        
        # Notifications Tab
        self._create_notifications_tab()
        
        # Advanced Tab
        self._create_advanced_tab()
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.clicked.connect(self._save_settings)
        self.save_btn.setProperty("class", "success")
        buttons_layout.addWidget(self.save_btn)
        
        self.reset_btn = QPushButton("Reset to Defaults")
        self.reset_btn.clicked.connect(self._reset_defaults)
        self.reset_btn.setProperty("class", "warning")
        buttons_layout.addWidget(self.reset_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
    
    def _create_general_tab(self) -> None:
        """Create general settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        
        # Theme Settings
        theme_group = QGroupBox("Appearance")
        theme_layout = QFormLayout(theme_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Auto", "Light", "Dark", "Dracula"])
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        theme_layout.addRow("Theme:", self.theme_combo)
        
        self.high_contrast = QCheckBox()
        self.high_contrast.setToolTip("Enable high contrast mode for better visibility")
        theme_layout.addRow("High Contrast:", self.high_contrast)
        
        layout.addWidget(theme_group)
        
        # Window Settings
        window_group = QGroupBox("Window")
        window_layout = QFormLayout(window_group)
        
        self.start_maximized = QCheckBox()
        self.start_maximized.setToolTip("Start application maximized")
        window_layout.addRow("Start Maximized:", self.start_maximized)
        
        self.minimize_to_tray = QCheckBox()
        self.minimize_to_tray.setChecked(True)
        self.minimize_to_tray.setToolTip("Minimize to system tray instead of taskbar")
        window_layout.addRow("Minimize to Tray:", self.minimize_to_tray)
        
        layout.addWidget(window_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "General")
    
    def _create_detection_tab(self) -> None:
        """Create detection settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        
        # Detection Engine
        engine_group = QGroupBox("Detection Engine")
        engine_layout = QFormLayout(engine_group)
        
        self.detection_engine = QComboBox()
        self.detection_engine.addItems(["Heuristics", "MediaPipe"])
        self.detection_engine.currentTextChanged.connect(self._on_detection_engine_changed)
        engine_layout.addRow("Engine:", self.detection_engine)
        
        engine_info = QLabel(
            "Heuristics: Fast, works without additional dependencies\n"
            "MediaPipe: More accurate, requires MediaPipe installation"
        )
        engine_info.setProperty("class", "secondary")
        engine_info.setWordWrap(True)
        engine_layout.addRow("", engine_info)
        
        layout.addWidget(engine_group)
        
        # Detection Parameters
        params_group = QGroupBox("Detection Parameters")
        params_layout = QFormLayout(params_group)
        
        self.head_tilt_threshold = QSpinBox()
        self.head_tilt_threshold.setRange(10, 60)
        self.head_tilt_threshold.setValue(25)
        self.head_tilt_threshold.setSuffix("°")
        params_layout.addRow("Head Tilt Threshold:", self.head_tilt_threshold)
        
        self.hand_distance_threshold = QSpinBox()
        self.hand_distance_threshold.setRange(50, 200)
        self.hand_distance_threshold.setValue(100)
        self.hand_distance_threshold.setSuffix(" px")
        params_layout.addRow("Hand-Face Distance:", self.hand_distance_threshold)
        
        self.confidence_threshold = QSlider(Qt.Orientation.Horizontal)
        self.confidence_threshold.setRange(10, 100)
        self.confidence_threshold.setValue(50)
        self.confidence_threshold.valueChanged.connect(self._update_confidence_label)
        params_layout.addRow("Confidence Threshold:", self.confidence_threshold)
        
        self.confidence_label = QLabel("50%")
        self.confidence_label.setProperty("class", "secondary")
        params_layout.addRow("", self.confidence_label)
        
        layout.addWidget(params_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "Detection")
    
    def _create_camera_tab(self) -> None:
        """Create camera settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        
        # Camera Selection
        camera_group = QGroupBox("Camera")
        camera_layout = QFormLayout(camera_group)
        
        # Camera selection
        self.camera_combo = QComboBox()
        self._populate_camera_list()
        self.camera_combo.currentTextChanged.connect(self._on_camera_selected)
        camera_layout.addRow("Camera:", self.camera_combo)
        
        self.camera_index = QSpinBox()
        self.camera_index.setRange(0, 10)
        self.camera_index.setValue(0)
        self.camera_index.setToolTip("Camera index (0 for default camera)")
        self.camera_index.valueChanged.connect(self._on_camera_index_changed)
        camera_layout.addRow("Camera Index:", self.camera_index)
        
        self.camera_width = QSpinBox()
        self.camera_width.setRange(320, 1920)
        self.camera_width.setValue(640)
        self.camera_width.setSuffix(" px")
        camera_layout.addRow("Width:", self.camera_width)
        
        self.camera_height = QSpinBox()
        self.camera_height.setRange(240, 1080)
        self.camera_height.setValue(480)
        self.camera_height.setSuffix(" px")
        camera_layout.addRow("Height:", self.camera_height)
        
        self.camera_fps = QSpinBox()
        self.camera_fps.setRange(15, 60)
        self.camera_fps.setValue(30)
        self.camera_fps.setSuffix(" fps")
        camera_layout.addRow("Frame Rate:", self.camera_fps)
        
        layout.addWidget(camera_group)
        
        # Camera Test
        test_group = QGroupBox("Camera Test")
        test_layout = QVBoxLayout(test_group)
        
        test_info = QLabel("Test your camera settings to ensure proper detection.")
        test_info.setProperty("class", "secondary")
        test_layout.addWidget(test_info)
        
        self.test_camera_btn = QPushButton("Test Camera")
        self.test_camera_btn.clicked.connect(self._test_camera)
        test_layout.addWidget(self.test_camera_btn)
        
        layout.addWidget(test_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "Camera")
    
    def _create_notifications_tab(self) -> None:
        """Create notifications settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        
        # Notification Settings
        notif_group = QGroupBox("Notifications")
        notif_layout = QFormLayout(notif_group)
        
        self.enable_notifications = QCheckBox()
        self.enable_notifications.setChecked(True)
        notif_layout.addRow("Enable Notifications:", self.enable_notifications)
        
        self.goal_reminder = QCheckBox()
        self.goal_reminder.setChecked(True)
        notif_layout.addRow("Goal Reminder:", self.goal_reminder)
        
        self.reminder_hour = QSpinBox()
        self.reminder_hour.setRange(0, 23)
        self.reminder_hour.setValue(20)
        notif_layout.addRow("Reminder Hour:", self.reminder_hour)
        
        self.reminder_minute = QSpinBox()
        self.reminder_minute.setRange(0, 59)
        self.reminder_minute.setValue(0)
        notif_layout.addRow("Reminder Minute:", self.reminder_minute)
        
        layout.addWidget(notif_group)
        
        # Test Notifications
        test_group = QGroupBox("Test Notifications")
        test_layout = QVBoxLayout(test_group)
        
        self.test_notification_btn = QPushButton("Test Notification")
        self.test_notification_btn.clicked.connect(self._test_notification)
        test_layout.addWidget(self.test_notification_btn)
        
        layout.addWidget(test_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "Notifications")
    
    def _create_advanced_tab(self) -> None:
        """Create advanced settings tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        
        # Database Settings
        db_group = QGroupBox("Database")
        db_layout = QFormLayout(db_group)
        
        self.db_path = QLineEdit()
        self.db_path.setReadOnly(True)
        self.db_path.setToolTip("Path to the database file")
        db_layout.addRow("Database Path:", self.db_path)
        
        self.export_data_btn = QPushButton("Export Data")
        self.export_data_btn.clicked.connect(self._export_data)
        db_layout.addRow("", self.export_data_btn)
        
        self.import_data_btn = QPushButton("Import Data")
        self.import_data_btn.clicked.connect(self._import_data)
        db_layout.addRow("", self.import_data_btn)
        
        layout.addWidget(db_group)
        
        # Logging Settings
        log_group = QGroupBox("Logging")
        log_layout = QFormLayout(log_group)
        
        self.log_level = QComboBox()
        self.log_level.addItems(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        log_layout.addRow("Log Level:", self.log_level)
        
        self.enable_telemetry = QCheckBox()
        self.enable_telemetry.setToolTip("Help improve the app by sending anonymous usage data")
        log_layout.addRow("Enable Telemetry:", self.enable_telemetry)
        
        layout.addWidget(log_group)
        
        # Reset Settings
        reset_group = QGroupBox("Reset")
        reset_layout = QVBoxLayout(reset_group)
        
        reset_info = QLabel(
            "Reset all settings to their default values. This will not affect your data."
        )
        reset_info.setProperty("class", "secondary")
        reset_info.setWordWrap(True)
        reset_layout.addWidget(reset_info)
        
        self.reset_all_btn = QPushButton("Reset All Settings")
        self.reset_all_btn.clicked.connect(self._reset_all_settings)
        self.reset_all_btn.setProperty("class", "error")
        reset_layout.addWidget(self.reset_all_btn)
        
        layout.addWidget(reset_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab, "Advanced")
    
    def _load_settings(self) -> None:
        """Load settings from database."""
        if not self.database:
            return
        
        try:
            settings = self.database.get_user_settings()
            
            # General settings
            self.theme_combo.setCurrentText(settings.theme.title())
            self.start_maximized.setChecked(settings.window_maximized)
            
            # Detection settings
            self.detection_engine.setCurrentText(settings.detection_engine.title())
            
            # Camera settings
            self.camera_index.setValue(settings.camera_index)
            self.camera_width.setValue(settings.camera_width)
            self.camera_height.setValue(settings.camera_height)
            self.camera_fps.setValue(settings.camera_fps)
            
            # Notification settings
            self.enable_notifications.setChecked(settings.enable_notifications)
            self.reminder_hour.setValue(settings.goal_reminder_hour)
            self.reminder_minute.setValue(settings.goal_reminder_minute)
            
            # Database path
            from app.core.config import settings as app_settings
            self.db_path.setText(str(app_settings.get_database_path()))
            
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
    
    def _on_theme_changed(self, theme: str) -> None:
        """Handle theme change.
        
        Args:
            theme: New theme name
        """
        self.theme_changed.emit(theme.lower())
    
    def _on_detection_engine_changed(self, engine: str) -> None:
        """Handle detection engine change.
        
        Args:
            engine: New detection engine
        """
        self.detection_engine_changed.emit(engine.lower())
    
    def _update_confidence_label(self, value: int) -> None:
        """Update confidence threshold label.
        
        Args:
            value: Confidence threshold value
        """
        self.confidence_label.setText(f"{value}%")
    
    def _test_camera(self) -> None:
        """Test camera settings."""
        QMessageBox.information(
            self, 
            "Camera Test", 
            "Camera test not yet implemented. This would open a camera preview window."
        )
    
    def _populate_camera_list(self) -> None:
        """Populate camera list with available cameras."""
        self.camera_combo.clear()
        self.camera_combo.addItem("Auto-detect", -1)
        
        try:
            import cv2
            for i in range(5):  # Check first 5 camera indices
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    self.camera_combo.addItem(f"Camera {i}", i)
                cap.release()
        except ImportError:
            self.camera_combo.addItem("OpenCV not available", -1)
    
    def _on_camera_selected(self, text: str) -> None:
        """Handle camera selection."""
        index = self.camera_combo.currentData()
        if index != -1:
            self.camera_index.setValue(index)
    
    def _on_camera_index_changed(self, value: int) -> None:
        """Handle camera index change."""
        # Update combo box to match
        for i in range(self.camera_combo.count()):
            if self.camera_combo.itemData(i) == value:
                self.camera_combo.setCurrentIndex(i)
                break
    
    def _test_notification(self) -> None:
        """Test notification system."""
        QMessageBox.information(
            self, 
            "Test Notification", 
            "This is a test notification. Your notification system is working correctly!"
        )
    
    def _export_data(self) -> None:
        """Export application data."""
        QMessageBox.information(
            self, 
            "Export Data", 
            "Data export not yet implemented. This would allow you to export your data to CSV files."
        )
    
    def _import_data(self) -> None:
        """Import application data."""
        QMessageBox.information(
            self, 
            "Import Data", 
            "Data import not yet implemented. This would allow you to import data from CSV files."
        )
    
    def _save_settings(self) -> None:
        """Save all settings."""
        try:
            if not self.database:
                QMessageBox.warning(self, "Error", "Database not available.")
                return
            
            # Get current settings
            settings = self.database.get_user_settings()
            
            # Update settings
            from app.core.models import ThemeMode, DetectionEngine
            settings.theme = ThemeMode(self.theme_combo.currentText().lower())
            settings.detection_engine = DetectionEngine(self.detection_engine.currentText().lower())
            settings.camera_index = self.camera_index.value()
            settings.camera_width = self.camera_width.value()
            settings.camera_height = self.camera_height.value()
            settings.camera_fps = self.camera_fps.value()
            settings.enable_notifications = self.enable_notifications.isChecked()
            settings.goal_reminder_hour = self.reminder_hour.value()
            settings.goal_reminder_minute = self.reminder_minute.value()
            
            # Save to database
            self.database.update_user_settings(settings)
            
            QMessageBox.information(
                self, 
                "Settings Saved", 
                "Settings saved successfully!"
            )
            
            logger.info("Settings saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            QMessageBox.critical(
                self, 
                "Save Error", 
                f"Failed to save settings:\n\n{str(e)}"
            )
    
    def _reset_defaults(self) -> None:
        """Reset settings to defaults."""
        reply = QMessageBox.question(
            self,
            "Reset to Defaults",
            "Are you sure you want to reset all settings to their default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Reset to default values
            self.theme_combo.setCurrentText("Auto")
            self.start_maximized.setChecked(False)
            self.minimize_to_tray.setChecked(True)
            
            self.detection_engine.setCurrentText("Heuristics")
            self.head_tilt_threshold.setValue(25)
            self.hand_distance_threshold.setValue(100)
            self.confidence_threshold.setValue(50)
            
            self.camera_index.setValue(0)
            self.camera_width.setValue(640)
            self.camera_height.setValue(480)
            self.camera_fps.setValue(30)
            
            self.enable_notifications.setChecked(True)
            self.goal_reminder.setChecked(True)
            self.reminder_hour.setValue(20)
            self.reminder_minute.setValue(0)
            
            logger.info("Settings reset to defaults")
    
    def _reset_all_settings(self) -> None:
        """Reset all settings including data."""
        reply = QMessageBox.question(
            self,
            "Reset All Settings",
            "Are you sure you want to reset ALL settings? This will also clear your data!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(
                self, 
                "Reset All", 
                "Reset all settings not yet implemented. This would reset everything to defaults."
            )
    
    def refresh_data(self) -> None:
        """Refresh data (called from parent)."""
        self._load_settings()
