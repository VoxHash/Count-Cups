# Count-Cups 💧

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/VoxHash/Count-Cups)

> A cross-platform water intake tracker that uses computer vision to automatically detect and count your drinking gestures. Stay hydrated with intelligent sip detection and comprehensive tracking features.

## ✨ Features

- **🤖 Automatic Sip Detection**: Computer vision-based detection from your webcam
- **✋ Manual Entry**: Quick-add sips or cups when automatic detection isn't available
- **📊 Daily Goal Tracking**: Set and track daily hydration goals with visual progress
- **📈 Statistics & Analytics**: View hydration patterns over time with detailed charts
- **☕ Multiple Cup Profiles**: Calibrate different cup sizes and types
- **🌍 Cross-Platform**: Works seamlessly on Windows, macOS, and Linux
- **🎨 Modern UI**: Clean PyQt6 interface with dark/light themes
- **🔒 Privacy-First**: All data stored locally

## 🚀 Quick Start

```bash
# 1) Clone and setup
git clone https://github.com/VoxHash/Count-Cups.git
cd Count-Cups
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run
python -m app.main
```

## 💿 Installation

See [docs/installation.md](docs/installation.md) for platform-specific steps and pre-built binaries.

## 🛠 Usage

Basic usage:

1. Launch Count-Cups and allow camera access
2. Set up your first cup profile in the Calibration screen
3. Configure your daily goal in Settings
4. Start tracking in the Live Camera screen
5. View progress on the Dashboard

Advanced usage: [docs/usage.md](docs/usage.md) and [docs/cli.md](docs/cli.md)

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
DETECTION_ENGINE=heuristics
DEFAULT_THEME=auto
ENABLE_NOTIFICATIONS=true
GOAL_REMINDER_HOUR=20
```

Full reference: [docs/configuration.md](docs/configuration.md)

## 📚 Examples

- Start here: [docs/examples/example-01.md](docs/examples/example-01.md)
- More examples: [docs/examples/](docs/examples/)

## 🧩 Architecture

High-level overview: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## 🗺 Roadmap

Planned milestones: [ROADMAP.md](ROADMAP.md). For changes, see [CHANGELOG.md](CHANGELOG.md).

## 🤝 Contributing

We welcome PRs! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and follow the PR template.

## 🔒 Security

Please report vulnerabilities via [SECURITY.md](SECURITY.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenCV** for computer vision capabilities
- **PyQt6** for the modern user interface
- **MediaPipe** for advanced pose detection (optional)
- **SQLite** for local data storage
- **Nuitka** for cross-platform compilation

---

**Count-Cups** - Stay hydrated, stay healthy! 💧

Made with ❤️ by [VoxHash](https://github.com/VoxHash)
