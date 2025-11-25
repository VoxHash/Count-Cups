# Getting Started Guide

Complete guide for first-time users of Count-Cups.

## Prerequisites

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

## Installation

See [Installation Guide](installation.md) for detailed installation instructions.

## First-Time Setup

### 1. Launch Count-Cups

- **Windows**: Double-click `Count-Cups.exe`
- **macOS**: Open from Applications folder
- **Linux**: Run `./Count-Cups-x86_64.AppImage` or `count-cups`

### 2. Camera Setup

1. **Grant Camera Permissions**: Allow camera access when prompted
2. **Test Camera**: Go to Live Camera screen and verify camera feed
3. **Adjust Position**: Position camera at eye level, facing you
4. **Check Lighting**: Ensure good lighting on your face

### 3. Create Your First Cup Profile

1. **Navigate to Calibration**: Click "Calibration" in the main menu
2. **Fill in Cup Details**:
   - **Name**: Descriptive name (e.g., "Coffee Mug", "Water Bottle")
   - **Size**: Volume in milliliters (e.g., 250ml, 500ml)
   - **Sips per Cup**: Average number of sips to finish (e.g., 10)
3. **Set as Default**: Check "Default" if this is your primary cup
4. **Save Profile**: Click "Save Settings"

### 4. Configure Daily Goal

1. **Navigate to Settings**: Click "Settings" in the main menu
2. **Set Daily Goal**: Enter your daily water intake goal (e.g., 2000ml)
3. **Save Settings**: Click "Save Settings"

### 5. Test Detection

1. **Go to Live Camera**: Click "Live Camera" in the main menu
2. **Start Detection**: Click "Start Detection" button
3. **Position Yourself**: Sit in front of the camera
4. **Test Drinking**: Make a drinking motion with your cup
5. **Observe Detection**: Watch for detection indicators and sip count
6. **Stop Detection**: Click "Stop Detection" when finished

## Daily Usage

### Starting Your Day

1. **Launch Count-Cups**: Start the application
2. **Check Dashboard**: View your daily progress
3. **Start Detection**: Go to Live Camera and start detection
4. **Drink Normally**: The app will automatically detect sips

### During the Day

1. **Monitor Progress**: Check Dashboard regularly
2. **Manual Entry**: Add sips manually if detection misses any
3. **Adjust Settings**: Fine-tune detection if needed

### End of Day

1. **Review Statistics**: Check History for daily summary
2. **Export Data**: Export data if needed (Settings > Export)
3. **Close Application**: Application will save data automatically

## Understanding the Interface

### Dashboard

- **Today's Intake**: Total milliliters, cups, and sips
- **Goal Progress**: Visual progress bar and percentage
- **Quick Actions**: Manual sip/cup entry buttons
- **Recent Activity**: List of recent sip events

### Live Camera

- **Camera Feed**: Live video from your webcam
- **Detection Overlay**: Visual indicators for face and hand detection
- **Controls**: Start/stop detection, calibration tools
- **Status**: Detection status and confidence levels

### History

- **Daily Stats**: Day-by-day breakdown
- **Weekly/Monthly Views**: Longer-term trends
- **Export Options**: CSV export for external analysis
- **Goal Achievement**: Track your consistency

### Calibration

- **Cup Profiles**: Manage different cup sizes and types
- **Detection Parameters**: Fine-tune detection sensitivity
- **Test Mode**: Validate your calibration settings

### Settings

- **General**: Theme, window behavior, system tray
- **Detection**: Engine selection, sensitivity parameters
- **Camera**: Device selection, resolution, frame rate
- **Notifications**: Goal reminders, notification preferences
- **Advanced**: Database settings, logging, telemetry

## Tips for Success

### Environment Setup

- **Consistent Lighting**: Use the same lighting conditions daily
- **Stable Camera**: Mount camera or use a stable surface
- **Clean Background**: Minimize distractions behind you
- **Comfortable Position**: Sit in a comfortable, repeatable position

### Detection Optimization

- **Good Lighting**: Ensure your face and hands are well-lit
- **Camera Position**: Position camera at eye level
- **Cup Visibility**: Keep your cup visible to the camera
- **Calibration**: Regularly calibrate for best accuracy

### Best Practices

- **Regular Use**: Consistent usage improves detection accuracy
- **Manual Backup**: Use manual entry when detection isn't available
- **Review Data**: Regularly review your hydration patterns
- **Adjust Goals**: Update goals based on your actual needs

## Troubleshooting

If you encounter issues:

1. **Check [Troubleshooting Guide](troubleshooting.md)** for common problems
2. **Review [FAQ](faq.md)** for answers to common questions
3. **Check Logs**: Review logs in `~/.count-cups/logs/`
4. **Get Support**: Visit [SUPPORT.md](../SUPPORT.md) for help

## Next Steps

- **Learn More**: Read the [Usage Guide](usage.md) for advanced features
- **Customize**: Check [Configuration](configuration.md) for settings
- **Develop**: See [API Reference](api.md) for development
- **Examples**: Explore [Examples](examples/) for code samples

---

**Congratulations!** You're now ready to start tracking your hydration with Count-Cups. Happy hydrating! 💧

