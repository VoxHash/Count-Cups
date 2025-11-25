# Quick Start Guide

Get Count-Cups up and running in minutes!

## Installation

### Pre-built Binary (Recommended)

1. Download the latest release from [GitHub Releases](https://github.com/VoxHash/Count-Cups/releases)
2. Run the executable:
   - **Windows**: `Count-Cups.exe`
   - **macOS**: Open `Count-Cups.dmg` and drag to Applications
   - **Linux**: `chmod +x Count-Cups-x86_64.AppImage && ./Count-Cups-x86_64.AppImage`

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

## First Steps

1. **Launch Count-Cups** and allow camera access when prompted
2. **Set up your first cup profile**:
   - Go to Calibration screen
   - Enter cup name (e.g., "Coffee Mug")
   - Set cup size in milliliters (e.g., 250ml)
   - Set sips per cup (e.g., 10)
   - Click "Save Settings"
3. **Configure your daily goal**:
   - Go to Settings screen
   - Set your daily water intake goal (e.g., 2000ml)
4. **Start tracking**:
   - Go to Live Camera screen
   - Click "Start Detection"
   - Position yourself in front of the camera
   - Drink normally - sips will be detected automatically
5. **View your progress**:
   - Check the Dashboard for daily statistics
   - View History for analytics and trends

## Tips for Best Results

- **Good Lighting**: Ensure your face is well-lit
- **Camera Position**: Position camera at eye level
- **Cup Visibility**: Keep your cup visible to the camera
- **Calibration**: Use the Calibration screen to fine-tune detection
- **Consistent Use**: Regular usage improves detection accuracy

## Next Steps

- Read the [Getting Started Guide](getting-started.md) for detailed setup
- Check the [Usage Guide](usage.md) for advanced features
- Review [Configuration](configuration.md) for customization options
- See [Troubleshooting](troubleshooting.md) if you encounter issues

---

**Ready to dive deeper?** Continue to the [Getting Started Guide](getting-started.md) or [Usage Guide](usage.md).

