# Frequently Asked Questions (FAQ)

Common questions and answers about Count-Cups.

## General Questions

### What is Count-Cups?

Count-Cups is a cross-platform water intake tracker that uses computer vision to automatically detect and count your drinking gestures. It helps you stay hydrated by tracking your daily water consumption.

### How does Count-Cups work?

Count-Cups uses computer vision (OpenCV and optionally MediaPipe) to detect drinking gestures from your webcam. It analyzes face and hand positions to identify when you're drinking and automatically counts sips.

### Is Count-Cups free?

Yes, Count-Cups is free and open source under the MIT License.

### What platforms are supported?

Count-Cups supports Windows, macOS, and Linux.

### Do I need a camera?

Yes, Count-Cups requires a camera for automatic sip detection. You can also manually enter sips if detection isn't available.

## Installation Questions

### How do I install Count-Cups?

See the [Installation Guide](installation.md) for detailed instructions. You can either download pre-built binaries or install from source.

### What are the system requirements?

**Minimum**: Windows 10/macOS 10.14/Linux (Ubuntu 18.04+), Python 3.10+, 4GB RAM, 100MB storage, camera

**Recommended**: Windows 11/macOS 12+/Linux (Ubuntu 20.04+), Python 3.11+, 8GB RAM, 500MB storage, HD webcam

### Do I need Python installed?

Only if installing from source. Pre-built binaries don't require Python.

### Can I install on multiple devices?

Yes, you can install Count-Cups on multiple devices. Data is stored locally on each device.

## Usage Questions

### How accurate is the detection?

Detection accuracy depends on lighting, camera position, and calibration. With proper setup, accuracy is typically 80-90%. You can manually add missed sips.

### Can I use multiple cup types?

Yes, you can create multiple cup profiles with different sizes and types. Switch between profiles as needed.

### How do I set my daily goal?

Go to Settings and set your daily water intake goal in milliliters. The default is typically 2000ml (8 cups).

### Can I track other beverages?

Yes, you can track any beverage. Create cup profiles for different beverages and Count-Cups will track them all.

### Does Count-Cups work in the background?

Count-Cups needs to be running for detection. You can minimize to system tray on supported platforms.

## Privacy Questions

### Is my data private?

Yes, all data is stored locally on your device. No data is transmitted to external servers unless you explicitly enable telemetry (opt-in).

### Does Count-Cups record video?

No, Count-Cups does not record or store video. All processing happens in real-time and video frames are discarded immediately.

### What data is collected?

With telemetry disabled (default), no data is collected. If telemetry is enabled, only anonymous usage statistics are collected (no personal or hydration data).

### Can I export my data?

Yes, you can export your data to CSV format from the History screen or Settings.

## Technical Questions

### What detection engines are available?

- **Heuristics**: Fast, default engine using OpenCV
- **MediaPipe**: More accurate, requires MediaPipe installation

### Can I customize detection sensitivity?

Yes, you can adjust detection parameters in the Calibration screen and Settings.

### How do I update Count-Cups?

**Pre-built binaries**: Download the latest release and replace the executable.

**From source**: `git pull origin main && pip install -r requirements.txt --upgrade`

### Can I contribute to Count-Cups?

Yes! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Troubleshooting Questions

### Camera not detected?

See [Troubleshooting Guide](troubleshooting.md) for solutions. Common fixes: check permissions, try different camera index, update drivers.

### Poor detection accuracy?

Improve lighting, adjust camera position, calibrate settings, try different detection engine.

### Application crashes?

Check logs in `~/.count-cups/logs/`, update dependencies, reset settings, report issue with log details.

### Performance issues?

Reduce camera resolution, close other applications, use heuristics engine, update graphics drivers.

## Feature Questions

### Can I set different goals for different days?

This feature is planned for version 1.1. Currently, you can set one daily goal.

### Can I sync data across devices?

This feature is planned for version 1.3. Currently, data is stored locally on each device.

### Can I export to health apps?

CSV export is available. Integration with health apps (Apple Health, Google Fit) is planned for future versions.

### Are there mobile apps?

Mobile apps are planned for future versions. Currently, Count-Cups is desktop-only.

## Support Questions

### Where can I get help?

- **Documentation**: Check the [documentation](index.md)
- **Troubleshooting**: See [Troubleshooting Guide](troubleshooting.md)
- **GitHub Issues**: [Create an issue](https://github.com/VoxHash/Count-Cups/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/VoxHash/Count-Cups/discussions)
- **Email**: contact@voxhash.dev

### How do I report a bug?

Create an issue on GitHub with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment information
- Log files

See [SUPPORT.md](../SUPPORT.md) for more details.

### How do I request a feature?

Create a feature request issue on GitHub with:
- Description of the feature
- Use case
- Proposed solution
- Alternatives considered

## Next Steps

- **Documentation**: Browse the [documentation index](index.md)
- **Troubleshooting**: Check [Troubleshooting Guide](troubleshooting.md)
- **Support**: Visit [SUPPORT.md](../SUPPORT.md)

---

**Have a question not answered here?** Create an issue on GitHub or contact us at contact@voxhash.dev.

