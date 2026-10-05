# Changelog — Count-Cups

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-10-05

### Added
- Pydantic v2 compatibility updates
- Improved theme management consistency

### Changed
- Pin `opencv-python` to `>=4.8.0,<5` (OpenCV 5.0 breaks Haar cascade sip detection)
- Bump package/app version metadata to 1.0.1
- Rename `docs/ARCHITECTURE.md` to `docs/architecture.md` for kit consistency
- Remove obsolete `DEVELOPMENT_GOALS.md` (goals live in `ROADMAP.md`)
- Tighten `.gitignore` to project-relevant patterns
- Refresh `ROADMAP.md` for post-1.0 priorities
- Updated Pydantic validators to use `@field_validator` instead of deprecated `@validator`
- Migrated all Pydantic models to use `model_config` instead of `class Config`
- Unified `ThemeMode` enum definition (removed duplicate)

### Fixed
- Haar cascade detection failing when `pip` resolved OpenCV 5.0 (`CascadeClassifier` missing)
- Resolved duplicate `ThemeMode` enum causing import conflicts
- Fixed Pydantic v2 compatibility issues in configuration and models

## [1.0.0] - 2025-01-01

### Added
- Initial release with core functionality
- Computer vision-based sip detection using OpenCV
- Manual entry options for sips and cups
- Daily goal tracking with visual progress indicators
- Statistics and analytics dashboard
- Multiple cup profile support with calibration
- Cross-platform support (Windows, macOS, Linux)
- Modern PyQt6 user interface
- Theme support (Light, Dark, Dracula, Auto)
- Data persistence with SQLite database
- CSV export and import functionality
- Desktop notifications for goal reminders
- System tray integration
- Comprehensive documentation

### Technical
- Heuristic-based detection engine (default)
- Optional MediaPipe detection engine
- SQLite database with migration support
- Structured logging with file rotation
- Configuration management with Pydantic
- Cross-platform build scripts with Nuitka

---

[Unreleased]: https://github.com/VoxHash/Count-Cups/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/VoxHash/Count-Cups/releases/tag/v1.0.1
[1.0.0]: https://github.com/VoxHash/Count-Cups/releases/tag/v1.0.0
