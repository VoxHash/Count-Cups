#!/bin/bash
# Build script for Linux using Nuitka
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

echo "Building Count-Cups for Linux with Nuitka..."

# Set build directories
BUILD_DIR="build/linux"
DIST_DIR="dist/linux"

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
    "--output-filename=count-cups"
    "--linux-icon=app/assets/icons/CountCups_App.ico"
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
    echo "Executable location: $DIST_DIR/count-cups"
    
    # Make executable
    chmod +x "$DIST_DIR/count-cups"
    
    # Create AppImage (if appimagetool is available)
    if command -v appimagetool &> /dev/null; then
        echo "Creating AppImage..."
        
        # Create AppDir structure
        APPDIR="$DIST_DIR/Count-Cups.AppDir"
        mkdir -p "$APPDIR"
        
        # Copy executable
        cp "$DIST_DIR/count-cups" "$APPDIR/"
        
        # Create desktop file
        cat > "$APPDIR/count-cups.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Count-Cups
Comment=Cross-platform water intake tracker using computer vision
Exec=count-cups
Icon=count-cups
Categories=Utility;Health;
StartupNotify=true
EOF
        
        # Copy icon
        cp "app/assets/icons/CountCups_App.ico" "$APPDIR/count-cups.png"
        
        # Create AppImage
        appimagetool "$APPDIR" "$DIST_DIR/Count-Cups-x86_64.AppImage"
        
        echo "AppImage created: $DIST_DIR/Count-Cups-x86_64.AppImage"
    else
        echo "appimagetool not found, skipping AppImage creation"
    fi
    
    # Create DEB package (if dpkg-deb is available)
    if command -v dpkg-deb &> /dev/null; then
        echo "Creating DEB package..."
        
        # Create package structure
        PKG_DIR="$DIST_DIR/count-cups-pkg"
        mkdir -p "$PKG_DIR/usr/bin"
        mkdir -p "$PKG_DIR/usr/share/applications"
        mkdir -p "$PKG_DIR/usr/share/pixmaps"
        mkdir -p "$PKG_DIR/DEBIAN"
        
        # Copy executable
        cp "$DIST_DIR/count-cups" "$PKG_DIR/usr/bin/"
        
        # Create desktop file
        cat > "$PKG_DIR/usr/share/applications/count-cups.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Count-Cups
Comment=Cross-platform water intake tracker using computer vision
Exec=count-cups
Icon=count-cups
Categories=Utility;Health;
StartupNotify=true
EOF
        
        # Copy icon
        cp "app/assets/icons/CountCups_App.ico" "$PKG_DIR/usr/share/pixmaps/count-cups.png"
        
        # Create control file
        cat > "$PKG_DIR/DEBIAN/control" << EOF
Package: count-cups
Version: 1.0.0
Section: utils
Priority: optional
Architecture: amd64
Depends: libc6, libgcc-s1, libstdc++6
Maintainer: VoxHash <contact@voxhash.dev>
Description: Cross-platform water intake tracker using computer vision
 Count-Cups is a desktop application that uses computer vision to automatically
 track your water intake by detecting drinking gestures from your webcam.
 .
 Features:
  - Automatic sip detection using computer vision
  - Manual sip/cup entry
  - Daily goal tracking and statistics
  - Multiple cup profiles and calibration
  - Cross-platform support (Windows, macOS, Linux)
  - Modern, themeable UI
Homepage: https://github.com/VoxHash/Count-Cups
EOF
        
        # Create package
        dpkg-deb --build "$PKG_DIR" "$DIST_DIR/count-cups_1.0.0_amd64.deb"
        
        # Clean up
        rm -rf "$PKG_DIR"
        
        echo "DEB package created: $DIST_DIR/count-cups_1.0.0_amd64.deb"
    else
        echo "dpkg-deb not found, skipping DEB package creation"
    fi
    
    # Create installation script
    cat > "$DIST_DIR/install.sh" << 'EOF'
#!/bin/bash
# Count-Cups Installer for Linux

echo "Installing Count-Cups..."

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please do not run this script as root"
    exit 1
fi

# Create installation directory
INSTALL_DIR="$HOME/.local/bin"
mkdir -p "$INSTALL_DIR"

# Copy executable
if [ -f "count-cups" ]; then
    cp "count-cups" "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/count-cups"
    echo "Count-Cups has been installed to $INSTALL_DIR"
    echo "Make sure $INSTALL_DIR is in your PATH"
else
    echo "count-cups executable not found in current directory"
    exit 1
fi

# Create desktop file
DESKTOP_FILE="$HOME/.local/share/applications/count-cups.desktop"
mkdir -p "$(dirname "$DESKTOP_FILE")"

cat > "$DESKTOP_FILE" << 'DESKTOP_EOF'
[Desktop Entry]
Type=Application
Name=Count-Cups
Comment=Cross-platform water intake tracker using computer vision
Exec=count-cups
Icon=count-cups
Categories=Utility;Health;
StartupNotify=true
DESKTOP_EOF

# Copy icon
ICON_DIR="$HOME/.local/share/pixmaps"
mkdir -p "$ICON_DIR"
if [ -f "app/assets/icons/CountCups_App.ico" ]; then
    cp "app/assets/icons/CountCups_App.ico" "$ICON_DIR/count-cups.png"
fi

echo "Desktop entry created: $DESKTOP_FILE"
echo "Installation completed!"
EOF
    
    chmod +x "$DIST_DIR/install.sh"
    echo "Installation script created: $DIST_DIR/install.sh"
    
else
    echo "Build failed!"
    exit 1
fi
