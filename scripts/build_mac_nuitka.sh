#!/bin/bash
# Build script for macOS using Nuitka
# Run this script from the project root directory

set -e

# Parse command line arguments
CLEAN=false
RELEASE=false
PYTHON_PATH="python3"

while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN=true
            shift
            ;;
        --release)
            RELEASE=true
            shift
            ;;
        --python)
            PYTHON_PATH="$2"
            shift 2
            ;;
        *)
            echo "Unknown option $1"
            exit 1
            ;;
    esac
done

echo "Building Count-Cups for macOS with Nuitka..."

# Set build directories
BUILD_DIR="build/macos"
DIST_DIR="dist/macos"

# Clean build directory if requested
if [ "$CLEAN" = true ]; then
    echo "Cleaning build directory..."
    rm -rf "$BUILD_DIR"
    rm -rf "$DIST_DIR"
fi

# Create build directories
mkdir -p "$BUILD_DIR"
mkdir -p "$DIST_DIR"

# Set Nuitka options
NUITKA_OPTIONS=(
    "--standalone"
    "--onefile"
    "--enable-plugin=pyqt6"
    "--include-data-dir=app/assets=assets"
    "--include-data-file=haarcascade_frontalface_default.xml=haarcascade_frontalface_default.xml"
    "--output-dir=$DIST_DIR"
    "--output-filename=Count-Cups"
    "--macos-create-app-bundle"
    "--macos-app-icon=app/assets/icons/CountCups_App.ico"
    "--product-name=Count-Cups"
    "--product-version=1.0.0"
    "--file-version=1.0.0.0"
    "--company-name=VoxHash"
    "--file-description=Cross-platform water intake tracker using computer vision"
    "--copyright=© 2025 VoxHash. All rights reserved."
    "--assume-yes-for-downloads"
)

# Add release optimizations if requested
if [ "$RELEASE" = true ]; then
    NUITKA_OPTIONS+=(
        "--lto=yes"
        "--jobs=4"
    )
else
    NUITKA_OPTIONS+=(
        "--debug"
    )
fi

# Build the application
echo "Building application..."
BUILD_COMMAND="$PYTHON_PATH -m nuitka ${NUITKA_OPTIONS[*]} app/main.py"

echo "Running: $BUILD_COMMAND"
eval $BUILD_COMMAND

if [ $? -eq 0 ]; then
    echo "Build completed successfully!"
    echo "Application bundle location: $DIST_DIR/Count-Cups.app"
    
    # Create DMG installer
    echo "Creating DMG installer..."
    
    # Create DMG directory structure
    DMG_DIR="dmg_temp"
    mkdir -p "$DMG_DIR"
    
    # Copy app bundle
    cp -R "$DIST_DIR/Count-Cups.app" "$DMG_DIR/"
    
    # Create Applications symlink
    ln -s /Applications "$DMG_DIR/Applications"
    
    # Create DMG
    hdiutil create -volname "Count-Cups" -srcfolder "$DMG_DIR" -ov -format UDZO "$DIST_DIR/Count-Cups.dmg"
    
    # Clean up
    rm -rf "$DMG_DIR"
    
    echo "DMG installer created: $DIST_DIR/Count-Cups.dmg"
    
    # Create installation script
    cat > "$DIST_DIR/install.sh" << 'EOF'
#!/bin/bash
# Count-Cups Installer for macOS

echo "Installing Count-Cups..."

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run this script as root"
    exit 1
fi

# Copy app to Applications folder
if [ -d "Count-Cups.app" ]; then
    cp -R "Count-Cups.app" "/Applications/"
    echo "Count-Cups has been installed to /Applications/"
    echo "You can now launch it from the Applications folder or Spotlight search."
else
    echo "Count-Cups.app not found in current directory"
    exit 1
fi
EOF
    
    chmod +x "$DIST_DIR/install.sh"
    echo "Installation script created: $DIST_DIR/install.sh"
    
else
    echo "Build failed!"
    exit 1
fi
