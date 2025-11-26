# Count-Cups Documentation

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Overview

Count-Cups is a cross-platform water intake tracker that uses computer vision to automatically detect and count your drinking gestures. It helps you stay hydrated by tracking your daily water consumption through intelligent sip detection and manual entry options.

## Features

### 🎯 Core Features

- **Automatic Sip Detection**: Uses computer vision to detect drinking gestures from your webcam
- **Manual Entry**: Quick-add sips or cups when automatic detection isn't available
- **Daily Goal Tracking**: Set and track daily hydration goals
- **Statistics & Analytics**: View your hydration patterns over time
- **Multiple Cup Profiles**: Calibrate different cup sizes and types
- **Cross-Platform**: Works on Windows, macOS, and Linux

### 🎨 User Interface

- **Modern UI**: Clean, responsive PyQt6 interface
- **Theme Support**: Auto-detection with manual theme switching (Light, Dark, Dracula)
- **Accessibility**: Keyboard shortcuts, high-contrast mode, resizable fonts
- **System Tray**: Minimize to system tray on supported platforms

### 🔧 Technical Features

- **Detection Engines**: Heuristic-based detection (default) with optional MediaPipe support
- **Data Persistence**: SQLite database with migration support
- **Export/Import**: CSV export and import functionality
- **Notifications**: Desktop notifications for goal reminders
- **Privacy-First**: All data stored locally, optional telemetry

## Installation

### Pre-built Binaries

