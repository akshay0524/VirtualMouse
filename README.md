# Virtual Mouse System 🖱️✋

A professional, production-ready virtual mouse control system using real-time hand gesture recognition through computer vision.

## 🎯 Features

### ✅ Fully Implemented Gestures

1. **Cursor Movement**
   - Track index finger tip in real-time
   - Smooth cursor movement with exponential moving average
   - Dynamic coordinate mapping from camera to screen
   - No jitter or lag

2. **Left Click**
   - Pinch gesture: Index finger + Thumb
   - Debounced to prevent multiple unintended clicks
   - Visual feedback in UI

3. **Right Click**
   - Pinch gesture: Middle finger + Thumb
   - Independent from left click detection
   - Cooldown mechanism

4. **Drag & Drop**
   - Hold index + thumb pinch continuously
   - Activation delay to prevent accidental drags
   - Visual "DRAGGING" indicator
   - Smooth drag operation

5. **Scroll Control**
   - Extend index and middle fingers vertically
   - Move hand up/down to scroll
   - Adjustable sensitivity
   - Debounced for smooth scrolling

## 🏗️ Architecture

```
VirtualMouse/
├── config.py              # All configurable parameters
├── hand_tracker.py        # MediaPipe hand detection & gesture recognition
├── mouse_controller.py    # System mouse control & coordinate mapping
├── virtual_mouse.py       # Main application & orchestration
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── INSTALLATION.md       # Detailed setup instructions
└── DOCUMENTATION.md      # Technical documentation
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install opencv-python mediapipe pyautogui numpy
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python virtual_mouse.py
```

### 3. Use Gestures

- **Move cursor**: Point with your index finger
- **Left click**: Pinch index finger and thumb together
- **Right click**: Pinch middle finger and thumb together
- **Drag**: Hold index + thumb pinch and move
- **Scroll**: Extend index and middle fingers, move hand vertically

### 4. Exit

Press **Q** to quit the application.

## 📋 Requirements

### System Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.7 or higher
- **Webcam**: Any USB or built-in camera
- **RAM**: 4GB minimum (8GB recommended)
- **CPU**: Multi-core processor recommended

### Python Dependencies
- `opencv-python >= 4.5.0` - Webcam capture and image processing
- `mediapipe >= 0.8.0` - Hand landmark detection
- `pyautogui >= 0.9.50` - System mouse control
- `numpy >= 1.19.0` - Mathematical operations

## ⚙️ Configuration

All settings can be adjusted in `config.py`:

### Camera Settings
```python
CAMERA_INDEX = 0          # Camera selection (0, 1, 2...)
CAMERA_WIDTH = 640        # Frame width
CAMERA_HEIGHT = 480       # Frame height
CAMERA_FPS = 30          # Target FPS
```

### Gesture Sensitivity
```python
LEFT_CLICK_THRESHOLD = 0.04   # Lower = easier to trigger
RIGHT_CLICK_THRESHOLD = 0.04
DRAG_THRESHOLD = 0.04
SCROLL_THRESHOLD = 0.15
```

### Cursor Movement
```python
SMOOTHING_FACTOR = 0.5    # 0.0 = very smooth, 1.0 = instant
FRAME_REDUCTION = 100     # Edge dead zone in pixels
CURSOR_SPEED = 1.0        # Speed multiplier
```

### Performance
```python
FRAME_SKIP = 1           # Process every Nth frame (1 = all frames)
MODEL_COMPLEXITY = 1     # 0 = lite/fast, 1 = full/accurate
```

## 🎨 UI Elements

The camera feed window displays:
- **Green landmarks**: Hand skeleton overlay
- **Blue rectangle**: Active control area
- **FPS counter**: Real-time performance
- **Gesture status**: Current detected gesture
- **Drag indicator**: Shows when dragging is active

## 🔧 Troubleshooting

### Camera Not Opening
```
Error: Failed to open camera
```
**Solutions**:
1. Check if camera is connected
2. Close other applications using the camera
3. Try different `CAMERA_INDEX` values (0, 1, 2)
4. Check camera permissions in system settings

### Cursor Too Sensitive/Slow
**Solutions**:
1. Adjust `SMOOTHING_FACTOR` in config.py (0.3-0.7 range)
2. Modify `CURSOR_SPEED` multiplier
3. Increase `FRAME_REDUCTION` for smaller control area

