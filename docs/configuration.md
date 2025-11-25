# Configuration Guide

Complete guide to configuring Count-Cups to suit your needs.

## Configuration Methods

Count-Cups can be configured through:

1. **Environment Variables** (`.env` file)
2. **Settings Screen** (GUI)
3. **Command-Line Arguments** (CLI)

## Environment Variables

Create a `.env` file in the project root to customize settings:

```env
# Application Settings
APP_NAME=Count-Cups
APP_VERSION=1.0.0
DEBUG=false
LOG_LEVEL=INFO

# Database
DATABASE_URL=sqlite:///count_cups.db

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

# Telemetry
ENABLE_TELEMETRY=false
TELEMETRY_ENDPOINT=

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

## Settings Screen

Access the Settings screen from the main menu to configure:

### General Tab

- **Theme**: Auto, Light, Dark, Dracula
- **Window Behavior**: Width, height, maximized state
- **System Tray**: Enable/disable system tray integration
- **Start on Boot**: Launch on system startup

### Detection Tab

- **Detection Engine**: Heuristics or MediaPipe
- **Sip Duration**: Minimum and maximum sip duration
- **Head Tilt Threshold**: Sensitivity for head tilt detection
- **Hand-Face Distance**: Threshold for hand proximity to face
- **Confidence Threshold**: Minimum confidence for detection

### Camera Tab

- **Camera Selection**: Choose camera device
- **Resolution**: Camera resolution (320x240 to 1920x1080)
- **Frame Rate**: Detection frame rate (15-60 FPS)
- **Auto Focus**: Enable/disable auto focus

### Notifications Tab

- **Enable Notifications**: Toggle desktop notifications
- **Goal Reminders**: Enable goal reminder notifications
- **Reminder Time**: Hour and minute for daily reminders
- **Achievement Notifications**: Notify on goal achievements

### Advanced Tab

- **Database Settings**: Database location and backup
- **Logging**: Log level and file location
- **Telemetry**: Enable/disable anonymous telemetry
- **Reset Settings**: Reset all settings to defaults

## Command-Line Arguments

Run Count-Cups with command-line arguments:

```bash
python -m app.main [OPTIONS]
```

### Available Options

- `--debug`: Enable debug mode
- `--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}`: Set log level
- `--theme {auto,light,dark,dracula}`: Set theme
- `--detection-engine {heuristics,mediapipe}`: Set detection engine
- `--camera-index INTEGER`: Camera index to use
- `--no-camera`: Run without camera (for testing)
- `--version`: Show version and exit

### Examples

```bash
# Run with debug mode
python -m app.main --debug

# Run with dark theme
python -m app.main --theme dark

# Run with MediaPipe detection
python -m app.main --detection-engine mediapipe

# Run with specific camera
python -m app.main --camera-index 1
```

## Configuration Reference

### Application Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `APP_NAME` | string | `Count-Cups` | Application name |
| `APP_VERSION` | string | `1.0.0` | Application version |
| `DEBUG` | boolean | `false` | Enable debug mode |
| `LOG_LEVEL` | string | `INFO` | Logging level |

### Detection Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `DETECTION_ENGINE` | string | `heuristics` | Detection engine (heuristics/mediapipe) |
| `SIP_DURATION_MIN` | float | `0.8` | Minimum sip duration (seconds) |
| `SIP_DURATION_MAX` | float | `3.5` | Maximum sip duration (seconds) |
| `HEAD_TILT_THRESHOLD` | float | `25.0` | Head tilt threshold (degrees) |
| `HAND_FACE_DISTANCE_THRESHOLD` | float | `100.0` | Hand-face distance threshold (pixels) |

### Calibration Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `DEFAULT_CUP_SIZE_ML` | integer | `250` | Default cup size (milliliters) |
| `DEFAULT_SIPS_PER_CUP` | integer | `10` | Default sips per cup |

### Notification Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `ENABLE_NOTIFICATIONS` | boolean | `true` | Enable desktop notifications |
| `GOAL_REMINDER_HOUR` | integer | `20` | Goal reminder hour (0-23) |
| `GOAL_REMINDER_MINUTE` | integer | `0` | Goal reminder minute (0-59) |

### UI Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `DEFAULT_THEME` | string | `auto` | Default theme (auto/light/dark/dracula) |
| `WINDOW_WIDTH` | integer | `1200` | Window width (pixels) |
| `WINDOW_HEIGHT` | integer | `800` | Window height (pixels) |
| `WINDOW_MAXIMIZED` | boolean | `false` | Start maximized |

### Camera Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `CAMERA_INDEX` | integer | `0` | Camera device index |
| `CAMERA_WIDTH` | integer | `640` | Camera width (pixels) |
| `CAMERA_HEIGHT` | integer | `480` | Camera height (pixels) |
| `CAMERA_FPS` | integer | `30` | Camera frame rate (FPS) |

## Best Practices

### Detection Configuration

- **Start with defaults**: Use default settings initially
- **Calibrate gradually**: Adjust settings incrementally
- **Test changes**: Test detection after each change
- **Document settings**: Note what works for your setup

### Performance Optimization

- **Lower resolution**: Reduce camera resolution for better performance
- **Adjust frame rate**: Lower frame rate for less CPU usage
- **Choose engine**: Use heuristics for speed, MediaPipe for accuracy

### Privacy Settings

- **Disable telemetry**: Set `ENABLE_TELEMETRY=false` for privacy
- **Local storage**: All data stored locally by default
- **No cloud sync**: No data transmitted without explicit opt-in

## Configuration Files Location

- **Settings**: `~/.count-cups/data/settings.json`
- **Database**: `~/.count-cups/data/count_cups.db`
- **Logs**: `~/.count-cups/logs/`
- **Environment**: `.env` (project root)

## Resetting Configuration

### Reset All Settings

1. Go to Settings > Advanced
2. Click "Reset All Settings"
3. Confirm reset

### Manual Reset

1. Close Count-Cups
2. Delete `~/.count-cups/data/settings.json`
3. Restart Count-Cups (defaults will be restored)

## Next Steps

- Learn about [Usage](usage.md) for using configured features
- Check [CLI Reference](cli.md) for command-line options
- See [Troubleshooting](troubleshooting.md) if configuration issues occur

---

**Configuration complete!** Your Count-Cups is now customized to your preferences.

