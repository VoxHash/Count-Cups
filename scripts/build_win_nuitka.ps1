# Build script for Windows using Nuitka
# Run this script from the project root directory

param(
    [switch]$Clean,
    [switch]$Release,
    [string]$PythonPath = "python"
)

Write-Host "Building Count-Cups for Windows with Nuitka..." -ForegroundColor Green

# Set build directory
$BuildDir = "build\windows"
$DistDir = "dist\windows"

# Clean build directory if requested
if ($Clean) {
    Write-Host "Cleaning build directory..." -ForegroundColor Yellow
    if (Test-Path $BuildDir) {
        Remove-Item -Recurse -Force $BuildDir
    }
    if (Test-Path $DistDir) {
        Remove-Item -Recurse -Force $DistDir
    }
}

# Create build directories
New-Item -ItemType Directory -Force -Path $BuildDir
New-Item -ItemType Directory -Force -Path $DistDir

# Set Nuitka options
$NuitkaOptions = @(
    "--standalone",
    "--onefile",
    "--windows-disable-console",
    "--enable-plugin=pyqt6",
    "--include-data-dir=app\assets=assets",
    "--include-data-file=haarcascade_frontalface_default.xml=haarcascade_frontalface_default.xml",
    "--output-dir=$DistDir",
    "--output-filename=Count-Cups.exe",
    "--windows-icon-from-ico=app\assets\icons\CountCups_App.ico",
    "--product-name=Count-Cups",
    "--product-version=1.0.0",
    "--file-version=1.0.0.0",
    "--company-name=VoxHash",
    "--file-description=Cross-platform water intake tracker using computer vision",
    "--copyright=© 2025 VoxHash. All rights reserved.",
    "--assume-yes-for-downloads"
)

# Add release optimizations if requested
if ($Release) {
    $NuitkaOptions += @(
        "--lto=yes",
        "--jobs=4"
    )
} else {
    $NuitkaOptions += @(
        "--debug"
    )
}

# Build the application
Write-Host "Building application..." -ForegroundColor Yellow
$BuildCommand = "$PythonPath -m nuitka " + ($NuitkaOptions -join " ") + " app\main.py"

Write-Host "Running: $BuildCommand" -ForegroundColor Cyan
Invoke-Expression $BuildCommand

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build completed successfully!" -ForegroundColor Green
    Write-Host "Executable location: $DistDir\Count-Cups.exe" -ForegroundColor Green
    
    # Create installer script
    $InstallerScript = @"
# Count-Cups Installer for Windows
# Run this script as Administrator to install Count-Cups

Write-Host "Installing Count-Cups..." -ForegroundColor Green

# Create installation directory
`$InstallDir = "C:\Program Files\Count-Cups"
New-Item -ItemType Directory -Force -Path `$InstallDir

# Copy executable
Copy-Item "Count-Cups.exe" "`$InstallDir\Count-Cups.exe"

# Create desktop shortcut
`$WshShell = New-Object -comObject WScript.Shell
`$Shortcut = `$WshShell.CreateShortcut("`$env:USERPROFILE\Desktop\Count-Cups.lnk")
`$Shortcut.TargetPath = "`$InstallDir\Count-Cups.exe"
`$Shortcut.Save()

# Create start menu shortcut
`$StartMenuDir = "`$env:APPDATA\Microsoft\Windows\Start Menu\Programs"
New-Item -ItemType Directory -Force -Path "`$StartMenuDir\Count-Cups"
`$StartMenuShortcut = `$WshShell.CreateShortcut("`$StartMenuDir\Count-Cups\Count-Cups.lnk")
`$StartMenuShortcut.TargetPath = "`$InstallDir\Count-Cups.exe"
`$StartMenuShortcut.Save()

Write-Host "Installation completed!" -ForegroundColor Green
Write-Host "Count-Cups has been installed to: `$InstallDir" -ForegroundColor Green
"@
    
    $InstallerScript | Out-File -FilePath "$DistDir\install.ps1" -Encoding UTF8
    
    Write-Host "Installer script created: $DistDir\install.ps1" -ForegroundColor Green
} else {
    Write-Host "Build failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}
