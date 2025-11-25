"""Main application entry point for Count-Cups."""

import argparse
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMessageBox

from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.ui.main_window import MainWindow

logger = get_logger(__name__)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Count-Cups: A cross-platform water intake tracker using computer vision"
    )

    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=settings.log_level,
        help="Set log level",
    )

    parser.add_argument(
        "--theme",
        choices=["auto", "light", "dark", "dracula"],
        default=settings.default_theme,
        help="Set theme",
    )

    parser.add_argument(
        "--detection-engine",
        choices=["heuristics", "mediapipe"],
        default=settings.detection_engine,
        help="Set detection engine",
    )

    parser.add_argument(
        "--camera-index",
        type=int,
        default=settings.camera_index,
        help="Camera index to use",
    )

    parser.add_argument(
        "--no-camera", action="store_true", help="Run without camera (for testing)"
    )

    parser.add_argument(
        "--version", action="version", version=f"Count-Cups {settings.app_version}"
    )

    return parser.parse_args()


def setup_application() -> QApplication:
    """Set up QApplication with proper configuration.

    Returns:
        Configured QApplication instance
    """
    # Note: DPI scaling attributes are not available in PyQt6
    # PyQt6 handles DPI scaling automatically

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(settings.app_name)
    app.setApplicationVersion(settings.app_version)
    app.setOrganizationName("VoxHash")
    app.setOrganizationDomain("voxhash.com")

    # Set application icon
    icon_path = settings.assets_dir / "icons" / "CountCups_App.ico"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    return app


def check_dependencies() -> bool:
    """Check if all required dependencies are available.

    Returns:
        True if all dependencies are available, False otherwise
    """
    import importlib.util

    missing_deps = []

    deps = {
        "opencv-python": "cv2",
        "numpy": "numpy",
        "PyQt6": "PyQt6",
    }

    for package_name, module_name in deps.items():
        if importlib.util.find_spec(module_name) is None:
            missing_deps.append(package_name)

    if missing_deps:
        logger.error(f"Missing required dependencies: {', '.join(missing_deps)}")
        return False

    return True


def main() -> int:
    """Main application entry point.

    Returns:
        Exit code
    """
    try:
        # Parse arguments
        args = parse_arguments()

        # Update settings from arguments
        if args.debug:
            settings.debug = True
            settings.log_level = "DEBUG"

        if args.log_level:
            settings.log_level = args.log_level

        if args.theme:
            settings.default_theme = args.theme

        if args.detection_engine:
            settings.detection_engine = args.detection_engine

        if args.camera_index is not None:
            settings.camera_index = args.camera_index

        # Set up logging
        setup_logging(level=settings.log_level)
        logger.info(f"Starting {settings.app_name} v{settings.app_version}")

        # Check dependencies
        if not check_dependencies():
            logger.error(
                "Missing required dependencies. Please install them and try again."
            )
            return 1

        # Ensure directories exist
        settings.ensure_directories()

        # Set up application
        app = setup_application()

        # Create and show main window
        main_window = MainWindow()
        main_window.show()

        # Apply theme from settings
        if hasattr(main_window, "theme_manager") and main_window.theme_manager:
            main_window.theme_manager.set_theme(args.theme)

        # Run application
        logger.info("Application started successfully")
        return app.exec()

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        return 0
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)

        # Show error dialog if possible
        try:
            app_instance = QApplication.instance()
            if app_instance:
                from PyQt6.QtWidgets import QApplication as QApp
                if isinstance(app_instance, QApp):
                    QMessageBox.critical(
                        None,
                        "Fatal Error",
                        f"An unexpected error occurred:\n\n{str(e)}\n\nPlease check the logs for more details.",
                    )
        except Exception:
            pass

        return 1


if __name__ == "__main__":
    sys.exit(main())
