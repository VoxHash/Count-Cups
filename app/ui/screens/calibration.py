"""Calibration screen for Count-Cups."""

from typing import Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QSpinBox, QLineEdit, QGroupBox, QFormLayout,
    QMessageBox, QProgressBar, QCheckBox
)

from app.core.db import Database
from app.core.logging import get_logger

logger = get_logger(__name__)


class CalibrationScreen(QWidget):
    """Calibration screen for setting up cup profiles and detection parameters."""
    
    def __init__(self, database: Optional[Database], parent=None):
        """Initialize calibration screen.
        
        Args:
            database: Database instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.database = database
        self.parent_window = parent
        
        self._init_ui()
        self._load_cup_profiles()
    
    def _init_ui(self) -> None:
        """Initialize UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Calibration")
        title.setProperty("class", "title")
        layout.addWidget(title)
        
        # Cup Profile Section
        cup_group = QGroupBox("Cup Profile")
        cup_layout = QFormLayout(cup_group)
        
        self.cup_name = QLineEdit()
        self.cup_name.setPlaceholderText("e.g., Coffee Mug, Water Bottle")
        cup_layout.addRow("Name:", self.cup_name)
        
        self.cup_size = QSpinBox()
        self.cup_size.setRange(50, 2000)
        self.cup_size.setValue(250)
        self.cup_size.setSuffix(" ml")
        cup_layout.addRow("Size:", self.cup_size)
        
        self.sips_per_cup = QSpinBox()
        self.sips_per_cup.setRange(1, 100)
        self.sips_per_cup.setValue(10)
        cup_layout.addRow("Sips per Cup:", self.sips_per_cup)
        
        self.cup_color = QLineEdit()
        self.cup_color.setPlaceholderText("#3b82f6")
        cup_layout.addRow("Color (hex):", self.cup_color)
        
        self.is_default = QCheckBox()
        self.is_default.setChecked(True)
        cup_layout.addRow("Default Profile:", self.is_default)
        
        layout.addWidget(cup_group)
        
        # Detection Parameters Section
        detection_group = QGroupBox("Detection Parameters")
        detection_layout = QFormLayout(detection_group)
        
        self.head_tilt_threshold = QSpinBox()
        self.head_tilt_threshold.setRange(10, 60)
        self.head_tilt_threshold.setValue(25)
        self.head_tilt_threshold.setSuffix("°")
        detection_layout.addRow("Head Tilt Threshold:", self.head_tilt_threshold)
        
        self.hand_distance_threshold = QSpinBox()
        self.hand_distance_threshold.setRange(50, 200)
        self.hand_distance_threshold.setValue(100)
        self.hand_distance_threshold.setSuffix(" px")
        detection_layout.addRow("Hand-Face Distance:", self.hand_distance_threshold)
        
        self.sip_duration_min = QSpinBox()
        self.sip_duration_min.setRange(1, 10)
        self.sip_duration_min.setValue(8)
        self.sip_duration_min.setSuffix(" frames")
        detection_layout.addRow("Min Sip Duration:", self.sip_duration_min)
        
        self.sip_duration_max = QSpinBox()
        self.sip_duration_max.setRange(10, 100)
        self.sip_duration_max.setValue(35)
        self.sip_duration_max.setSuffix(" frames")
        detection_layout.addRow("Max Sip Duration:", self.sip_duration_max)
        
        layout.addWidget(detection_group)
        
        # Calibration Test Section
        test_group = QGroupBox("Calibration Test")
        test_layout = QVBoxLayout(test_group)
        
        test_info = QLabel(
            "Test your calibration by performing drinking gestures in front of the camera. "
            "The system will detect and count sips based on your settings."
        )
        test_info.setWordWrap(True)
        test_info.setProperty("class", "secondary")
        test_layout.addWidget(test_info)
        
        test_buttons = QHBoxLayout()
        
        self.start_test_btn = QPushButton("Start Test")
        self.start_test_btn.clicked.connect(self._start_test)
        test_buttons.addWidget(self.start_test_btn)
        
        self.stop_test_btn = QPushButton("Stop Test")
        self.stop_test_btn.clicked.connect(self._stop_test)
        self.stop_test_btn.setEnabled(False)
        test_buttons.addWidget(self.stop_test_btn)
        
        test_layout.addLayout(test_buttons)
        
        # Test progress
        self.test_progress = QProgressBar()
        self.test_progress.setVisible(False)
        test_layout.addWidget(self.test_progress)
        
        # Test results
        self.test_results = QLabel("Test not started")
        self.test_results.setProperty("class", "secondary")
        test_layout.addWidget(self.test_results)
        
        layout.addWidget(test_group)
        
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
    
    def _load_cup_profiles(self) -> None:
        """Load existing cup profiles."""
        if not self.database:
            return
        
        try:
            profiles = self.database.get_all_cup_profiles()
            if profiles:
                # Load the first profile as default
                profile = profiles[0]
                self.cup_name.setText(profile.name)
                self.cup_size.setValue(profile.size_ml)
                self.sips_per_cup.setValue(profile.sips_per_cup)
                self.cup_color.setText(profile.color or "")
                self.is_default.setChecked(profile.is_default)
        except Exception as e:
            logger.error(f"Failed to load cup profiles: {e}")
    
    def _start_test(self) -> None:
        """Start calibration test."""
        self.start_test_btn.setEnabled(False)
        self.stop_test_btn.setEnabled(True)
        self.test_progress.setVisible(True)
        self.test_progress.setRange(0, 100)
        self.test_progress.setValue(0)
        self.test_results.setText("Test in progress... Perform drinking gestures")
        
        # Simulate test progress
        self._simulate_test_progress()
    
    def _stop_test(self) -> None:
        """Stop calibration test."""
        self.start_test_btn.setEnabled(True)
        self.stop_test_btn.setEnabled(False)
        self.test_progress.setVisible(False)
        self.test_results.setText("Test stopped")
    
    def _simulate_test_progress(self) -> None:
        """Simulate test progress (placeholder)."""
        import random
        progress = random.randint(10, 90)
        self.test_progress.setValue(progress)
        
        if progress < 100:
            # Continue test
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(1000, self._simulate_test_progress)
        else:
            # Test complete
            self.test_results.setText("Test completed! Detection sensitivity looks good.")
            self.stop_test()
    
    def _save_settings(self) -> None:
        """Save calibration settings."""
        try:
            # Validate inputs
            if not self.cup_name.text().strip():
                QMessageBox.warning(self, "Validation Error", "Please enter a cup name.")
                return
            
            # Create cup profile
            from app.core.models import CupProfile
            from datetime import datetime
            
            profile = CupProfile(
                name=self.cup_name.text().strip(),
                size_ml=self.cup_size.value(),
                sips_per_cup=self.sips_per_cup.value(),
                color=self.cup_color.text().strip() or None,
                is_default=self.is_default.isChecked(),
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Save to database
            if self.database:
                profile_id = self.database.create_cup_profile(profile)
                profile.id = profile_id
                
                QMessageBox.information(
                    self, 
                    "Settings Saved", 
                    f"Cup profile '{profile.name}' saved successfully!"
                )
                
                logger.info(f"Cup profile saved: {profile.name}")
            
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            QMessageBox.critical(
                self, 
                "Save Error", 
                f"Failed to save settings:\n\n{str(e)}"
            )
    
    def _reset_defaults(self) -> None:
        """Reset to default settings."""
        reply = QMessageBox.question(
            self,
            "Reset to Defaults",
            "Are you sure you want to reset all settings to their default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.cup_name.setText("Default Cup")
            self.cup_size.setValue(250)
            self.sips_per_cup.setValue(10)
            self.cup_color.setText("#3b82f6")
            self.is_default.setChecked(True)
            
            self.head_tilt_threshold.setValue(25)
            self.hand_distance_threshold.setValue(100)
            self.sip_duration_min.setValue(8)
            self.sip_duration_max.setValue(35)
            
            logger.info("Settings reset to defaults")
    
    def refresh_data(self) -> None:
        """Refresh data (called from parent)."""
        self._load_cup_profiles()
