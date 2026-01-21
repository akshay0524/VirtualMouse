# Installation Guide - Virtual Mouse System

Complete step-by-step installation instructions for Windows, macOS, and Linux.

## 📋 Prerequisites

### 1. Python Installation

**Windows:**
```bash
# Download Python from python.org (3.7 or higher)
# During installation, check "Add Python to PATH"

# Verify installation
python --version
pip --version
```

**macOS:**
```bash
# Install using Homebrew
brew install python3

# Or download from python.org

# Verify installation
python3 --version
pip3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip

# Verify installation
python3 --version
pip3 --version
```

### 2. Webcam

- Built-in laptop camera, or
- USB webcam
- Ensure camera is functional and accessible

### 3. System Permissions

**macOS:**
- System Preferences → Security & Privacy → Camera
- Allow Terminal/Python to access camera

**Windows:**
- Settings → Privacy → Camera
- Enable camera access for desktop apps

**Linux:**
- Ensure user is in `video` group:
```bash
sudo usermod -a -G video $USER
```

## 🚀 Installation Steps

### Method 1: Using requirements.txt (Recommended)

```bash
# Navigate to project directory
cd c:/Users/aksha/OneDrive/Desktop/VirtualMouse

# Install all dependencies
pip install -r requirements.txt
```

### Method 2: Manual Installation

```bash
# Install each package individually
pip install opencv-python
pip install mediapipe
pip install pyautogui
pip install numpy
```

### Method 3: Using Virtual Environment (Best Practice)

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🔍 Verify Installation

### Test Python Packages

```python
# Run this in Python shell
python

>>> import cv2
>>> import mediapipe
>>> import pyautogui
>>> import numpy
>>> print("All packages installed successfully!")
>>> exit()
```

### Test Camera Access

```python
# Run this test script
python

>>> import cv2
>>> cap = cv2.VideoCapture(0)
>>> ret, frame = cap.read()
>>> print(f"Camera working: {ret}")
>>> cap.release()
>>> exit()
```

## ⚙️ Platform-Specific Setup

### Windows

**1. Install Visual C++ Redistributable** (if needed)
- Download from Microsoft website
- Required for OpenCV

**2. Disable PyAutoGUI Fail-Safe** (already done in code)
```python
# In mouse_controller.py
pyautogui.FAILSAFE = False
```

**3. Run with Administrator** (if mouse control doesn't work)
- Right-click Python script
- Select "Run as administrator"

### macOS

**1. Grant Accessibility Permissions**
```bash
# System Preferences → Security & Privacy → Accessibility
# Add Terminal or your Python IDE
```

**2. Install Xcode Command Line Tools** (if needed)
```bash
xcode-select --install
```

**3. Camera Permission**
```bash
# First run will prompt for camera access
# Click "Allow"
```

### Linux

**1. Install Additional Dependencies**
```bash
# Ubuntu/Debian
sudo apt install python3-tk python3-dev

# Fedora
sudo dnf install python3-tkinter python3-devel

# Arch
sudo pacman -S tk
```

**2. Install X11 Development Files** (for PyAutoGUI)
```bash
sudo apt install python3-xlib
```

**3. Grant Camera Access**
```bash
# Add user to video group
sudo usermod -a -G video $USER

# Log out and log back in
```

## 🧪 Test Run

### Basic Test

```bash
# Run the application
python virtual_mouse.py

# You should see:
# - Camera feed window opens
# - Hand landmarks appear when hand is visible
# - FPS counter in top-left
# - Gesture status updates
```

### Gesture Test Checklist

- [ ] Camera opens successfully
- [ ] Hand landmarks appear (green skeleton)
- [ ] Cursor moves with index finger
- [ ] Left click works (index + thumb pinch)
- [ ] Right click works (middle + thumb pinch)
- [ ] Drag works (hold pinch)
- [ ] Scroll works (two fingers vertical)
- [ ] Press 'Q' to quit

## 🐛 Installation Troubleshooting

### Error: "No module named 'cv2'"

```bash
# Uninstall and reinstall OpenCV
pip uninstall opencv-python
pip install opencv-python
```

### Error: "No module named 'mediapipe'"

```bash
# MediaPipe may not be available for all Python versions
# Use Python 3.7 - 3.10 (recommended: 3.9)

# Check Python version
python --version

# Install MediaPipe
pip install mediapipe
```

### Error: "ImportError: DLL load failed" (Windows)

```bash
# Install Visual C++ Redistributable
# Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe

# Or install via pip
pip install --upgrade opencv-python
```

### Error: "Camera not found"

```bash
# Test different camera indices
# Edit config.py:
CAMERA_INDEX = 0  # Try 0, 1, 2, etc.

# List available cameras (Windows)
# Run this Python script:
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i}: Available")
        cap.release()
    else:
        print(f"Camera {i}: Not available")
```

### Error: "PyAutoGUI not working on Linux"

```bash
# Install X11 dependencies
sudo apt install python3-tk python3-dev python3-xlib

# Install PyAutoGUI with X11 support
pip install python-xlib
pip install pyautogui
```

### Error: "Permission denied" (macOS)

```bash
# Grant accessibility permissions
# System Preferences → Security & Privacy → Privacy
# Select "Accessibility" and add Terminal/Python

# Grant camera permissions
# System Preferences → Security & Privacy → Privacy
# Select "Camera" and enable for Terminal/Python
```

## 🔄 Updating Dependencies

```bash
# Update all packages to latest versions
pip install --upgrade opencv-python mediapipe pyautogui numpy

# Or update from requirements.txt
pip install --upgrade -r requirements.txt
```

## 🗑️ Uninstallation

```bash
# Uninstall all packages
pip uninstall opencv-python mediapipe pyautogui numpy

# Remove virtual environment (if used)
# Windows
rmdir /s venv

# macOS/Linux
rm -rf venv
```

## 📦 Offline Installation

If you need to install on a machine without internet:

**1. Download packages on internet-connected machine:**
```bash
pip download -r requirements.txt -d packages/
```

**2. Transfer `packages/` folder to offline machine**

**3. Install from local packages:**
```bash
pip install --no-index --find-links=packages/ -r requirements.txt
```

## 🎯 Quick Installation Script

**Windows (PowerShell):**
```powershell
# Save as install.ps1
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
Write-Host "Installation complete! Run: python virtual_mouse.py"
```

**macOS/Linux (Bash):**
```bash
# Save as install.sh
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Installation complete! Run: python virtual_mouse.py"
```

## ✅ Installation Complete!

If all tests pass, you're ready to use the Virtual Mouse System!

**Next Steps:**
1. Read `README.md` for usage instructions
2. Review `config.py` for customization options
3. Check `DOCUMENTATION.md` for technical details
4. Run `python virtual_mouse.py` to start

---

**Need Help?**
- Enable `DEBUG_MODE = True` in `config.py`
- Check error messages carefully
- Verify all dependencies are installed
- Ensure camera permissions are granted