Download the latest release from the [GitHub Releases](https://github.com/VoxHash/Count-Cups/releases) page:

- **Windows**: `Count-Cups.exe` (standalone executable)
- **macOS**: `Count-Cups.dmg` (disk image)
- **Linux**: `count-cups` (AppImage or DEB package)

### From Source

1. **Clone the repository**:
   ```bash
   git clone https://github.com/VoxHash/Count-Cups.git
   cd Count-Cups
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python -m app.main
   ```

## Quick Start

1. **Launch Count-Cups** and allow camera access when prompted
2. **Set up your first cup profile** in the Calibration screen
3. **Configure your daily goal** in Settings
4. **Start tracking** by going to the Live Camera screen
5. **View your progress** on the Dashboard

### First-Time Setup

1. **Camera Setup**: Ensure your webcam is working and positioned correctly
2. **Calibration**: Use the Calibration screen to set up your cup profiles
3. **Goal Setting**: Set your daily water intake goal in Settings
4. **Detection Test**: Test the detection system in the Live Camera screen

## Configuration

### Environment Variables

Create a `.env` file in the project root to customize settings:

```env
# Application Settings
DEBUG=false
LOG_LEVEL=INFO

# Detection Settings
DETECTION_ENGINE=heuristics
SIP_DURATION_MIN=0.8
SIP_DURATION_MAX=3.5
HEAD_TILT_THRESHOLD=25.0
HAND_FACE_DISTANCE_THRESHOLD=100.0

# Calibration
DEFAULT_CUP_SIZE_ML=250
DEFAULT_SIPS_PER_CUP=10

# Notifications
ENABLE_NOTIFICATIONS=true
GOAL_REMINDER_HOUR=20
GOAL_REMINDER_MINUTE=0

# UI Settings
DEFAULT_THEME=auto
WINDOW_WIDTH=1200
WINDOW_HEIGHT=800
WINDOW_MAXIMIZED=false

# Camera Settings
CAMERA_INDEX=0
CAMERA_WIDTH=640
CAMERA_HEIGHT=480
CAMERA_FPS=30
```

### Settings Screen

Access the Settings screen to configure:

- **General**: Theme, window behavior, system tray
- **Detection**: Engine selection, sensitivity parameters
- **Camera**: Camera selection, resolution, frame rate
- **Notifications**: Goal reminders, notification preferences
- **Advanced**: Database settings, logging, telemetry

## Usage

### Dashboard

The Dashboard provides an overview of your daily hydration:

- **Today's Intake**: Total milliliters, cups, and sips consumed
- **Goal Progress**: Visual progress bar and percentage
- **Quick Actions**: Manual sip/cup entry buttons
- **Recent Activity**: List of recent sip events

### Live Camera

The Live Camera screen shows real-time detection:

- **Camera Feed**: Live video from your webcam
- **Detection Overlay**: Visual indicators for face and hand detection
- **Controls**: Start/stop detection, calibration tools
- **Status**: Detection status and confidence levels

### History

View your hydration history and analytics:

- **Daily Stats**: Day-by-day breakdown of your intake
- **Weekly/Monthly Views**: Longer-term trends
- **Export Options**: CSV export for external analysis
- **Goal Achievement**: Track your consistency

### Calibration

Set up and manage cup profiles:

- **Cup Profiles**: Define different cup sizes and types
- **Detection Parameters**: Fine-tune detection sensitivity
- **Test Mode**: Validate your calibration settings
- **Multiple Profiles**: Support for different drinking vessels

### Settings

Configure application behavior:

- **Appearance**: Themes, window settings, accessibility
- **Detection**: Engine selection, sensitivity tuning
- **Camera**: Device selection, resolution, frame rate
- **Notifications**: Goal reminders, desktop notifications
- **Advanced**: Database, logging, telemetry options

## Troubleshooting

### Common Issues

#### Camera Not Detected
- **Check camera permissions**: Ensure the application has camera access
- **Try different camera index**: Use Settings > Camera to change camera index
- **Verify camera is not in use**: Close other applications using the camera
- **Check drivers**: Update camera drivers on Windows

#### Poor Detection Accuracy
- **Improve lighting**: Ensure good lighting on your face
- **Adjust camera position**: Position camera at eye level
- **Calibrate settings**: Use the Calibration screen to fine-tune detection
- **Check detection engine**: Try switching between Heuristics and MediaPipe

#### Application Crashes
- **Check logs**: Look in `~/.count-cups/logs/` for error details
- **Update dependencies**: Ensure all required packages are installed
- **Reset settings**: Use Settings > Advanced > Reset All Settings
- **Report issue**: Create an issue on GitHub with log details

#### Performance Issues
- **Reduce camera resolution**: Lower camera resolution in Settings
- **Close other applications**: Free up system resources
- **Check system requirements**: Ensure your system meets minimum requirements
- **Update graphics drivers**: Keep graphics drivers up to date

### System Requirements

#### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **Python**: 3.10+ (for source installation)
- **RAM**: 4GB
- **Storage**: 100MB
- **Camera**: USB webcam or built-in camera

#### Recommended Requirements
- **OS**: Windows 11, macOS 12+, or Linux (Ubuntu 20.04+)
- **Python**: 3.11+ (for source installation)
- **RAM**: 8GB
- **Storage**: 500MB
- **Camera**: HD webcam with good lighting

### Getting Help

1. **Check the documentation**: Review this guide and other docs
2. **Search issues**: Look through existing GitHub issues
3. **Create an issue**: Report bugs or request features
4. **Join discussions**: Participate in GitHub Discussions

## Development

### Setting Up Development Environment

1. **Clone and setup**:
   ```bash
   git clone https://github.com/VoxHash/Count-Cups.git
   cd Count-Cups
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. **Run in development mode**:
   ```bash
   # Linux/macOS
   ./scripts/dev_run.sh
   
   # Windows
   .\scripts\dev_run.ps1
   ```

3. **Run tests**:
   ```bash
   pytest tests/ -v
   ```

4. **Run linting**:
   ```bash
   ruff check .
   ruff format .
   mypy app/
   ```

### Building from Source

#### Windows
```powershell
.\scripts\build_win_nuitka.ps1 -Release
```

#### macOS
```bash
./scripts/build_mac_nuitka.sh --release
```

#### Linux
```bash
./scripts/build_linux_nuitka.sh --release
```

### Project Structure

```
Count-Cups/
├── app/                    # Main application code
│   ├── core/              # Core functionality
│   ├── ui/                # User interface
│   ├── services/          # Background services
│   └── assets/            # Static assets
├── tests/                 # Test suite
├── scripts/               # Build and utility scripts
├── docs/                  # Documentation
├── .github/               # GitHub templates and issue templates
└── requirements.txt       # Python dependencies
```

### Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Run the test suite**: `pytest tests/ -v`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Code Style

- **Formatting**: Black with 88 character line length
- **Linting**: Ruff for fast linting and import sorting
- **Type Checking**: MyPy for static type analysis
- **Testing**: Pytest with coverage reporting
- **Documentation**: Google-style docstrings

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **OpenCV** for computer vision capabilities
- **PyQt6** for the modern user interface
- **MediaPipe** for advanced pose detection (optional)
- **SQLite** for local data storage
- **Nuitka** for cross-platform compilation

---

**Count-Cups** - Stay hydrated, stay healthy! 💧
