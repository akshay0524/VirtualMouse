# 🔧 Troubleshooting Guide - Virtual Mouse System

Complete solutions for common issues and errors.

## 📋 Table of Contents

1. [Installation Issues](#installation-issues)
2. [Camera Issues](#camera-issues)
3. [Gesture Detection Issues](#gesture-detection-issues)
4. [Performance Issues](#performance-issues)
5. [Mouse Control Issues](#mouse-control-issues)
6. [Platform-Specific Issues](#platform-specific-issues)

---

## 🔨 Installation Issues

### Error: "No module named 'cv2'"

**Cause:** OpenCV not installed

**Solution:**
```bash
pip uninstall opencv-python
pip install opencv-python
```

**Alternative:**
```bash
pip install opencv-python-headless  # If GUI issues
```

---

### Error: "No module named 'mediapipe'"

**Cause:** MediaPipe not installed or incompatible Python version

**Solution:**
```bash
# Check Python version (must be 3.7-3.11)
python --version

# Install MediaPipe
pip install mediapipe

# If fails, try specific version
pip install mediapipe==0.10.0
```

**Note:** MediaPipe may not support Python 3.12+ yet. Use Python 3.9-3.11.

---

### Error: "ImportError: DLL load failed" (Windows)

**Cause:** Missing Visual C++ Redistributable

**Solution:**
1. Download VC++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Install and restart computer
3. Reinstall packages:
```bash
pip install --upgrade opencv-python mediapipe
```

---

### Error: "Permission denied" during pip install

**Cause:** Insufficient permissions

**Solution (Windows):**
```bash
# Install for user only
pip install --user -r requirements.txt

# OR run as administrator
# Right-click Command Prompt → Run as Administrator
pip install -r requirements.txt
```

**Solution (macOS/Linux):**
```bash
# Install for user only
pip install --user -r requirements.txt

# OR use sudo (not recommended)
sudo pip install -r requirements.txt
```

---

## 📷 Camera Issues

### Error: "Failed to open camera"

**Cause:** Camera not available or in use

**Solution 1 - Check camera index:**
```python
# Test all camera indices
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i}: Available")
        cap.release()
    else:
        print(f"Camera {i}: Not available")

# Update config.py with working index
CAMERA_INDEX = 1  # or whichever works
```

**Solution 2 - Close other applications:**
- Close Zoom, Skype, Teams, etc.
- Close other Python scripts using camera
- Restart computer

**Solution 3 - Check permissions:**

**Windows:**
- Settings → Privacy → Camera
- Enable "Allow desktop apps to access your camera"

**macOS:**
- System Preferences → Security & Privacy → Camera
- Add Terminal/Python to allowed apps

**Linux:**
```bash
# Check if user is in video group
groups

# Add user to video group
sudo usermod -a -G video $USER

# Log out and log back in
```

---

### Camera opens but shows black screen

**Cause:** Camera blocked or driver issue

**Solution:**
1. Check if camera lens is covered
2. Test camera with another application
3. Update camera drivers
4. Try different USB port (if external camera)
5. Restart computer

---

### Camera feed is very slow/laggy

**Cause:** High resolution or slow hardware

**Solution:**
```python
# In config.py
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
CAMERA_FPS = 15
```

---

## 👋 Gesture Detection Issues

### Hand not detected

**Cause:** Poor lighting, hand position, or detection settings

**Solution 1 - Improve lighting:**
- Use bright, even lighting
- Avoid backlighting (light behind you)
- Face a window or use desk lamp

**Solution 2 - Adjust detection confidence:**
```python
# In config.py
MIN_DETECTION_CONFIDENCE = 0.5  # Lower = easier detection
MIN_TRACKING_CONFIDENCE = 0.5
```

**Solution 3 - Check hand position:**
- Keep hand 30-60cm from camera
- Keep hand flat with fingers spread
- Ensure entire hand is in frame
- Stay within blue rectangle

**Solution 4 - Check background:**
- Use plain background
- Avoid cluttered or moving backgrounds
- Ensure good contrast between hand and background

---

### Gestures not triggering

**Cause:** Thresholds too strict

**Solution:**
```python
# In config.py - Make gestures easier to trigger
LEFT_CLICK_THRESHOLD = 0.06  # Increase from 0.04
RIGHT_CLICK_THRESHOLD = 0.06
DRAG_THRESHOLD = 0.06
SCROLL_THRESHOLD = 0.12  # Decrease from 0.15

# Enable debug mode to see distances
DEBUG_MODE = True
PRINT_DISTANCES = True
```

**Test process:**
1. Run application with debug mode
2. Perform gesture
3. Note printed distance
4. Set threshold slightly above/below that value

---

### Multiple unintended clicks

**Cause:** Cooldown too short or threshold too loose

**Solution:**
```python
# In config.py
CLICK_COOLDOWN_FRAMES = 25  # Increase from 15
LEFT_CLICK_THRESHOLD = 0.03  # Decrease from 0.04 (stricter)
```

---

### Drag activates when trying to click

**Cause:** Activation delay too short

**Solution:**
```python
# In config.py
DRAG_ACTIVATION_FRAMES = 5  # Increase from 3
```

---

### Scroll not working

**Cause:** Fingers not detected as separated

**Solution:**
```python
# In config.py
SCROLL_THRESHOLD = 0.12  # Decrease from 0.15
SCROLL_SENSITIVITY = 30  # Increase from 20
```

**Technique:**
- Extend index and middle fingers clearly
- Keep fingers separated (peace sign)
- Move hand vertically (not horizontally)

---

## ⚡ Performance Issues

### Low FPS (< 15)

**Cause:** Hardware limitations or settings

**Solution - Optimize for performance:**
```python
# In config.py
FRAME_SKIP = 2  # Process every other frame
MODEL_COMPLEXITY = 0  # Use lite model
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
SHOW_LANDMARKS = False  # Disable visual landmarks
```

**Additional steps:**
- Close other applications
- Update graphics drivers
- Use wired camera (not wireless)
- Reduce screen resolution

---

### High CPU usage

**Cause:** Processing too many frames

**Solution:**
```python
# In config.py
FRAME_SKIP = 3  # Process every 3rd frame
MODEL_COMPLEXITY = 0
CAMERA_FPS = 15  # Reduce target FPS
```

---

### Memory leak / increasing RAM usage

**Cause:** OpenCV or MediaPipe not releasing resources

**Solution:**
1. Restart application periodically
2. Update packages:
```bash
pip install --upgrade opencv-python mediapipe
```

3. Add manual cleanup:
```python
# Press 'R' to reset (already implemented)
```

---

## 🖱️ Mouse Control Issues

### Cursor not moving

**Cause:** PyAutoGUI not working or permissions

**Solution 1 - Test PyAutoGUI:**
```python
import pyautogui
pyautogui.moveTo(500, 500)  # Should move cursor
```

**Solution 2 - Grant permissions:**

**macOS:**
- System Preferences → Security & Privacy → Accessibility
- Add Terminal/Python

**Linux:**
```bash
# Install X11 dependencies
sudo apt install python3-tk python3-dev python3-xlib
pip install python-xlib
```

**Windows:**
- Run as Administrator

---

### Cursor movement is jittery

**Cause:** Smoothing factor too high

**Solution:**
```python
# In config.py
SMOOTHING_FACTOR = 0.3  # Decrease from 0.5
```

---

### Cursor movement is too slow/laggy

**Cause:** Smoothing factor too low

**Solution:**
```python
# In config.py
SMOOTHING_FACTOR = 0.7  # Increase from 0.5
CURSOR_SPEED = 1.5  # Increase speed multiplier
```

---

### Cursor gets stuck at screen edges

**Cause:** Frame reduction too small

**Solution:**
```python
# In config.py
FRAME_REDUCTION = 150  # Increase from 100
```

---

### Clicks not working

**Cause:** PyAutoGUI permissions or cooldown

**Solution 1 - Check permissions (see above)**

**Solution 2 - Reduce cooldown:**
```python
# In config.py
CLICK_COOLDOWN_FRAMES = 10  # Decrease from 15
```

**Solution 3 - Test manually:**
```python
import pyautogui
pyautogui.click()  # Should click
```

---

### Drag and drop not working

**Cause:** Activation delay or PyAutoGUI issue

**Solution:**
```python
# In config.py
DRAG_ACTIVATION_FRAMES = 2  # Decrease from 3

# Test PyAutoGUI drag
import pyautogui
pyautogui.mouseDown()
pyautogui.moveTo(500, 500)
pyautogui.mouseUp()
```

---

## 💻 Platform-Specific Issues

### Windows Issues

**Issue: "VCRUNTIME140.dll not found"**

**Solution:**
- Install Visual C++ Redistributable
- https://aka.ms/vs/17/release/vc_redist.x64.exe

---

**Issue: Antivirus blocking PyAutoGUI**

**Solution:**
- Add Python to antivirus exceptions
- Temporarily disable antivirus for testing

---

### macOS Issues

**Issue: "Operation not permitted"**

**Solution:**
1. System Preferences → Security & Privacy → Privacy
2. Select "Accessibility" and add Terminal
3. Select "Camera" and add Terminal
4. Restart Terminal

---

**Issue: "No module named '_tkinter'"**

**Solution:**
```bash
# Install tkinter
brew install python-tk

# Or reinstall Python with tkinter
brew reinstall python
```

---

### Linux Issues

**Issue: "ImportError: libGL.so.1"**

**Solution:**
```bash
# Ubuntu/Debian
sudo apt install libgl1-mesa-glx

# Fedora
sudo dnf install mesa-libGL

# Arch
sudo pacman -S mesa
```

---

**Issue: "No module named 'Xlib'"**

**Solution:**
```bash
sudo apt install python3-xlib
pip install python-xlib
```

---

**Issue: PyAutoGUI not working on Wayland**

**Solution:**
```bash
# Switch to X11 session
# Or install ydotool for Wayland support
sudo apt install ydotool
```

---

## 🔍 Debugging Tools

### Enable Debug Mode

```python
# In config.py
DEBUG_MODE = True
PRINT_DISTANCES = True
```

**Output:**
- Gesture distances
- Click events
- Drag events
- Scroll events

---

### Test Individual Components

**Test Camera:**
```python
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cv2.imshow("Test", frame)
cv2.waitKey(0)
cap.release()
```

**Test MediaPipe:**
```python
import mediapipe as mp
hands = mp.solutions.hands.Hands()
print("MediaPipe initialized successfully")
```

**Test PyAutoGUI:**
```python
import pyautogui
print(f"Screen size: {pyautogui.size()}")
pyautogui.moveTo(500, 500)
pyautogui.click()
```

---

### Check System Information

```python
import sys
import cv2
import mediapipe as mp
import pyautogui

print(f"Python: {sys.version}")
print(f"OpenCV: {cv2.__version__}")
print(f"MediaPipe: {mp.__version__}")
print(f"PyAutoGUI: {pyautogui.__version__}")
print(f"Screen: {pyautogui.size()}")
```

---

## 📞 Still Having Issues?

### Checklist:

- [ ] Python 3.7-3.11 installed
- [ ] All dependencies installed (`pip list`)
- [ ] Camera working in other apps
- [ ] Good lighting conditions
- [ ] Permissions granted (camera, accessibility)
- [ ] No other apps using camera
- [ ] Debug mode enabled
- [ ] Tried different camera indices
- [ ] Tried adjusting thresholds
- [ ] Restarted computer

### Get More Help:

1. **Enable verbose logging:**
```python
# In config.py
DEBUG_MODE = True
PRINT_DISTANCES = True
```

2. **Check error messages carefully**
   - Read full error traceback
   - Google specific error messages
   - Check line numbers in stack trace

3. **Test with minimal settings:**
```python
# In config.py - Minimal configuration
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
FRAME_SKIP = 2
MODEL_COMPLEXITY = 0
SHOW_LANDMARKS = True
DEBUG_MODE = True
```

4. **Verify hardware:**
   - Test camera in other applications
   - Check system requirements
   - Update drivers

---

## 🎯 Quick Fixes Summary

| Problem | Quick Fix |
|---------|-----------|
| Camera won't open | Try `CAMERA_INDEX = 1` |
| Hand not detected | Lower `MIN_DETECTION_CONFIDENCE = 0.5` |
| Gestures not working | Increase thresholds to 0.06 |
| Too many clicks | Increase `CLICK_COOLDOWN_FRAMES = 25` |
| Low FPS | Set `FRAME_SKIP = 2`, `MODEL_COMPLEXITY = 0` |
| Jittery cursor | Lower `SMOOTHING_FACTOR = 0.3` |
| Slow cursor | Increase `SMOOTHING_FACTOR = 0.7` |
| Cursor stuck at edges | Increase `FRAME_REDUCTION = 150` |

---

**Last Resort:** Delete and reinstall everything:
```bash
pip uninstall opencv-python mediapipe pyautogui numpy
pip install -r requirements.txt
```

---

**Document Version:** 1.0  
**Last Updated:** January 2026
