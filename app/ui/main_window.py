"""Main window for Count-Cups application."""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QAction, QActionGroup, QIcon, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QSystemTrayIcon,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from app.core.config import settings
from app.core.db import Database
from app.core.logging import get_logger
from app.ui.screens.calibration import CalibrationScreen
from app.ui.screens.dashboard import DashboardScreen
from app.ui.screens.history import HistoryScreen
from app.ui.screens.live_cam import LiveCameraScreen
from app.ui.screens.settings import SettingsScreen
from app.ui.theme import ThemeManager, ThemeMode

logger = get_logger(__name__)


class MainWindow(QMainWindow):
    """Main application window."""

    # Signals
    theme_changed = pyqtSignal(str)
    detection_engine_changed = pyqtSignal(str)

    def __init__(self):
        """Initialize main window."""
        super().__init__()

        # Initialize components
        self.database: Database | None = None
        self.theme_manager: ThemeManager | None = None
        self.current_screen = "dashboard"

        # Initialize UI
        self._init_ui()
        self._init_database()
        self._init_theme()
        self._init_menu()
        self._init_toolbar()
        self._init_status_bar()

        # Initialize screens only if database is available
        if self.database:
            self._init_screens()
        else:
            logger.error("Cannot initialize screens - database not available")

        self._init_system_tray()

        # Connect signals
        self._connect_signals()

        # Apply initial settings
        self._apply_settings()

        logger.info("Main window initialized")

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        # Save window state
        settings.window_width = self.width()
        settings.window_height = self.height()
        settings.window_maximized = self.isMaximized()

        # Save settings to database
        if self.database:
            try:
                user_settings = self.database.get_user_settings()
                user_settings.window_width = self.width()
                user_settings.window_height = self.height()
                user_settings.window_maximized = self.isMaximized()
                self.database.update_user_settings(user_settings)
            except Exception as e:
                logger.warning(f"Failed to save window state: {e}")

        # Clean up camera resources
        if hasattr(self, "live_cam_screen") and self.live_cam_screen:
            self.live_cam_screen.cleanup_camera()

        # Close database connection
        if self.database:
            self.database.close()

        # Hide to tray if available
        if hasattr(self, "tray_icon") and self.tray_icon and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            super().closeEvent(event)

    def _init_ui(self) -> None:
        """Initialize UI components."""
        # Set window properties
        self.setWindowTitle(f"{settings.app_name} v{settings.app_version}")
        self.setGeometry(100, 100, settings.window_width, settings.window_height)

        if settings.window_maximized:
            self.showMaximized()

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create stacked widget for screens
        self.screen_stack = QStackedWidget()
        main_layout.addWidget(self.screen_stack)

    def _init_database(self) -> None:
        """Initialize database connection."""
        try:
            self.database = Database()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            QMessageBox.critical(
                self,
                "Database Error",
                f"Failed to initialize database:\n\n{str(e)}\n\nPlease check your data directory permissions.",
            )

    def _init_theme(self) -> None:
        """Initialize theme manager."""
        app = QApplication.instance()
        if app:
            self.theme_manager = ThemeManager(app)
            self.theme_manager.theme_changed.connect(self._on_theme_changed)

    def _init_screens(self) -> None:
        """Initialize all screens."""
        # Dashboard screen
        self.dashboard_screen = DashboardScreen(self.database, self)
        self.screen_stack.addWidget(self.dashboard_screen)

        # Live camera screen
        self.live_cam_screen = LiveCameraScreen(self.database, self)
        self.screen_stack.addWidget(self.live_cam_screen)

        # History screen
        self.history_screen = HistoryScreen(self.database, self)
        self.screen_stack.addWidget(self.history_screen)

        # Calibration screen
        self.calibration_screen = CalibrationScreen(self.database, self)
        self.screen_stack.addWidget(self.calibration_screen)

        # Settings screen
        self.settings_screen = SettingsScreen(self.database, self)
        self.screen_stack.addWidget(self.settings_screen)

        # Show dashboard by default
        self.show_screen("dashboard")

    def _init_menu(self) -> None:
        """Initialize menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        # New session action
        new_session_action = QAction("&New Session", self)
        new_session_action.setShortcut(QKeySequence.StandardKey.New)
        new_session_action.triggered.connect(self._new_session)
        file_menu.addAction(new_session_action)

        file_menu.addSeparator()

        # Export actions
        export_daily_action = QAction("Export &Daily Stats", self)
        export_daily_action.triggered.connect(self._export_daily_stats)
        file_menu.addAction(export_daily_action)

        export_events_action = QAction("Export &Sip Events", self)
        export_events_action.triggered.connect(self._export_sip_events)
        file_menu.addAction(export_events_action)

        file_menu.addSeparator()

        # Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        # Screen navigation
        dashboard_action = QAction("&Dashboard", self)
        dashboard_action.setShortcut("Ctrl+1")
        dashboard_action.triggered.connect(lambda: self.show_screen("dashboard"))
        view_menu.addAction(dashboard_action)

        live_cam_action = QAction("&Live Camera", self)
        live_cam_action.setShortcut("Ctrl+2")
        live_cam_action.triggered.connect(lambda: self.show_screen("live_cam"))
        view_menu.addAction(live_cam_action)

        history_action = QAction("&History", self)
        history_action.setShortcut("Ctrl+3")
        history_action.triggered.connect(lambda: self.show_screen("history"))
        view_menu.addAction(history_action)

        calibration_action = QAction("&Calibration", self)
        calibration_action.setShortcut("Ctrl+4")
        calibration_action.triggered.connect(lambda: self.show_screen("calibration"))
        view_menu.addAction(calibration_action)

        settings_action = QAction("&Settings", self)
        settings_action.setShortcut("Ctrl+5")
        settings_action.triggered.connect(lambda: self.show_screen("settings"))
        view_menu.addAction(settings_action)

        view_menu.addSeparator()

        # Theme menu
        theme_menu = view_menu.addMenu("&Theme")

        self.theme_group = QActionGroup(self)

        auto_theme_action = QAction("&Auto", self)
        auto_theme_action.setCheckable(True)
        auto_theme_action.triggered.connect(lambda: self._set_theme("auto"))
        self.theme_group.addAction(auto_theme_action)
        theme_menu.addAction(auto_theme_action)

        light_theme_action = QAction("&Light", self)
        light_theme_action.setCheckable(True)
        light_theme_action.triggered.connect(lambda: self._set_theme("light"))
        self.theme_group.addAction(light_theme_action)
        theme_menu.addAction(light_theme_action)

        dark_theme_action = QAction("&Dark", self)
        dark_theme_action.setCheckable(True)
        dark_theme_action.triggered.connect(lambda: self._set_theme("dark"))
        self.theme_group.addAction(dark_theme_action)
        theme_menu.addAction(dark_theme_action)

        dracula_theme_action = QAction("&Dracula", self)
        dracula_theme_action.setCheckable(True)
        dracula_theme_action.triggered.connect(lambda: self._set_theme("dracula"))
        self.theme_group.addAction(dracula_theme_action)
        theme_menu.addAction(dracula_theme_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

        about_qt_action = QAction("About &Qt", self)
        about_qt_action.triggered.connect(self._show_about_qt)
        help_menu.addAction(about_qt_action)

    def _init_toolbar(self) -> None:
        """Initialize toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Screen navigation buttons
        dashboard_btn = QPushButton("Dashboard")
        dashboard_btn.clicked.connect(lambda: self.show_screen("dashboard"))
        toolbar.addWidget(dashboard_btn)

        live_cam_btn = QPushButton("Live Camera")
        live_cam_btn.clicked.connect(lambda: self.show_screen("live_cam"))
        toolbar.addWidget(live_cam_btn)

        history_btn = QPushButton("History")
        history_btn.clicked.connect(lambda: self.show_screen("history"))
        toolbar.addWidget(history_btn)

        calibration_btn = QPushButton("Calibration")
        calibration_btn.clicked.connect(lambda: self.show_screen("calibration"))
        toolbar.addWidget(calibration_btn)

        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(lambda: self.show_screen("settings"))
        toolbar.addWidget(settings_btn)

        # Add separator
        toolbar.addSeparator()

        # Quick add sip button
        quick_add_btn = QPushButton("Quick Add Sip")
        quick_add_btn.clicked.connect(self._quick_add_sip)
        toolbar.addWidget(quick_add_btn)

    def _init_status_bar(self) -> None:
        """Initialize status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Status label
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)

        # Camera status
        self.camera_status_label = QLabel("Camera: Not Connected")
        self.status_bar.addPermanentWidget(self.camera_status_label)

        # Detection engine status
        self.detection_status_label = QLabel(f"Detection: {settings.detection_engine}")
        self.status_bar.addPermanentWidget(self.detection_status_label)

    def _init_system_tray(self) -> None:
        """Initialize system tray icon."""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)

            # Set icon
            icon_path = settings.assets_dir / "icons" / "CountCups_App.ico"
            if icon_path.exists():
                self.tray_icon.setIcon(QIcon(str(icon_path)))

            # Create context menu
            tray_menu = QMenu()

            show_action = QAction("Show", self)
            show_action.triggered.connect(self.show)
            tray_menu.addAction(show_action)

            hide_action = QAction("Hide", self)
            hide_action.triggered.connect(self.hide)
            tray_menu.addAction(hide_action)

            tray_menu.addSeparator()

            quit_action = QAction("Quit", self)
            quit_action.triggered.connect(self.close)
            tray_menu.addAction(quit_action)

            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.activated.connect(self._on_tray_activated)

            # Show tray icon
            self.tray_icon.show()
        else:
            self.tray_icon = None

    def _connect_signals(self) -> None:
        """Connect signals."""
        # Connect screen signals
        if hasattr(self, "live_cam_screen"):
            self.live_cam_screen.camera_status_changed.connect(
                self._on_camera_status_changed
            )
            self.live_cam_screen.sip_detected.connect(self._on_sip_detected)

        if hasattr(self, "settings_screen"):
            self.settings_screen.detection_engine_changed.connect(
                self._on_detection_engine_changed
            )

    def _apply_settings(self) -> None:
        """Apply initial settings."""
        # Set initial theme
        if self.theme_manager:
            from app.core.models import ThemeMode

            theme_enum = ThemeMode(settings.default_theme)
            self.theme_manager.set_theme(theme_enum)

        # Update status bar
        self.detection_status_label.setText(f"Detection: {settings.detection_engine}")

    def show_screen(self, screen_name: str) -> None:
        """Show specified screen.

        Args:
            screen_name: Name of screen to show
        """
        screen_map = {
            "dashboard": self.dashboard_screen,
            "live_cam": self.live_cam_screen,
            "history": self.history_screen,
            "calibration": self.calibration_screen,
            "settings": self.settings_screen,
        }

        if screen_name in screen_map:
            self.screen_stack.setCurrentWidget(screen_map[screen_name])
            self.current_screen = screen_name

            # Update status label if it exists
            if hasattr(self, "status_label"):
                self.status_label.setText(f"Viewing: {screen_name.title()}")

            # Update toolbar button states
            self._update_toolbar_states(screen_name)

    def _update_toolbar_states(self, active_screen: str) -> None:
        """Update toolbar button states.

        Args:
            active_screen: Currently active screen
        """
        # This would update button states in a real implementation
        pass

    def _set_theme(self, theme: str) -> None:
        """Set application theme.

        Args:
            theme: Theme name
        """
        if self.theme_manager:
            theme_mode = ThemeMode(theme)
            self.theme_manager.set_theme(theme_mode)

    def _on_theme_changed(self, theme: str) -> None:
        """Handle theme change.

        Args:
            theme: New theme name
        """
        # Update theme group selection
        for action in self.theme_group.actions():
            if action.text().lower().replace("&", "") == theme:
                action.setChecked(True)
                break

        self.theme_changed.emit(theme)

    def _on_camera_status_changed(self, status: str) -> None:
        """Handle camera status change.

        Args:
            status: Camera status
        """
        self.camera_status_label.setText(f"Camera: {status}")

    def _on_sip_detected(self, ml_amount: float) -> None:
        """Handle sip detection.

        Args:
            ml_amount: Amount of water in milliliters
        """
        self.status_label.setText(f"Sip detected: {ml_amount:.1f}ml")

        # Update dashboard if visible
        if self.current_screen == "dashboard":
            self.dashboard_screen.refresh_data()

    def _on_detection_engine_changed(self, engine: str) -> None:
        """Handle detection engine change.

        Args:
            engine: New detection engine
        """
        self.detection_status_label.setText(f"Detection: {engine}")
        self.detection_engine_changed.emit(engine)

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """Handle system tray activation.

        Args:
            reason: Activation reason
        """
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.raise_()
                self.activateWindow()

    def _new_session(self) -> None:
        """Start new tracking session."""
        reply = QMessageBox.question(
            self,
            "New Session",
            "Are you sure you want to start a new session? This will reset today's statistics.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Reset daily statistics
            if self.database:
                # This would reset daily stats in a real implementation
                pass

            # Refresh current screen
            current_screen = self.screen_stack.currentWidget()
            if hasattr(current_screen, "refresh_data"):
                current_screen.refresh_data()

            self.status_label.setText("New session started")

    def _export_daily_stats(self) -> None:
        """Export daily statistics."""
        # This would implement CSV export in a real implementation
        QMessageBox.information(
            self, "Export", "Daily statistics export not yet implemented."
        )

    def _export_sip_events(self) -> None:
        """Export sip events."""
        # This would implement CSV export in a real implementation
        QMessageBox.information(
            self, "Export", "Sip events export not yet implemented."
        )

    def _quick_add_sip(self) -> None:
        """Quick add sip manually."""
        # This would show a dialog for manual sip entry
        QMessageBox.information(self, "Quick Add", "Quick add sip not yet implemented.")

    def _show_about(self) -> None:
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Count-Cups",
            f"""
            <h3>{settings.app_name} v{settings.app_version}</h3>
            <p>A cross-platform water intake tracker using computer vision.</p>
            <p>Developed by VoxHash</p>
            <p>Built with Python, PyQt6, and OpenCV</p>
            <p>© 2025 VoxHash. All rights reserved.</p>
            """,
        )

    def _show_about_qt(self) -> None:
        """Show about Qt dialog."""
        QMessageBox.aboutQt(self)

    def changeEvent(self, event) -> None:
        """Handle window state change."""
        if event.type() == event.Type.WindowStateChange:
            if self.isMinimized() and self.tray_icon and self.tray_icon.isVisible():
                self.hide()
                event.ignore()
            else:
                super().changeEvent(event)
        else:
            super().changeEvent(event)
