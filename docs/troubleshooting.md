# Troubleshooting Guide

Common issues and solutions for Count-Cups.

## Common Issues

### Camera Not Detected

**Symptoms**:
- Camera feed is black or shows error
- "Camera not found" message
- Application cannot access camera

**Solutions**:

1. **Check Camera Permissions**:
   - **Windows**: Settings > Privacy > Camera > Allow apps to access camera
   - **macOS**: System Preferences > Security & Privacy > Camera
   - **Linux**: Check camera permissions in system settings

2. **Try Different Camera Index**:
   - Go to Settings > Camera
   - Try different camera index (0, 1, 2, etc.)

3. **Verify Camera is Not in Use**:
   - Close other applications using the camera
   - Restart the application

4. **Update Camera Drivers** (Windows):
   - Update camera drivers through Device Manager
   - Download latest drivers from manufacturer website

5. **Test Camera**:
   - Test camera with another application
   - Verify camera works in system camera app

### Poor Detection Accuracy

**Symptoms**:
- Missed sips
- False positive detections
- Low confidence values

**Solutions**:

1. **Improve Lighting**:
   - Ensure face and hands are well-lit
   - Avoid backlighting
   - Use consistent lighting conditions

2. **Adjust Camera Position**:
   - Position camera at eye level
   - Ensure face is centered in frame
   - Maintain consistent distance from camera

3. **Calibrate Settings**:
   - Go to Calibration screen
   - Adjust head tilt threshold
   - Adjust hand-face distance threshold
   - Test with different sensitivity settings

4. **Try Different Detection Engine**:
   - Switch between Heuristics and MediaPipe
   - MediaPipe may provide better accuracy

5. **Check Cup Visibility**:
   - Ensure cup is visible to camera
   - Avoid occluding cup with hands

### Application Crashes

**Symptoms**:
- Application closes unexpectedly
- Error messages on startup
- Freezing or hanging

**Solutions**:

1. **Check Logs**:
   - Review logs in `~/.count-cups/logs/`
   - Look for error messages
   - Note error details for reporting

2. **Update Dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

3. **Reset Settings**:
   - Go to Settings > Advanced
   - Click "Reset All Settings"
   - Restart application

4. **Check System Requirements**:
   - Verify system meets minimum requirements
   - Check available RAM and storage

5. **Report Issue**:
   - Create issue on GitHub with log details
   - Include error messages and steps to reproduce

### Performance Issues

**Symptoms**:
- Slow detection
- High CPU usage
- Laggy interface

**Solutions**:

1. **Reduce Camera Resolution**:
   - Go to Settings > Camera
   - Lower resolution (e.g., 320x240)
   - Lower frame rate (e.g., 15 FPS)

2. **Close Other Applications**:
   - Free up system resources
   - Close unnecessary applications

3. **Check System Resources**:
   - Monitor CPU and memory usage
   - Ensure sufficient resources available

4. **Update Graphics Drivers**:
   - Keep graphics drivers up to date
   - Update OpenCV if needed

5. **Use Heuristics Engine**:
   - Heuristics is faster than MediaPipe
   - Switch to heuristics for better performance

### Database Errors

**Symptoms**:
- Data not saving
- Database errors in logs
- Missing historical data

**Solutions**:

1. **Check Database Permissions**:
   - Ensure write permissions for data directory
   - Check `~/.count-cups/data/` permissions

2. **Backup and Reset**:
   - Export data before resetting
   - Delete database file and restart
   - Database will be recreated

3. **Check Disk Space**:
   - Ensure sufficient disk space
   - Free up space if needed

4. **Database Corruption**:
   - Backup data
   - Delete corrupted database
   - Restart application

### Import/Export Issues

**Symptoms**:
- CSV export fails
- Import errors
- Data format issues

**Solutions**:

1. **Check File Permissions**:
   - Ensure write permissions for export location
   - Check file path is valid

2. **Verify CSV Format**:
   - Ensure CSV follows expected format
   - Check for encoding issues (UTF-8)

3. **Check File Size**:
   - Large exports may take time
   - Be patient with large datasets

## System-Specific Issues

### Windows

**Camera Permissions**:
- Settings > Privacy > Camera > Allow desktop apps to access camera

**Antivirus Interference**:
- Add exception for Count-Cups executable
- Whitelist application in antivirus

**Driver Issues**:
- Update camera drivers
- Reinstall camera drivers if needed

### macOS

**Gatekeeper Warnings**:
- System Preferences > Security & Privacy > General
- Click "Open Anyway" for Count-Cups

**Camera Permissions**:
- System Preferences > Security & Privacy > Camera
- Grant camera access to Count-Cups

**Code Signing**:
- Pre-built binaries are code-signed
- Contact support if signing issues occur

### Linux

**Camera Permissions**:
- Check `v4l2` permissions
- Add user to `video` group: `sudo usermod -a -G video $USER`

**AppImage Issues**:
- Ensure `libfuse2` is installed
- Make AppImage executable: `chmod +x Count-Cups-x86_64.AppImage`

**Dependencies**:
- Install required system libraries
- Check distribution-specific requirements

## Getting Help

### Before Asking for Help

1. **Check Documentation**: Review relevant documentation
2. **Search Issues**: Search existing GitHub issues
3. **Check Logs**: Review application logs
4. **Try Solutions**: Attempt troubleshooting steps above

### When Reporting Issues

Include the following information:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps to reproduce
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**:
  - Operating System and version
  - Python version (if from source)
  - Count-Cups version
  - Camera model
- **Logs**: Relevant log files or output
- **Screenshots**: If applicable

### Support Channels

- **GitHub Issues**: [Create an issue](https://github.com/VoxHash/Count-Cups/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/VoxHash/Count-Cups/discussions)
- **Email**: contact@voxhash.dev
- **Documentation**: Check [FAQ](faq.md) for common questions

## Prevention

### Best Practices

1. **Regular Updates**: Keep Count-Cups updated
2. **Backup Data**: Regularly export and backup data
3. **System Maintenance**: Keep system and drivers updated
4. **Consistent Setup**: Maintain consistent camera and lighting setup
5. **Monitor Logs**: Check logs periodically for warnings

### Maintenance

1. **Clear Logs**: Periodically clear old log files
2. **Database Maintenance**: Export and backup database regularly
3. **Settings Backup**: Export settings for backup
4. **System Updates**: Keep operating system updated

## Next Steps

- **FAQ**: Check [FAQ](faq.md) for more answers
- **Support**: Visit [SUPPORT.md](../SUPPORT.md) for support options
- **Configuration**: See [Configuration](configuration.md) for settings

---

**Still having issues?** Create an issue on GitHub or contact support at contact@voxhash.dev.

