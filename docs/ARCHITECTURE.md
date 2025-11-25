# Count-Cups Architecture

## Overview

Count-Cups is built using a modular architecture that separates concerns and enables easy testing and maintenance. The application follows the Model-View-Controller (MVC) pattern with additional service layers for background tasks.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                     │
├─────────────────────────────────────────────────────────────┤
│  Main Window  │  Dashboard  │  Live Camera  │  Settings    │
│  History      │  Calibration│  Theme Manager│  Widgets     │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    Service Layer                           │
├─────────────────────────────────────────────────────────────┤
│  Notification Service  │  Scheduler Service  │  Exporter   │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    Core Business Logic                     │
├─────────────────────────────────────────────────────────────┤
│  Sip Logic    │  Detection   │  Database    │  Models      │
│  Aggregator   │  Engines     │  Operations  │  & Config    │
└─────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                              │
├─────────────────────────────────────────────────────────────┤
│  SQLite Database  │  File System  │  Configuration Files   │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Application Core (`app/core/`)

#### Configuration (`config.py`)
- **Purpose**: Centralized configuration management using Pydantic
- **Features**: Environment variable support, validation, type safety
- **Key Classes**: `Settings`

#### Models (`models.py`)
- **Purpose**: Data models and business entities
- **Features**: Pydantic models with validation, serialization
- **Key Classes**: `CupProfile`, `SipEvent`, `DailyGoal`, `UserSettings`

#### Database (`db.py`)
- **Purpose**: Database operations and data persistence
- **Features**: SQLite with migrations, CRUD operations, transactions
- **Key Classes**: `Database`

#### Logging (`logging.py`)
- **Purpose**: Structured logging with file rotation
- **Features**: Colored console output, file logging, configurable levels
- **Key Classes**: `ColoredFormatter`, logging setup functions

### 2. Detection System (`app/core/detection/`)

#### Base Detection (`base.py`)
- **Purpose**: Abstract base classes for detection engines
- **Features**: Plugin architecture, common interfaces
- **Key Classes**: `DetectionEngine`, `HeuristicDetector`, `MediaPipeDetector`

#### Heuristic Detection (`heuristics.py`)
- **Purpose**: OpenCV-based detection using computer vision heuristics
- **Features**: Face detection, hand tracking, motion analysis
- **Key Classes**: `AdvancedHeuristicDetector`

#### MediaPipe Detection (`mediapipe_impl.py`)
- **Purpose**: Advanced detection using MediaPipe (optional)
- **Features**: Pose estimation, facial landmarks, hand tracking
- **Key Classes**: `AdvancedMediaPipeDetector`

### 3. Sip Logic (`app/core/sip_logic.py`)

#### Sip Aggregator (`SipAggregator`)
- **Purpose**: Aggregates detection results into sip events
- **Features**: Temporal filtering, confidence thresholds, cooldown periods
- **Key Methods**: `process_detection()`, `_complete_sip()`

#### Cup Converter (`CupConverter`)
- **Purpose**: Converts between sips, milliliters, and cups
- **Features**: Multiple cup profiles, volume estimation
- **Key Methods**: `sips_to_cups()`, `ml_to_cups()`, `estimate_sip_ml()`

#### Sip Tracker (`SipTracker`)
- **Purpose**: Main coordinator for sip tracking
- **Features**: Daily statistics, manual entry, data aggregation
- **Key Methods**: `process_detection()`, `add_manual_sip()`, `get_daily_stats()`

### 4. User Interface (`app/ui/`)

#### Theme System (`theme.py`)
- **Purpose**: Application theming and styling
- **Features**: Auto-detection, manual switching, custom stylesheets
- **Key Classes**: `ThemeManager`, `ThemeMode`

#### Main Window (`main_window.py`)
- **Purpose**: Main application window and navigation
- **Features**: Menu bar, toolbar, status bar, screen management
- **Key Classes**: `MainWindow`

#### Screen Components (`screens/`)
- **Dashboard**: Daily statistics and quick actions
- **Live Camera**: Real-time detection interface
- **History**: Historical data and analytics
- **Calibration**: Cup profile setup and testing
- **Settings**: Application configuration

### 5. Services (`app/services/`)

#### Notification Service (`notifier.py`)
- **Purpose**: Desktop notifications and alerts
- **Features**: Cross-platform notifications, goal reminders
- **Key Classes**: `NotificationService`

#### Scheduler Service (`scheduler.py`)
- **Purpose**: Background task scheduling
- **Features**: Daily resets, goal reminders, recurring tasks
- **Key Classes**: `Scheduler`, `DailyResetScheduler`, `GoalReminderScheduler`

## Data Flow

### 1. Sip Detection Flow

```
Camera Feed → Detection Engine → Sip Aggregator → Sip Tracker → Database
     ↓              ↓                ↓              ↓           ↓
  Raw Video    Detection Result   Sip Event    Statistics   Persistence
```

### 2. User Interface Flow

```
User Action → UI Screen → Business Logic → Database → UI Update
     ↓           ↓            ↓             ↓          ↓
  Button Click  Event Handler  Core Logic  Data I/O  Refresh
```

### 3. Configuration Flow

```
Environment Variables → Settings → Database → UI Components
         ↓                ↓          ↓           ↓
    .env File      Pydantic Model  User Prefs  Theme/Config
```

