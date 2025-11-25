# Installation Guide

Complete installation instructions for Count-Cups on all supported platforms.

## System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **Python**: 3.10+ (for source installation)
- **RAM**: 4GB
- **Storage**: 100MB
- **Camera**: USB webcam or built-in camera

### Recommended Requirements
- **OS**: Windows 11, macOS 12+, or Linux (Ubuntu 20.04+)
- **Python**: 3.11+ (for source installation)
- **RAM**: 8GB
- **Storage**: 500MB
- **Camera**: HD webcam with good lighting

## Installation Methods

### Method 1: Pre-built Binaries (Recommended)

Download the latest release from the [GitHub Releases](https://github.com/VoxHash/Count-Cups/releases) page.

#### Windows

1. Download `Count-Cups.exe` from the releases page
2. Run the executable (no installation required)
3. Allow camera access when prompted
4. Start tracking your hydration!

#### macOS

1. Download `Count-Cups.dmg` from the releases page
2. Open the DMG file and drag Count-Cups to Applications
3. Launch from Applications folder
4. Grant camera permissions when requested

#### Linux

##### AppImage (Recommended)

1. Download `Count-Cups-x86_64.AppImage` from the releases page
2. Make executable: `chmod +x Count-Cups-x86_64.AppImage`
3. Run: `./Count-Cups-x86_64.AppImage`

##### DEB Package

1. Download `count-cups_1.0.0_amd64.deb` from the releases page
2. Install: `sudo dpkg -i count-cups_1.0.0_amd64.deb`
3. Run: `count-cups`

### Method 2: From Source

#### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git (for cloning the repository)

#### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/VoxHash/Count-Cups.git
   cd Count-Cups
   ```

2. **Create virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python -m app.main
   ```

#### Development Installation

For development, also install development dependencies:

```bash
pip install -r requirements-dev.txt
```

## Post-Installation

### First Launch

1. **Camera Permissions**: Grant camera access when prompted
2. **Initial Setup**: Follow the first-time setup wizard
3. **Calibration**: Set up your first cup profile
4. **Goal Setting**: Configure your daily hydration goal

### Verification

1. **Check Installation**: Launch Count-Cups and verify it starts
2. **Test Camera**: Go to Live Camera screen and verify camera feed
3. **Test Detection**: Try a test detection to ensure everything works

## Troubleshooting Installation

### Python Not Found

**Windows**: Add Python to PATH or use full path to Python executable
**macOS/Linux**: Install Python 3.10+ using package manager

### Dependencies Installation Fails

- **Update pip**: `python -m pip install --upgrade pip`
- **Use virtual environment**: Ensure you're in a virtual environment
- **Check Python version**: Ensure Python 3.10+ is installed

### Camera Not Detected

- **Check permissions**: Ensure camera permissions are granted
- **Test camera**: Test camera with another application
- **Update drivers**: Update camera drivers (Windows)

### Import Errors

- **Reinstall dependencies**: `pip install -r requirements.txt --force-reinstall`
- **Check virtual environment**: Ensure virtual environment is activated
- **Python version**: Verify Python version is 3.10+

## Uninstallation

### Pre-built Binaries

#### Windows
- Delete `Count-Cups.exe`
- Remove data directory: `%USERPROFILE%\.count-cups`

#### macOS
- Delete from Applications folder
- Remove data directory: `~/.count-cups`

#### Linux
- Delete AppImage or uninstall package: `sudo dpkg -r count-cups`
- Remove data directory: `~/.count-cups`

### From Source

1. **Deactivate virtual environment**: `deactivate`
2. **Remove virtual environment**: Delete `venv` directory
3. **Remove repository**: Delete cloned repository
4. **Remove data**: Delete `~/.count-cups` directory

## Updating

### Pre-built Binaries

1. Download the latest release
2. Replace the old executable/package
3. Launch the new version (settings are preserved)

### From Source

1. **Pull latest changes**:
   ```bash
   git pull origin main
   ```

2. **Update dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Restart application**

## Platform-Specific Notes

### Windows

- **Antivirus**: Some antivirus software may flag the executable; add exception if needed
- **Firewall**: No firewall rules required (local application)
- **Administrator Rights**: Not required for normal operation

### macOS

- **Gatekeeper**: May require allowing the app in Security & Privacy settings
- **Camera Permissions**: Grant in System Preferences > Security & Privacy > Camera
- **Code Signing**: Pre-built binaries are code-signed

### Linux

- **AppImage**: May require `libfuse2` for older distributions
- **Dependencies**: Some distributions may require additional libraries
- **Permissions**: Ensure user has camera access permissions

## Next Steps

After installation:

1. Read the [Quick Start Guide](quick-start.md)
2. Follow the [Getting Started Guide](getting-started.md)
3. Configure settings in [Configuration Guide](configuration.md)
4. Learn usage in [Usage Guide](usage.md)

---

**Installation complete!** Continue to the [Quick Start Guide](quick-start.md) to begin using Count-Cups.

