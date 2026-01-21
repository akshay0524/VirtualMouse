# 🚀 Quick Start Guide - Virtual Mouse System

Get up and running in 2 minutes!

## ⚡ Installation (One Command)

```bash
pip install -r requirements.txt
```

## ▶️ Run

```bash
python virtual_mouse.py
```

## 🎮 Controls

| Gesture | Action | How To |
|---------|--------|--------|
| 👆 **Point** | Move Cursor | Extend index finger |
| 👌 **Index Pinch** | Left Click | Touch index finger to thumb |
| 🤏 **Middle Pinch** | Right Click | Touch middle finger to thumb |
| ✊ **Hold Pinch** | Drag & Drop | Hold index+thumb pinch while moving |
| ✌️ **Two Fingers** | Scroll | Extend index+middle, move up/down |

## 🎯 Tips for Best Results

### ✅ DO:
- Use good lighting (natural or bright indoor light)
- Keep hand 30-60cm from camera
- Keep hand flat and fingers spread
- Stay within the blue rectangle boundary
- Make deliberate, clear gestures

### ❌ DON'T:
- Use in dim lighting
- Move hand too fast
- Make ambiguous gestures
- Cover camera or use cluttered background
- Wear gloves (may reduce accuracy)

## ⚙️ Quick Settings (Optimized "Turbo" Defaults)

We have pre-tuned `config.py` for maximum speed and accuracy:

```python
# Speed & Responsiveness
MODEL_COMPLEXITY = 0        # Lite model (Fastest)
SMOOTHING_FACTOR = 0.15     # Low latency (Snappy cursor)

# Gesture Accuracy
DRAG_THRESHOLD = 0.06       # "Sticky" drag (Prevents dropping)
SCROLL_THRESHOLD = 0.20     # Strict scroll (Prevents accidental scrolls)
SCROLL_SENSITIVITY = 15     # Smooth scrolling
```

### To Customize Further:
Edit `config.py` to adjust:

```python
# Make cursor smoother (slower response)
SMOOTHING_FACTOR = 0.3

# Make cursor faster (more jittery)
SMOOTHING_FACTOR = 0.1

# Reduce sensitivity (harder to click)
LEFT_CLICK_THRESHOLD = 0.04
```

## 🐛 Common Issues

### Camera won't open
```python
# Try different camera index in config.py
CAMERA_INDEX = 1  # or 2, 3, etc.
```

### Gestures not working
- Check lighting
- Lower thresholds in config.py
- Ensure hand is within blue rectangle

### Low FPS / Lag
```python
# In config.py
FRAME_SKIP = 2
MODEL_COMPLEXITY = 0
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
```

### Cursor too sensitive
```python
# In config.py
SMOOTHING_FACTOR = 0.3  # Lower = smoother
```

## 🔑 Keyboard Shortcuts

- **Q**: Quit application
- **R**: Reset system state

## 📊 Performance Expectations

| Hardware | Expected FPS | Responsiveness |
|----------|-------------|----------------|
| Modern Laptop | 25-35 FPS | Excellent |
| Mid-range PC | 20-30 FPS | Good |
| Older Hardware | 15-25 FPS | Acceptable |

## 🎓 Learning Curve

- **5 minutes**: Basic cursor movement
- **10 minutes**: Comfortable with all gestures
- **30 minutes**: Proficient user
- **1 hour**: Expert level control

## 📞 Need Help?

1. Check `README.md` for detailed info
2. Read `INSTALLATION.md` for setup issues
3. Review `DOCUMENTATION.md` for technical details
4. Enable `DEBUG_MODE = True` in `config.py`

## 🎉 You're Ready!

Run the application and start controlling your computer with hand gestures!

```bash
python virtual_mouse.py
```

---

**Pro Tip:** Practice each gesture individually before combining them. Start with cursor movement, then add clicks, then drag, then scroll.