## Design Patterns

### 1. Model-View-Controller (MVC)
- **Models**: Pydantic data models in `core/models.py`
- **Views**: PyQt6 UI components in `ui/screens/`
- **Controllers**: Business logic in `core/sip_logic.py` and `core/db.py`

### 2. Observer Pattern
- **PyQt6 Signals**: UI components communicate via Qt signals
- **Event Handling**: Detection events trigger UI updates
- **State Management**: Centralized state with reactive updates

### 3. Strategy Pattern
- **Detection Engines**: Pluggable detection algorithms
- **Theme Management**: Different theme implementations
- **Export Formats**: Multiple export strategies

### 4. Factory Pattern
- **Detection Engine Creation**: Factory for creating detection engines
- **UI Component Creation**: Factory for creating screen components
- **Database Migration**: Factory for creating migration handlers

### 5. Singleton Pattern
- **Settings**: Global configuration instance
- **Database**: Single database connection
- **Theme Manager**: Global theme management

## Error Handling

### 1. Exception Hierarchy
```
CountCupsException
├── DatabaseError
├── DetectionError
├── ConfigurationError
└── UIError
```

### 2. Error Recovery
- **Graceful Degradation**: Fallback to manual entry if detection fails
- **User Notifications**: Toast messages for non-critical errors
- **Logging**: Comprehensive error logging for debugging
- **State Recovery**: Automatic recovery from transient errors

### 3. Validation
- **Input Validation**: Pydantic models validate all inputs
- **Configuration Validation**: Settings validated on startup
- **Data Integrity**: Database constraints ensure data consistency

## Performance Considerations

### 1. Detection Performance
- **Frame Rate**: Configurable camera frame rate (15-60 FPS)
- **Resolution**: Adjustable camera resolution for performance
- **Detection Intervals**: Throttled detection to reduce CPU usage
- **Background Processing**: Detection runs in separate thread

### 2. Database Performance
- **Indexing**: Proper database indexes for fast queries
- **Connection Pooling**: Efficient database connection management
- **Batch Operations**: Bulk operations for data import/export
- **Data Archiving**: Optional data archiving for large datasets

### 3. Memory Management
- **Resource Cleanup**: Proper cleanup of camera and detection resources
- **Memory Monitoring**: Optional memory usage monitoring
- **Garbage Collection**: Explicit cleanup of large objects
- **Caching**: Intelligent caching of frequently accessed data

## Security Considerations

### 1. Data Privacy
- **Local Storage**: All data stored locally on user's machine
- **No Cloud Sync**: No data transmitted to external servers
- **Optional Telemetry**: Opt-in telemetry with no personal data
- **Data Encryption**: Optional database encryption

### 2. Camera Security
- **Local Processing**: All video processing happens locally
- **No Recording**: No video recording or storage
- **Permission Requests**: Explicit camera permission requests
- **Secure Disposal**: Proper cleanup of camera resources

### 3. Code Security
- **Dependency Scanning**: Regular security scans of dependencies
- **Input Sanitization**: All user inputs properly sanitized
- **SQL Injection Prevention**: Parameterized queries only
- **File Path Validation**: Secure file path handling

## Testing Strategy

### 1. Unit Tests
- **Core Logic**: Business logic and data models
- **Database Operations**: CRUD operations and migrations
- **Detection Algorithms**: Detection engine functionality
- **Utility Functions**: Helper functions and utilities

### 2. Integration Tests
- **Database Integration**: End-to-end database operations
- **UI Integration**: Screen interactions and navigation
- **Service Integration**: Background service functionality
- **Detection Integration**: Full detection pipeline

### 3. End-to-End Tests
- **User Workflows**: Complete user scenarios
- **Cross-Platform**: Platform-specific functionality
- **Performance Tests**: Load and stress testing
- **Accessibility Tests**: UI accessibility compliance

## Deployment Architecture

### 1. Build Process
- **Nuitka Compilation**: Python to native executable compilation
- **Cross-Platform**: Windows, macOS, and Linux builds
- **Dependency Bundling**: All dependencies included in executable
- **Asset Packaging**: Icons, stylesheets, and data files included

### 2. Distribution
- **GitHub Releases**: Automated release builds
- **Platform Packages**: Platform-specific installers
- **Update Mechanism**: Optional automatic update checking
- **Installation Scripts**: Automated installation scripts

### 3. Configuration Management
- **Environment Variables**: Runtime configuration
- **User Settings**: Persistent user preferences
- **Default Values**: Sensible defaults for all settings
- **Migration Support**: Automatic configuration migration

## Future Architecture Considerations

### 1. Scalability
- **Plugin System**: Extensible plugin architecture
- **API Layer**: Optional REST API for external integrations
- **Microservices**: Potential service decomposition
- **Cloud Integration**: Optional cloud backup and sync

### 2. Performance
- **GPU Acceleration**: GPU-accelerated detection
- **Machine Learning**: ML-based detection improvements
- **Caching Layer**: Advanced caching strategies
- **Async Processing**: Full async/await implementation

### 3. Features
- **Multi-User**: Support for multiple user profiles
- **Team Features**: Shared goals and challenges
- **Health Integration**: Integration with health platforms
- **Wearable Support**: Integration with fitness trackers

This architecture provides a solid foundation for the Count-Cups application while maintaining flexibility for future enhancements and improvements.