### Gestures Not Detected
**Solutions**:
1. Ensure good lighting conditions
2. Lower `MIN_DETECTION_CONFIDENCE` (try 0.5)
3. Adjust gesture thresholds (increase values)
4. Keep hand within blue rectangle boundary

### Performance Issues (Low FPS)
**Solutions**:
1. Set `FRAME_SKIP = 2` or `3`
2. Use `MODEL_COMPLEXITY = 0` for lite model
3. Reduce `CAMERA_WIDTH` and `CAMERA_HEIGHT`
4. Close other resource-intensive applications

### Multiple Unintended Clicks
**Solutions**:
1. Increase `CLICK_COOLDOWN_FRAMES` (try 20-30)
2. Increase gesture thresholds (try 0.05-0.06)
3. Increase `DRAG_ACTIVATION_FRAMES` for drag

## 📊 Performance Tips

### Optimize for Speed
```python
FRAME_SKIP = 2
MODEL_COMPLEXITY = 0
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
```

### Optimize for Accuracy
```python
FRAME_SKIP = 1
MODEL_COMPLEXITY = 1
MIN_DETECTION_CONFIDENCE = 0.8
MIN_TRACKING_CONFIDENCE = 0.8
```

### Optimize for Smoothness
```python
SMOOTHING_FACTOR = 0.3
CLICK_COOLDOWN_FRAMES = 20
DRAG_ACTIVATION_FRAMES = 5
```

## 🐛 Common Errors & Fixes

### ImportError: No module named 'cv2'
```bash
pip install opencv-python
```

### ImportError: No module named 'mediapipe'
```bash
pip install mediapipe
```

### PyAutoGUI FailSafeException
Set `pyautogui.FAILSAFE = False` in `mouse_controller.py` (already done)

### Hand Detection Not Working
- Ensure good lighting
- Keep hand flat and fingers spread
- Stay within camera frame
- Avoid cluttered backgrounds

## 🎓 How It Works

### 1. Hand Detection (MediaPipe)
- Captures webcam frames using OpenCV
- Processes frames with MediaPipe Hands model
- Detects 21 hand landmarks in 3D space
- Tracks landmarks across frames

### 2. Gesture Recognition (Custom Logic)
- Calculates distances between specific landmarks
- Compares distances against thresholds
- Identifies gestures based on finger positions
- Implements state machine for gesture flow

### 3. Coordinate Mapping
- Normalizes camera coordinates (0-1 range)
- Applies frame reduction for edge handling
- Maps to screen resolution dynamically
- Flips X-axis for natural mirror effect

### 4. Mouse Control (PyAutoGUI)
- Moves cursor to mapped coordinates
- Executes clicks, drags, and scrolls
- Implements debouncing for reliability
- Manages gesture state transitions

### 5. Smoothing & Optimization
- Exponential moving average for cursor
- Frame skipping for performance
- Cooldown timers for gestures
- Activation delays for complex gestures

## 📈 Technical Specifications

- **Hand Detection**: MediaPipe Hands (Google)
- **Landmark Points**: 21 per hand (3D coordinates)
- **Detection Latency**: < 50ms on modern hardware
- **Cursor Smoothing**: Exponential moving average
- **Coordinate System**: Normalized (0.0-1.0)
- **Thread Safety**: Single-threaded design
- **Platform Support**: Cross-platform (Windows/macOS/Linux)

## 🔐 Privacy & Security

- **No data collection**: All processing is local
- **No network access**: Fully offline operation
- **No storage**: No images or data saved
- **Camera access**: Only while application is running
- **Open source**: Full code transparency

## 📝 License

This project is provided as-is for educational and personal use.

## 👨‍💻 Author

**Senior Computer Vision + Python Engineer**
- Expertise: Computer Vision, Real-time Processing, Gesture Recognition
- Date: January 2026

## 🙏 Acknowledgments

- **MediaPipe** by Google for hand tracking
- **OpenCV** for computer vision tools
- **PyAutoGUI** for cross-platform mouse control

## 📞 Support

For issues or questions:
1. Check `DOCUMENTATION.md` for detailed technical info
2. Review `INSTALLATION.md` for setup help
3. Adjust settings in `config.py`
4. Enable `DEBUG_MODE` for verbose logging

---

**Built with ❤️ for the Computer Vision Community**
# VirtualMouse
