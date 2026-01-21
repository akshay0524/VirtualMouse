"""
Configuration Module for Virtual Mouse System
==============================================
This module contains all configurable parameters for the virtual mouse system.
Adjust these values to fine-tune gesture sensitivity, performance, and behavior.

Author: Senior CV Engineer
Date: 2026-01-21
"""

# ============================================================================
# CAMERA SETTINGS
# ============================================================================
CAMERA_INDEX = 0  # Default webcam (0 = primary, 1 = secondary, etc.)
CAMERA_WIDTH = 640  # Frame width in pixels
CAMERA_HEIGHT = 480  # Frame height in pixels
CAMERA_FPS = 30  # Target frames per second

# ============================================================================
# MEDIAPIPE HAND DETECTION SETTINGS
# ============================================================================
# Detection confidence: Higher = more accurate but slower (0.0 to 1.0)
MIN_DETECTION_CONFIDENCE = 0.6

# Tracking confidence: Higher = more stable tracking (0.0 to 1.0)
MIN_TRACKING_CONFIDENCE = 0.6

# Maximum number of hands to detect (1 or 2)
# Using 1 hand for better performance and simpler gesture logic
MAX_NUM_HANDS = 1

# ============================================================================
# CURSOR MOVEMENT SETTINGS
# ============================================================================
# ============================================================================
# CURSOR MOVEMENT SETTINGS
# ============================================================================
# ============================================================================
# CURSOR MOVEMENT SETTINGS
# ============================================================================
# Smoothing factor for cursor movement (0.0 to 1.0)
# Lower = smoother but slower response, Higher = faster but more jittery
# 0.15 is the "Goldilocks" zone - stable but responsive
SMOOTHING_FACTOR = 0.15

# Frame reduction for cursor control area
# This creates a "dead zone" at screen edges to prevent cursor from getting stuck
FRAME_REDUCTION = 100  # pixels to reduce from each edge

# Cursor speed multiplier (adjust if cursor feels too slow/fast)
CURSOR_SPEED = 1.0

# ============================================================================
# GESTURE DETECTION THRESHOLDS
# ============================================================================
# Distance thresholds are normalized (0.0 to 1.0 relative to hand size)

# ============================================================================
# GESTURE DETECTION THRESHOLDS
# ============================================================================
# Distance thresholds are normalized (0.0 to 1.0 relative to hand size)

# Left Click: Index finger + Thumb pinch
LEFT_CLICK_THRESHOLD = 0.07  # Precise clicking (harder to misfire than 0.10)

# Right Click: Middle finger + Thumb pinch
RIGHT_CLICK_THRESHOLD = 0.07  # Precise clicking

# Double Click: DISABLED for simplicity and reliability
# (Ring finger tracking was causing conflicts with middle finger)
# To double click, simply pinch Index+Thumb twice quickly.

# Drag: DISABLED per user request (was causing accidental drags)
# DRAG_THRESHOLD = 0.12  
DRAG_THRESHOLD = 99.9  # Set to high value to effectively disable if logic remains

# Scroll: Two fingers vertical movement
SCROLL_THRESHOLD = 0.10  # Very easy activation (Left as is, working well)
SCROLL_SENSITIVITY = 15  # Controlled scroll (Lower = slower)

# ============================================================================
# GESTURE DEBOUNCING
# ============================================================================
# Prevents multiple unintended clicks from a single gesture

# Minimum frames between click gestures
CLICK_COOLDOWN_FRAMES = 8  # Balanced (prevents spamming but still fast)

# Minimum frames between scroll actions
SCROLL_COOLDOWN_FRAMES = 5  # Slower updates for smoother visual feel

# Drag activation delay (frames to hold pinch before drag starts)
DRAG_ACTIVATION_FRAMES = 5  # Reduce accidental drags

# ============================================================================
# VISUAL FEEDBACK SETTINGS
# ============================================================================
# Display settings for the camera feed window

# Show hand landmarks and connections
# ENABLED: User requested green skeleton
SHOW_LANDMARKS = True

# Show gesture status text on screen
SHOW_GESTURE_STATUS = True

# Show FPS counter
SHOW_FPS = True

# Colors (BGR format for OpenCV)
COLOR_HAND_LANDMARKS = (0, 255, 0)  # Green
COLOR_HAND_CONNECTIONS = (255, 255, 255)  # White
COLOR_GESTURE_TEXT = (0, 255, 255)  # Yellow
COLOR_FPS_TEXT = (255, 0, 255)  # Magenta
COLOR_BACKGROUND = (0, 0, 0)  # Black

# Text settings
FONT = 1  # cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
FONT_THICKNESS = 2

# ============================================================================
# PERFORMANCE OPTIMIZATION
# ============================================================================
# Skip frames for processing (1 = process every frame, 2 = every other frame)
FRAME_SKIP = 1  # Process every frame for maximum responsiveness

# Use static image mode (False for video, True for single images)
STATIC_IMAGE_MODE = False

# Model complexity (0 = lite, 1 = full)
# Lite model is faster but slightly less accurate
MODEL_COMPLEXITY = 0

# ============================================================================
# HAND LANDMARK INDICES
# ============================================================================
# MediaPipe hand landmark indices for easy reference
# These are constants and should not be modified

class HandLandmark:
    """
    MediaPipe Hand Landmark indices.
    
    Hand landmarks are numbered 0-20:
    - 0: WRIST
    - 1-4: THUMB (CMC, MCP, IP, TIP)
    - 5-8: INDEX (MCP, PIP, DIP, TIP)
    - 9-12: MIDDLE (MCP, PIP, DIP, TIP)
    - 13-16: RING (MCP, PIP, DIP, TIP)
    - 17-20: PINKY (MCP, PIP, DIP, TIP)
    """
    WRIST = 0
    
    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4
    
    INDEX_MCP = 5
    INDEX_PIP = 6
    INDEX_DIP = 7
    INDEX_TIP = 8
    
    MIDDLE_MCP = 9
    MIDDLE_PIP = 10
    MIDDLE_DIP = 11
    MIDDLE_TIP = 12
    
    RING_MCP = 13
    RING_PIP = 14
    RING_DIP = 15
    RING_TIP = 16
    
    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20

# ============================================================================
# DEBUGGING
# ============================================================================
# Enable verbose logging for troubleshooting
DEBUG_MODE = False

# Print distance values for threshold tuning
PRINT_DISTANCES = False
