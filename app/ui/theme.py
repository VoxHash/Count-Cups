"""Theme management for Count-Cups UI."""

import sys
from enum import Enum
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication

from app.core.logging import get_logger

logger = get_logger(__name__)


class ThemeMode(Enum):
    """Available theme modes."""

    AUTO = "auto"
    LIGHT = "light"
    DARK = "dark"
    DRACULA = "dracula"


class ThemeManager(QObject):
    """Manages application themes and styling."""

    theme_changed = pyqtSignal(str)  # Emitted when theme changes

    def __init__(self, app: QApplication):
        """Initialize theme manager.

        Args:
            app: QApplication instance
        """
        super().__init__()
        self.app = app
        self.current_theme = ThemeMode.AUTO
        self._themes = self._create_themes()
        self._apply_theme(self._detect_system_theme())

    def _create_themes(self) -> dict[ThemeMode, dict[str, Any]]:
        """Create theme definitions.

        Returns:
            Dictionary of theme definitions
        """
        return {
            ThemeMode.LIGHT: {
                "name": "Light",
                "colors": {
                    "primary": "#2563eb",
                    "primary_hover": "#1d4ed8",
                    "secondary": "#64748b",
                    "success": "#059669",
                    "warning": "#d97706",
                    "error": "#dc2626",
                    "info": "#0891b2",
                    "background": "#ffffff",
                    "surface": "#f8fafc",
                    "surface_variant": "#f1f5f9",
                    "outline": "#e2e8f0",
                    "outline_variant": "#cbd5e1",
                    "on_background": "#0f172a",
                    "on_surface": "#1e293b",
                    "on_surface_variant": "#475569",
                    "on_primary": "#ffffff",
                    "on_secondary": "#ffffff",
                    "text_primary": "#0f172a",
                    "text_secondary": "#475569",
                    "text_disabled": "#94a3b8",
                    "shadow": "#00000020",
                    "overlay": "#00000080",
                    # Additional colors for modern UI
                    "card_background": "#ffffff",
                    "card_border": "#e2e8f0",
                    "button_primary": "#2563eb",
                    "button_secondary": "#64748b",
                    "button_hover": "#1d4ed8",
                    "accent": "#2563eb",
                    "accent_hover": "#1d4ed8",
                },
                "fonts": {
                    "family": "Segoe UI, Arial, sans-serif",
                    "size_small": 10,
                    "size_medium": 12,
                    "size_large": 14,
                    "size_xlarge": 16,
                    "size_xxlarge": 20,
                    "size_title": 24,
                },
            },
            ThemeMode.DARK: {
                "name": "Dark",
                "colors": {
                    "primary": "#3b82f6",
                    "primary_hover": "#2563eb",
                    "secondary": "#64748b",
                    "success": "#10b981",
                    "warning": "#f59e0b",
                    "error": "#ef4444",
                    "info": "#06b6d4",
                    "background": "#0a0a0a",
                    "surface": "#1a1a1a",
                    "surface_variant": "#2a2a2a",
                    "outline": "#404040",
                    "outline_variant": "#606060",
                    "on_background": "#ffffff",
                    "on_surface": "#f0f0f0",
                    "on_surface_variant": "#d0d0d0",
                    "on_primary": "#ffffff",
                    "on_secondary": "#ffffff",
                    "text_primary": "#ffffff",
                    "text_secondary": "#d0d0d0",
                    "text_disabled": "#808080",
                    "shadow": "#00000060",
                    "overlay": "#00000090",
                    # Additional colors for modern UI
                    "card_background": "#1e1e1e",
                    "card_border": "#333333",
                    "button_primary": "#3b82f6",
                    "button_secondary": "#404040",
                    "button_hover": "#4f46e5",
                    "accent": "#3b82f6",
                    "accent_hover": "#2563eb",
                },
                "fonts": {
                    "family": "Segoe UI, Arial, sans-serif",
                    "size_small": 10,
                    "size_medium": 12,
                    "size_large": 14,
                    "size_xlarge": 16,
                    "size_xxlarge": 20,
                    "size_title": 24,
                },
            },
            ThemeMode.DRACULA: {
                "name": "Dracula",
                "colors": {
                    "primary": "#bd93f9",
                    "primary_hover": "#a855f7",
                    "secondary": "#6272a4",
                    "success": "#50fa7b",
                    "warning": "#ffb86c",
                    "error": "#ff5555",
                    "info": "#8be9fd",
                    "background": "#282a36",
                    "surface": "#44475a",
                    "surface_variant": "#6272a4",
                    "outline": "#6272a4",
                    "outline_variant": "#8be9fd",
                    "on_background": "#f8f8f2",
                    "on_surface": "#f8f8f2",
                    "on_surface_variant": "#f8f8f2",
                    "on_primary": "#282a36",
                    "on_secondary": "#f8f8f2",
                    "text_primary": "#f8f8f2",
                    "text_secondary": "#6272a4",
                    "text_disabled": "#44475a",
                    "shadow": "#00000040",
                    "overlay": "#00000080",
                    # Additional colors for modern UI
                    "card_background": "#44475a",
                    "card_border": "#6272a4",
                    "button_primary": "#bd93f9",
                    "button_secondary": "#6272a4",
                    "button_hover": "#a855f7",
                    "accent": "#bd93f9",
                    "accent_hover": "#a855f7",
                },
                "fonts": {
                    "family": "JetBrains Mono, Consolas, monospace",
                    "size_small": 10,
                    "size_medium": 12,
                    "size_large": 14,
                    "size_xlarge": 16,
                    "size_xxlarge": 20,
                    "size_title": 24,
                },
            },
        }

    def _detect_system_theme(self) -> ThemeMode:
        """Detect system theme preference.

        Returns:
            Detected theme mode
        """
        try:
            # Try to detect system theme
            if sys.platform == "win32":
                import winreg

                try:
                    key = winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER,
                        r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                    )
                    value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                    winreg.CloseKey(key)
                    return ThemeMode.LIGHT if value == 1 else ThemeMode.DARK
                except (OSError, FileNotFoundError):
                    pass
            elif sys.platform == "darwin":
                # macOS theme detection would go here
                pass
            elif sys.platform.startswith("linux"):
                # Linux theme detection would go here
                pass
        except Exception as e:
            logger.warning(f"Failed to detect system theme: {e}")

        # Default to dark theme
        return ThemeMode.DARK

    def get_theme(self) -> ThemeMode:
        """Get current theme.

        Returns:
            Current theme mode
        """
        return self.current_theme

    def set_theme(self, theme) -> None:
        """Set application theme.

        Args:
            theme: Theme mode to set (ThemeMode enum or string)
        """
        # Convert string to ThemeMode enum if needed
        if isinstance(theme, str):
            try:
                theme = ThemeMode(theme)
            except ValueError:
                logger.warning(f"Invalid theme string '{theme}', using AUTO")
                theme = ThemeMode.AUTO

        if theme == ThemeMode.AUTO:
            theme = self._detect_system_theme()

        self.current_theme = theme
        self._apply_theme(theme)
        self.theme_changed.emit(theme.value)

        logger.info(f"Theme changed to {theme.value}")

    def _apply_theme(self, theme: ThemeMode) -> None:
        """Apply theme to application.

        Args:
            theme: Theme to apply
        """
        if theme == ThemeMode.AUTO:
            theme = self._detect_system_theme()

        # Ensure we have a valid theme that exists in our themes dictionary
        if theme not in self._themes:
            logger.warning(f"Theme {theme} not found, falling back to DARK theme")
            theme = ThemeMode.DARK

        theme_config = self._themes[theme]
        colors = theme_config["colors"]

        # Create palette
        palette = QPalette()

        # Set colors
        palette.setColor(QPalette.ColorRole.Window, QColor(colors["background"]))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(colors["text_primary"]))
        palette.setColor(QPalette.ColorRole.Base, QColor(colors["surface"]))
        palette.setColor(
            QPalette.ColorRole.AlternateBase, QColor(colors["surface_variant"])
        )
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors["surface"]))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors["text_primary"]))
        palette.setColor(QPalette.ColorRole.Text, QColor(colors["text_primary"]))
        palette.setColor(QPalette.ColorRole.Button, QColor(colors["surface"]))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors["text_primary"]))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(colors["error"]))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(colors["primary"]))
        palette.setColor(
            QPalette.ColorRole.HighlightedText, QColor(colors["on_primary"])
        )

        # Apply palette
        self.app.setPalette(palette)

        # Set application style
        self.app.setStyle("Fusion")

        # Apply custom stylesheet
        stylesheet = self._create_stylesheet(theme_config)
        self.app.setStyleSheet(stylesheet)

    def _create_stylesheet(self, theme_config: dict[str, Any]) -> str:
        """Create custom stylesheet for theme.

        Args:
            theme_config: Theme configuration

        Returns:
            CSS stylesheet string
        """
        colors = theme_config["colors"]
        fonts = theme_config["fonts"]

        return f"""
        /* Global Styles */
        QWidget {{
            font-family: '{fonts["family"]}';
            font-size: {fonts["size_medium"]}px;
            color: {colors["text_primary"]};
            background-color: {colors["background"]};
        }}

        /* Main Window */
        QMainWindow {{
            background-color: {colors["background"]};
            color: {colors["text_primary"]};
            border: none;
        }}

        /* Cards and panels */
        .card {{
            background-color: {colors["card_background"]};
            border: 1px solid {colors["card_border"]};
            border-radius: 8px;
            padding: 16px;
            margin: 8px;
        }}

        .panel {{
            background-color: {colors["surface"]};
            border: 1px solid {colors["outline"]};
            border-radius: 6px;
            padding: 12px;
        }}

        /* Buttons */
        QPushButton {{
            background-color: {colors["button_primary"]};
            color: {colors["on_primary"]};
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: {fonts["size_medium"]}px;
            min-height: 20px;
        }}

        QPushButton:hover {{
            background-color: {colors["primary_hover"]};
        }}

        QPushButton:pressed {{
            background-color: {colors["primary_hover"]};
        }}

        QPushButton:disabled {{
            background-color: {colors["outline_variant"]};
            color: {colors["text_disabled"]};
        }}

        /* Secondary Button */
        QPushButton[class="secondary"] {{
            background-color: {colors["surface"]};
            color: {colors["text_primary"]};
            border: 1px solid {colors["outline"]};
        }}

        QPushButton[class="secondary"]:hover {{
            background-color: {colors["surface_variant"]};
        }}

        /* Success Button */
        QPushButton[class="success"] {{
            background-color: {colors["success"]};
            color: white;
        }}

        QPushButton[class="success"]:hover {{
            background-color: {colors["success"]};
            opacity: 0.9;
        }}

        /* Warning Button */
        QPushButton[class="warning"] {{
            background-color: {colors["warning"]};
            color: white;
        }}

        QPushButton[class="warning"]:hover {{
            background-color: {colors["warning"]};
            opacity: 0.9;
        }}

        /* Error Button */
        QPushButton[class="error"] {{
            background-color: {colors["error"]};
            color: white;
        }}

        QPushButton[class="error"]:hover {{
            background-color: {colors["error"]};
            opacity: 0.9;
        }}

        /* Labels */
        QLabel {{
            color: {colors["text_primary"]};
        }}

        QLabel[class="secondary"] {{
            color: {colors["text_secondary"]};
        }}

        QLabel[class="disabled"] {{
            color: {colors["text_disabled"]};
        }}

        QLabel[class="title"] {{
            font-size: {fonts["size_title"]}px;
            font-weight: bold;
        }}

        QLabel[class="heading"] {{
            font-size: {fonts["size_xxlarge"]}px;
            font-weight: 600;
        }}

        QLabel[class="subheading"] {{
            font-size: {fonts["size_xlarge"]}px;
            font-weight: 500;
        }}

        /* Line Edit */
        QLineEdit {{
            background-color: {colors["surface"]};
            border: 1px solid {colors["outline"]};
            border-radius: 4px;
            padding: 8px 12px;
            color: {colors["text_primary"]};
        }}

        QLineEdit:focus {{
            border-color: {colors["primary"]};
        }}

        QLineEdit:disabled {{
            background-color: {colors["surface_variant"]};
            color: {colors["text_disabled"]};
        }}

        /* Spin Box */
        QSpinBox, QDoubleSpinBox {{
            background-color: {colors["surface"]};
            border: 1px solid {colors["outline"]};
            border-radius: 4px;
            padding: 8px 12px;
            color: {colors["text_primary"]};
        }}

        QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {colors["primary"]};
        }}

        /* Combo Box */
        QComboBox {{
            background-color: {colors["surface"]};
            border: 1px solid {colors["outline"]};
            border-radius: 4px;
            padding: 8px 12px;
            color: {colors["text_primary"]};
        }}

        QComboBox:focus {{
            border-color: {colors["primary"]};
        }}

        QComboBox::drop-down {{
            border: none;
        }}

        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {colors["text_secondary"]};
            margin-right: 8px;
        }}

        QComboBox QAbstractItemView {{
            background-color: {colors["surface"]};
            border: 1px solid {colors["outline"]};
            selection-background-color: {colors["primary"]};
            color: {colors["text_primary"]};
        }}

        /* Check Box */
        QCheckBox {{
            color: {colors["text_primary"]};
        }}

        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 1px solid {colors["outline"]};
            border-radius: 3px;
            background-color: {colors["surface"]};
        }}

        QCheckBox::indicator:checked {{
            background-color: {colors["primary"]};
            border-color: {colors["primary"]};
        }}

        /* Radio Button */
        QRadioButton {{
            color: {colors["text_primary"]};
        }}

        QRadioButton::indicator {{
            width: 18px;
            height: 18px;
            border: 1px solid {colors["outline"]};
            border-radius: 9px;
            background-color: {colors["surface"]};
        }}

        QRadioButton::indicator:checked {{
            background-color: {colors["primary"]};
            border-color: {colors["primary"]};
        }}

        /* Slider */
        QSlider::groove:horizontal {{
            height: 6px;
            background-color: {colors["outline_variant"]};
            border-radius: 3px;
        }}

        QSlider::handle:horizontal {{
            background-color: {colors["primary"]};
            border: none;
            width: 18px;
            height: 18px;
            border-radius: 9px;
            margin: -6px 0;
        }}

        QSlider::handle:horizontal:hover {{
            background-color: {colors["primary_hover"]};
        }}

        /* Progress Bar */
        QProgressBar {{
            background-color: {colors["outline_variant"]};
            border: none;
            border-radius: 3px;
            text-align: center;
            color: {colors["text_primary"]};
        }}

        QProgressBar::chunk {{
            background-color: {colors["primary"]};
            border-radius: 3px;
        }}

        /* Group Box */
        QGroupBox {{
            font-weight: 600;
            border: 1px solid {colors["outline"]};
            border-radius: 6px;
            margin-top: 8px;
            padding-top: 8px;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 8px;
            padding: 0 8px 0 8px;
            background-color: {colors["background"]};
        }}

        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {colors["outline"]};
            border-radius: 6px;
            background-color: {colors["surface"]};
        }}

        QTabBar::tab {{
            background-color: {colors["surface_variant"]};
            color: {colors["text_secondary"]};
            border: 1px solid {colors["outline"]};
            border-bottom: none;
            border-radius: 6px 6px 0 0;
            padding: 8px 16px;
            margin-right: 2px;
        }}

        QTabBar::tab:selected {{
            background-color: {colors["surface"]};
            color: {colors["text_primary"]};
        }}

        QTabBar::tab:hover {{
            background-color: {colors["surface"]};
        }}

        /* Scroll Bar */
        QScrollBar:vertical {{
            background-color: {colors["surface_variant"]};
            width: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {colors["outline"]};
            border-radius: 6px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {colors["text_secondary"]};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            background-color: {colors["surface_variant"]};
            height: 12px;
            border-radius: 6px;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {colors["outline"]};
            border-radius: 6px;
            min-width: 20px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: {colors["text_secondary"]};
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}

        /* Menu Bar */
        QMenuBar {{
            background-color: {colors["surface"]};
            color: {colors["text_primary"]};
            border-bottom: 1px solid {colors["outline"]};
        }}

        QMenuBar::item {{
            padding: 8px 12px;
        }}

        QMenuBar::item:selected {{
            background-color: {colors["surface_variant"]};
        }}

        QMenu {{
            background-color: {colors["surface"]};
            color: {colors["text_primary"]};
            border: 1px solid {colors["outline"]};
            border-radius: 6px;
        }}

        QMenu::item {{
            padding: 8px 16px;
        }}

        QMenu::item:selected {{
            background-color: {colors["primary"]};
            color: {colors["on_primary"]};
        }}

        /* Status Bar */
        QStatusBar {{
            background-color: {colors["surface"]};
            color: {colors["text_secondary"]};
            border-top: 1px solid {colors["outline"]};
        }}

        /* Tool Bar */
        QToolBar {{
            background-color: {colors["surface"]};
            border: none;
            spacing: 4px;
        }}

        QToolButton {{
            background-color: transparent;
            border: none;
            border-radius: 4px;
            padding: 8px;
        }}

        QToolButton:hover {{
            background-color: {colors["surface_variant"]};
        }}

        QToolButton:pressed {{
            background-color: {colors["outline_variant"]};
        }}
        """

    def get_color(self, color_name: str) -> str:
        """Get color value by name.

        Args:
            color_name: Name of the color

        Returns:
            Color value as hex string
        """
        theme_config = self._themes[self.current_theme]
        return theme_config["colors"].get(color_name, "#000000")

    def get_font_size(self, size_name: str) -> int:
        """Get font size by name.

        Args:
            size_name: Name of the font size

        Returns:
            Font size in pixels
        """
        theme_config = self._themes[self.current_theme]
        return theme_config["fonts"].get(size_name, 12)

    def get_available_themes(self) -> list[str]:
        """Get list of available theme names.

        Returns:
            List of theme names
        """
        return [theme.value for theme in ThemeMode]
