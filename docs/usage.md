# Usage Guide

Complete guide to using Count-Cups effectively.

## Overview

Count-Cups provides several screens and features for tracking your hydration:

- **Dashboard**: Overview of daily progress
- **Live Camera**: Real-time sip detection
- **History**: Historical data and analytics
- **Calibration**: Cup profile setup and testing
- **Settings**: Application configuration

## Dashboard

The Dashboard provides an overview of your daily hydration progress.

### Features

- **Today's Intake**: Total milliliters, cups, and sips consumed
- **Goal Progress**: Visual progress bar and percentage
- **Quick Actions**: Manual sip/cup entry buttons
- **Recent Activity**: List of recent sip events

### Using the Dashboard

1. **View Progress**: Check your daily intake and goal progress
2. **Quick Entry**: Use "Add Sip" or "Add Cup" buttons for manual entry
3. **Navigate**: Click screen buttons to access other screens

## Live Camera

The Live Camera screen shows real-time detection with visual feedback.

### Features

- **Camera Feed**: Live video from your webcam
- **Detection Overlay**: Visual indicators for face and hand detection
- **Controls**: Start/stop detection, calibration tools
- **Status**: Detection status and confidence levels

### Using Live Camera

1. **Start Detection**: Click "Start Detection" button
2. **Position Yourself**: Sit in front of the camera at normal distance
3. **Drink Normally**: Make natural drinking motions
4. **Observe Feedback**: Watch for detection indicators and sip count
5. **Stop Detection**: Click "Stop Detection" when finished

### Detection Indicators

- **Green Circles**: Hand detection working
- **Blue Rectangles**: Face detection working
- **Yellow Lines**: Hand-to-face distance measurement
- **Confidence Values**: Detection confidence percentage

## History

View your hydration history and analytics over time.

### Features

- **Daily Stats**: Day-by-day breakdown of your intake
- **Weekly/Monthly Views**: Longer-term trends and patterns
- **Export Options**: CSV export for external analysis
- **Goal Achievement**: Track your consistency and goal completion

### Using History

1. **View Daily Stats**: See your intake for each day
2. **Switch Views**: Toggle between daily, weekly, and monthly views
3. **Export Data**: Click "Export" to save data as CSV
4. **Analyze Trends**: Review patterns in your hydration habits

## Calibration

Set up and manage cup profiles for accurate tracking.

### Features

- **Cup Profiles**: Define different cup sizes and types
- **Detection Parameters**: Fine-tune detection sensitivity
- **Test Mode**: Validate your calibration settings
- **Multiple Profiles**: Support for different drinking vessels

### Using Calibration

1. **Create Profile**: Enter cup name, size, and sips per cup
2. **Set Default**: Mark profile as default if it's your primary cup
3. **Test Detection**: Use test mode to validate settings
4. **Adjust Parameters**: Fine-tune detection sensitivity as needed
5. **Save Settings**: Save your calibration configuration

See [Calibration Guide](CALIBRATION.md) for detailed calibration instructions.

## Settings

Configure application behavior and preferences.

### General Tab

- **Theme**: Choose Light, Dark, Dracula, or Auto
- **Window Behavior**: Configure window size and state
- **System Tray**: Enable/disable system tray integration

### Detection Tab

- **Engine Selection**: Choose between Heuristics and MediaPipe
- **Sensitivity**: Adjust detection sensitivity parameters
- **Thresholds**: Configure head tilt and hand distance thresholds

### Camera Tab

- **Device Selection**: Choose which camera to use
- **Resolution**: Set camera resolution
- **Frame Rate**: Configure detection frame rate

### Notifications Tab

- **Enable Notifications**: Toggle desktop notifications
- **Goal Reminders**: Configure reminder times
- **Achievement Alerts**: Enable achievement notifications

### Advanced Tab

- **Database**: Database location and backup options
- **Logging**: Log level and file management
- **Telemetry**: Anonymous usage statistics (opt-in)
- **Reset**: Reset all settings to defaults

## Manual Entry

Add sips or cups manually when automatic detection isn't available.

### Adding a Sip

1. Go to Dashboard
2. Click "Add Sip" button
3. Sip is added to your daily intake

### Adding a Cup

1. Go to Dashboard
2. Click "Add Cup" button
3. Select cup profile
4. Cup is added to your daily intake

## Daily Workflow

### Morning Routine

1. **Launch Count-Cups**: Start the application
2. **Check Dashboard**: Review yesterday's progress
3. **Set Today's Goal**: Adjust goal if needed
4. **Start Detection**: Begin tracking for the day

### During the Day

1. **Keep Detection Running**: Leave Live Camera running
2. **Monitor Progress**: Check Dashboard periodically
3. **Manual Entry**: Add missed sips manually if needed
4. **Adjust Settings**: Fine-tune detection if accuracy is poor

### Evening Routine

1. **Review Statistics**: Check History for daily summary
2. **Export Data**: Export data if needed
3. **Plan Tomorrow**: Set goals for next day
4. **Close Application**: Application saves data automatically

## Tips for Best Results

### Environment

- **Consistent Lighting**: Use the same lighting conditions daily
- **Stable Camera**: Mount camera or use a stable surface
- **Clean Background**: Minimize distractions behind you
- **Comfortable Position**: Sit in a comfortable, repeatable position

### Detection

- **Good Lighting**: Ensure your face and hands are well-lit
- **Camera Position**: Position camera at eye level
- **Cup Visibility**: Keep your cup visible to the camera
- **Natural Gestures**: Use natural drinking motions

### Accuracy

- **Calibration**: Regularly calibrate for best accuracy
- **Regular Use**: Consistent usage improves detection
- **Manual Backup**: Use manual entry when detection isn't available
- **Review Data**: Regularly review your hydration patterns

## Keyboard Shortcuts

- **Ctrl+Q** (Cmd+Q on macOS): Quit application
- **Ctrl+S** (Cmd+S on macOS): Save settings
- **Ctrl+D**: Open Dashboard
- **Ctrl+L**: Open Live Camera
- **Ctrl+H**: Open History
- **Ctrl+C**: Open Calibration
- **Ctrl+,**: Open Settings

## Troubleshooting

If you encounter issues:

1. **Check [Troubleshooting Guide](troubleshooting.md)** for common problems
2. **Review [FAQ](faq.md)** for answers to questions
3. **Check Logs**: Review logs in `~/.count-cups/logs/`
4. **Get Support**: Visit [SUPPORT.md](../SUPPORT.md) for help

## Next Steps

- **Advanced Features**: Explore advanced features in [Configuration](configuration.md)
- **CLI Usage**: Learn command-line options in [CLI Reference](cli.md)
- **Development**: See [API Reference](api.md) for development
- **Examples**: Check [Examples](examples/) for code samples

---

**Happy tracking!** Use Count-Cups regularly to maintain healthy hydration habits.

