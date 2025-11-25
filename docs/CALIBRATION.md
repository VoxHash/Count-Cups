# Calibration Guide

This guide will help you set up and calibrate Count-Cups for optimal detection accuracy.

## Table of Contents

- [Quick Start](#quick-start)
- [Cup Profile Setup](#cup-profile-setup)
- [Detection Calibration](#detection-calibration)
- [Testing Your Setup](#testing-your-setup)
- [Troubleshooting](#troubleshooting)
- [Advanced Settings](#advanced-settings)

## Quick Start

1. **Launch Count-Cups** and navigate to the Calibration screen
2. **Set up your first cup profile** with name, size, and sips per cup
3. **Test the detection** using the built-in test mode
4. **Adjust sensitivity** if needed based on test results
5. **Save your settings** and start tracking

## Cup Profile Setup

### Creating a Cup Profile

1. **Open Calibration Screen**: Go to Calibration from the main menu
2. **Fill in Cup Details**:
   - **Name**: Descriptive name (e.g., "Coffee Mug", "Water Bottle")
   - **Size**: Volume in milliliters (e.g., 250ml, 500ml)
   - **Sips per Cup**: Average number of sips to finish the cup
   - **Color**: Optional hex color for UI display
   - **Default**: Check if this should be your default cup

3. **Save Profile**: Click "Save Settings" to create the profile

### Recommended Cup Profiles

| Cup Type | Size (ml) | Sips per Cup | Notes |
|----------|-----------|--------------|-------|
| Small Coffee Mug | 200 | 8-12 | Standard coffee mug |
| Large Coffee Mug | 350 | 12-18 | Large coffee mug |
| Water Glass | 250 | 10-15 | Standard drinking glass |
| Water Bottle | 500 | 15-25 | Reusable water bottle |
| Travel Mug | 300 | 12-20 | Insulated travel mug |
| Wine Glass | 150 | 6-10 | Standard wine glass |

### Tips for Accurate Profiles

- **Measure your cups**: Use a measuring cup to get exact volumes
- **Count sips**: Actually count sips while drinking to get accurate numbers
- **Test different scenarios**: Try different drinking speeds and styles
- **Update profiles**: Adjust profiles based on your actual usage

## Detection Calibration

### Basic Detection Settings

1. **Head Tilt Threshold**: How much you need to tilt your head (10-60°)
   - **Lower values**: More sensitive, detects smaller movements
   - **Higher values**: Less sensitive, requires more obvious tilting

2. **Hand-Face Distance**: How close your hand needs to be to your face (50-200px)
   - **Lower values**: Hand must be very close to face
   - **Higher values**: Hand can be further from face

3. **Sip Duration**: How long a sip must last to be counted (1-100 frames)
   - **Min Duration**: Minimum frames for a valid sip
   - **Max Duration**: Maximum frames before sip times out

### Advanced Detection Settings

1. **Confidence Threshold**: Minimum confidence for sip detection (10-100%)
   - **Lower values**: More detections, may include false positives
   - **Higher values**: Fewer detections, more accurate

2. **Motion Detection**: Enable/disable motion-based detection
   - **Enabled**: Requires movement in face region
   - **Disabled**: Only uses hand position and head tilt

3. **Detection Engine**: Choose between detection methods
   - **Heuristics**: Fast, works without additional dependencies
   - **MediaPipe**: More accurate, requires MediaPipe installation

## Testing Your Setup

### Using the Test Mode

1. **Start Test**: Click "Start Test" in the Calibration screen
2. **Position Yourself**: Sit in front of the camera at normal distance
3. **Perform Gestures**: Make drinking motions with your cup
4. **Observe Results**: Watch the detection feedback and confidence levels
5. **Stop Test**: Click "Stop Test" when finished

### What to Look For

- **Green Circles**: Hand detection working correctly
- **Blue Rectangles**: Face detection working correctly
- **Yellow Lines**: Hand-to-face distance measurement
- **Confidence Values**: Should be above 50% for good detection
- **Detection Count**: Should increment when you drink

### Test Scenarios

1. **Normal Drinking**: Standard drinking motion
2. **Slow Drinking**: Deliberate, slow drinking motion
3. **Quick Sips**: Fast, small sips
4. **Different Angles**: Try different head positions
5. **Different Distances**: Vary your distance from camera

## Troubleshooting

### Common Issues

#### No Hand Detection
- **Check lighting**: Ensure good lighting on your hands
- **Adjust distance**: Move hand closer to face
- **Check skin tone**: Ensure hands are visible against background
- **Try different angles**: Change hand position

#### No Face Detection
- **Check camera**: Ensure camera is working and positioned correctly
- **Improve lighting**: Ensure face is well-lit
- **Adjust position**: Sit directly in front of camera
- **Check camera permissions**: Ensure app has camera access

#### False Positives
- **Increase confidence threshold**: Raise the minimum confidence level
- **Adjust hand distance**: Increase minimum hand-to-face distance
- **Enable motion detection**: Require movement for detection
- **Fine-tune head tilt**: Increase head tilt threshold

#### Missed Sips
- **Decrease confidence threshold**: Lower the minimum confidence level
- **Adjust hand distance**: Decrease minimum hand-to-face distance
- **Check sip duration**: Ensure minimum duration isn't too high
- **Improve lighting**: Better lighting improves detection

### Detection Quality Tips

1. **Good Lighting**: Ensure your face and hands are well-lit
2. **Stable Position**: Sit in a consistent position relative to camera
3. **Visible Cup**: Keep your cup visible to the camera
4. **Consistent Gestures**: Use similar drinking motions
5. **Clean Background**: Avoid cluttered backgrounds behind you

## Advanced Settings

### Camera Settings

1. **Camera Index**: Select which camera to use (0 for default)
2. **Resolution**: Adjust camera resolution (320x240 to 1920x1080)
3. **Frame Rate**: Set detection frame rate (15-60 FPS)
4. **Auto Focus**: Enable/disable camera auto focus

### Performance Settings

1. **Detection Interval**: How often to run detection (every N frames)
2. **Memory Usage**: Limit memory usage for detection
3. **CPU Usage**: Limit CPU usage for detection
4. **Background Processing**: Run detection in background

### Debug Settings

1. **Debug Mode**: Enable detailed logging and visual feedback
2. **Detection Overlay**: Show detection overlays on camera feed
3. **Confidence Display**: Show confidence values on screen
4. **Frame Rate Display**: Show actual frame rate

## Calibration Best Practices

### Environment Setup

1. **Consistent Lighting**: Use the same lighting conditions daily
2. **Stable Camera**: Mount camera or use a stable surface
3. **Clean Background**: Minimize distractions behind you
4. **Comfortable Position**: Sit in a comfortable, repeatable position

### Profile Management

1. **Multiple Profiles**: Create profiles for different cup types
2. **Regular Updates**: Update profiles based on actual usage
3. **Seasonal Adjustments**: Adjust for different seasons/lighting
4. **Backup Settings**: Export settings for backup

### Testing Schedule

1. **Initial Setup**: Test thoroughly when first setting up
2. **Weekly Checks**: Test detection quality weekly
3. **After Changes**: Test after any setting changes
4. **Seasonal Reviews**: Review and adjust seasonally

## Getting Help

If you're having trouble with calibration:

1. **Check the troubleshooting section** above
2. **Review the user guide** for general setup
3. **Search existing issues** on GitHub
4. **Create a new issue** with detailed information
5. **Join discussions** for community help

## Calibration Checklist

- [ ] Cup profiles created and tested
- [ ] Detection settings calibrated
- [ ] Test mode completed successfully
- [ ] False positive rate acceptable
- [ ] Missed sip rate acceptable
- [ ] Settings saved and backed up
- [ ] Regular testing scheduled

Remember: Calibration is an ongoing process. Don't be afraid to adjust settings as you learn more about how the system works with your specific setup and drinking habits.
