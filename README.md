# Count-Cups 💧

[![CI/CD Pipeline](https://github.com/VoxHash/Count-Cups/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/VoxHash/Count-Cups/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/VoxHash/Count-Cups)

A cross-platform water intake tracker that uses computer vision to automatically detect and count your drinking gestures. Stay hydrated with intelligent sip detection and comprehensive tracking features.

## ✨ Features

### 🎯 Core Functionality
- **🤖 Automatic Sip Detection**: Uses computer vision to detect drinking gestures from your webcam
- **✋ Manual Entry**: Quick-add sips or cups when automatic detection isn't available
- **📊 Daily Goal Tracking**: Set and track daily hydration goals with visual progress indicators
- **📈 Statistics & Analytics**: View your hydration patterns over time with detailed charts
- **☕ Multiple Cup Profiles**: Calibrate different cup sizes and types for accurate tracking
- **🌍 Cross-Platform**: Works seamlessly on Windows, macOS, and Linux

### 🎨 User Experience
- **🎨 Modern UI**: Clean, responsive PyQt6 interface with dark/light themes
- **🌙 Theme Support**: Auto-detection with manual theme switching (Light, Dark, Dracula)
- **♿ Accessibility**: Keyboard shortcuts, high-contrast mode, resizable fonts
- **🔔 Smart Notifications**: Desktop notifications for goal reminders and achievements
- **📱 System Tray**: Minimize to system tray on supported platforms

### 🔧 Technical Features
- **🧠 Detection Engines**: Heuristic-based detection (default) with optional MediaPipe support
- **💾 Data Persistence**: SQLite database with migration support
- **📤 Export/Import**: CSV export and import functionality
- **🔒 Privacy-First**: All data stored locally, optional telemetry
- **⚡ Performance**: Optimized for real-time detection with minimal resource usage

## 🚀 Quick Start

### Pre-built Binaries

Download the latest release from the [GitHub Releases](https://github.com/VoxHash/Count-Cups/releases) page:

- **Windows**: `Count-Cups.exe` (standalone executable)
- **macOS**: `Count-Cups.dmg` (disk image)
- **Linux**: `count-cups` (AppImage or DEB package)

### From Source

```bash
# Clone the repository
git clone https://github.com/VoxHash/Count-Cups.git
cd Count-Cups

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m app.main
```

## 📸 Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)
*Overview of your daily hydration progress with quick actions*

### Live Camera
![Live Camera](docs/screenshots/live_camera.png)
*Real-time detection with visual feedback*

### History & Analytics
![History](docs/screenshots/history.png)
*Detailed analytics and trend analysis*

### Calibration
![Calibration](docs/screenshots/calibration.png)
*Set up cup profiles and fine-tune detection*

## 🛠️ Installation

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

### Windows Installation

1. Download `Count-Cups.exe` from the [releases page](https://github.com/VoxHash/Count-Cups/releases)
2. Run the executable (no installation required)
3. Allow camera access when prompted
4. Start tracking your hydration!

### macOS Installation

1. Download `Count-Cups.dmg` from the [releases page](https://github.com/VoxHash/Count-Cups/releases)
2. Open the DMG file and drag Count-Cups to Applications
3. Launch from Applications folder
4. Grant camera permissions when requested

### Linux Installation

#### AppImage (Recommended)
1. Download `Count-Cups-x86_64.AppImage` from the [releases page](https://github.com/VoxHash/Count-Cups/releases)
2. Make executable: `chmod +x Count-Cups-x86_64.AppImage`
3. Run: `./Count-Cups-x86_64.AppImage`

#### DEB Package
1. Download `count-cups_1.0.0_amd64.deb` from the [releases page](https://github.com/VoxHash/Count-Cups/releases)
2. Install: `sudo dpkg -i count-cups_1.0.0_amd64.deb`
3. Run: `count-cups`

## 📖 Usage

### First-Time Setup

1. **Launch Count-Cups** and allow camera access when prompted
2. **Set up your first cup profile** in the Calibration screen
3. **Configure your daily goal** in Settings
4. **Start tracking** by going to the Live Camera screen
5. **View your progress** on the Dashboard

### Daily Usage

1. **Position yourself** in front of the camera
2. **Start detection** in the Live Camera screen
3. **Drink normally** - the app will automatically detect sips
4. **Monitor progress** on the Dashboard
5. **Add manual entries** if needed

### Tips for Best Results

- **Good Lighting**: Ensure your face is well-lit
- **Camera Position**: Position camera at eye level
- **Cup Visibility**: Keep your cup visible to the camera
- **Calibration**: Use the Calibration screen to fine-tune detection
- **Regular Use**: Consistent usage improves detection accuracy

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root to customize settings (copy from `.env.example`):

```env
# Detection Settings
DETECTION_ENGINE=heuristics
HEAD_TILT_THRESHOLD=25.0
HAND_FACE_DISTANCE_THRESHOLD=100.0

# Calibration
DEFAULT_CUP_SIZE_ML=250
DEFAULT_SIPS_PER_CUP=10

# Notifications
ENABLE_NOTIFICATIONS=true
GOAL_REMINDER_HOUR=20

# UI Settings
DEFAULT_THEME=auto
WINDOW_WIDTH=1200
WINDOW_HEIGHT=800
```

### Settings Screen

Access the Settings screen to configure:

- **General**: Theme, window behavior, system tray
- **Detection**: Engine selection, sensitivity parameters
- **Camera**: Camera selection, resolution, frame rate
- **Notifications**: Goal reminders, notification preferences
- **Advanced**: Database settings, logging, telemetry

## 🔧 Development

### Setting Up Development Environment

```bash
# Clone and setup
git clone https://github.com/VoxHash/Count-Cups.git
cd Count-Cups
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run in development mode
./scripts/dev_run.sh  # Linux/macOS
.\scripts\dev_run.ps1  # Windows

# Run tests
pytest tests/ -v

# Run linting
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

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=app --cov-report=html

# Run specific test file
pytest tests/test_sip_logic.py -v

# Run linting
ruff check .
ruff format --check .
mypy app/
```

## 📚 Documentation

- **[User Guide](docs/README.md)**: Comprehensive user documentation
- **[Architecture](docs/ARCHITECTURE.md)**: Technical architecture overview
- **[API Reference](docs/API.md)**: API documentation for developers
- **[Contributing](CONTRIBUTING.md)**: Guidelines for contributing

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Common Issues

#### Camera Not Detected
- Check camera permissions
- Try different camera index in Settings
- Ensure camera is not in use by other applications
- Update camera drivers

#### Poor Detection Accuracy
- Improve lighting conditions
- Adjust camera position
- Use the Calibration screen to fine-tune settings
- Try switching between detection engines

#### Application Crashes
- Check logs in `~/.count-cups/logs/`
- Update dependencies
- Reset settings in Advanced tab
- Report issue on GitHub

### Getting Help

1. Check the [documentation](docs/README.md)
2. Search [existing issues](https://github.com/VoxHash/Count-Cups/issues)
3. Create a [new issue](https://github.com/VoxHash/Count-Cups/issues/new)
4. Join [discussions](https://github.com/VoxHash/Count-Cups/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenCV** for computer vision capabilities
- **PyQt6** for the modern user interface
- **MediaPipe** for advanced pose detection (optional)
- **SQLite** for local data storage
- **Nuitka** for cross-platform compilation

## 📊 Project Status

- **Version**: 1.0.0
- **Status**: Active Development
- **Python Support**: 3.10+
- **Platforms**: Windows, macOS, Linux
- **License**: MIT

---

**Count-Cups** - Stay hydrated, stay healthy! 💧

Made with ❤️ by [VoxHash](https://github.com/VoxHash)