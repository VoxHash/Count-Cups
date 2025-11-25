# CLI Reference

Command-line interface reference for Count-Cups.

## Overview

Count-Cups can be run from the command line with various options to customize behavior.

## Basic Usage

```bash
python -m app.main [OPTIONS]
```

## Command-Line Options

### `--debug`

Enable debug mode with verbose logging.

```bash
python -m app.main --debug
```

**Effect**: Sets log level to DEBUG and enables debug mode.

### `--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}`

Set the logging level.

```bash
python -m app.main --log-level DEBUG
```

**Default**: `INFO`

**Options**:
- `DEBUG`: Detailed debugging information
- `INFO`: General informational messages
- `WARNING`: Warning messages
- `ERROR`: Error messages only
- `CRITICAL`: Critical errors only

### `--theme {auto,light,dark,dracula}`

Set the application theme.

```bash
python -m app.main --theme dark
```

**Default**: `auto`

**Options**:
- `auto`: Auto-detect system theme
- `light`: Light theme
- `dark`: Dark theme
- `dracula`: Dracula theme

### `--detection-engine {heuristics,mediapipe}`

Set the detection engine.

```bash
python -m app.main --detection-engine mediapipe
```

**Default**: `heuristics`

**Options**:
- `heuristics`: Fast heuristic-based detection (default)
- `mediapipe`: Advanced MediaPipe-based detection (requires MediaPipe)

### `--camera-index INTEGER`

Specify which camera device to use.

```bash
python -m app.main --camera-index 1
```

**Default**: `0`

**Note**: Use `0` for default camera, `1` for second camera, etc.

### `--no-camera`

Run without camera (for testing).

```bash
python -m app.main --no-camera
```

**Use Case**: Testing without camera access or running in headless mode.

### `--version`

Show version information and exit.

```bash
python -m app.main --version
```

**Output**: `Count-Cups 1.0.0`

## Examples

### Basic Launch

```bash
python -m app.main
```

### Debug Mode

```bash
python -m app.main --debug
```

### Custom Theme and Detection

```bash
python -m app.main --theme dark --detection-engine mediapipe
```

### Specific Camera with Debug

```bash
python -m app.main --camera-index 1 --debug --log-level DEBUG
```

### Testing Without Camera

```bash
python -m app.main --no-camera --debug
```

## Environment Variables

Command-line arguments can be overridden by environment variables. See [Configuration Guide](configuration.md) for details.

## Exit Codes

- `0`: Success
- `1`: Error (missing dependencies, fatal error)

## Integration Examples

### Shell Script

```bash
#!/bin/bash
# Launch Count-Cups with custom settings

python -m app.main \
    --theme dark \
    --detection-engine heuristics \
    --camera-index 0 \
    --log-level INFO
```

### PowerShell Script

```powershell
# Launch Count-Cups with custom settings

python -m app.main `
    --theme dark `
    --detection-engine heuristics `
    --camera-index 0 `
    --log-level INFO
```

### Batch File (Windows)

```batch
@echo off
REM Launch Count-Cups with custom settings

python -m app.main ^
    --theme dark ^
    --detection-engine heuristics ^
    --camera-index 0 ^
    --log-level INFO
```

## Troubleshooting

### Command Not Found

**Issue**: `python: command not found`

**Solution**: 
- Use `python3` instead of `python`
- Add Python to PATH
- Use full path to Python executable

### Module Not Found

**Issue**: `ModuleNotFoundError: No module named 'app'`

**Solution**:
- Ensure you're in the project root directory
- Activate virtual environment
- Install dependencies: `pip install -r requirements.txt`

### Camera Not Found

**Issue**: Camera not detected

**Solution**:
- Check camera permissions
- Try different camera index: `--camera-index 1`
- Verify camera is not in use by other applications

## Next Steps

- **Configuration**: See [Configuration Guide](configuration.md) for settings
- **Usage**: Check [Usage Guide](usage.md) for application usage
- **API**: See [API Reference](api.md) for programmatic access

---

**CLI Reference complete!** Use command-line options to customize Count-Cups behavior.

