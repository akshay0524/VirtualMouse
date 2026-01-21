"""
Hand Tracking Module for Virtual Mouse System
==============================================
This module handles all hand detection and gesture recognition using MediaPipe.
It provides clean interfaces for detecting various hand gestures.

Author: Senior CV Engineer
Date: 2026-01-21
"""

import cv2
import numpy as np
import math
from typing import Tuple, Optional, List
import config

# Simple MediaPipe import - works with 0.10.31
try:
    from mediapipe import solutions
    mp_hands = solutions.hands
    mp_drawing = solutions.drawing_utils
    mp_drawing_styles = solutions.drawing_styles
except Exception as e:
    print(f"Error importing MediaPipe: {e}")
    raise


class HandTracker:
    """
    Hand tracking and gesture recognition class.
    
    This class encapsulates all MediaPipe hand detection logic and provides
    methods for detecting specific gestures like pinches, scrolls, etc.
    """
    
    def __init__(self):
        """Initialize MediaPipe Hands and tracking variables."""
        # Initialize MediaPipe Hands using solutions API
        self.mp_hands = mp_hands
        self.mp_drawing = mp_drawing
        self.mp_drawing_styles = mp_drawing_styles
        
        # Create Hands object with configuration
        self.hands = self.mp_hands.Hands(
            static_image_mode=config.STATIC_IMAGE_MODE,
            max_num_hands=config.MAX_NUM_HANDS,
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE,
            model_complexity=config.MODEL_COMPLEXITY
        )
        
        # Tracking state variables
        self.previous_index_pos = None  # For cursor smoothing
        self.landmarks = None  # Current frame landmarks
        self.hand_detected = False  # Whether a hand is currently detected
        
    def find_hands(self, frame: np.ndarray, draw: bool = True) -> np.ndarray:
        """
        Detect hands in the frame and optionally draw landmarks.
        
        Args:
            frame: Input BGR image from webcam
            draw: Whether to draw hand landmarks on the frame
            
        Returns:
            Processed frame with optional landmark drawings
        """
        # Convert BGR to RGB (MediaPipe uses RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame to detect hands
        # Setting writeable=False improves performance by passing by reference
        rgb_frame.flags.writeable = False
        results = self.hands.process(rgb_frame)
        rgb_frame.flags.writeable = True
        
        # Store detection results
        self.hand_detected = results.multi_hand_landmarks is not None
        
        if self.hand_detected:
            # Store the first hand's landmarks
            self.landmarks = results.multi_hand_landmarks[0]
            
            # Draw landmarks if requested
            if draw and config.SHOW_LANDMARKS:
                self.mp_drawing.draw_landmarks(
                    frame,
                    self.landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
        else:
            self.landmarks = None
            
        return frame
    
    def get_landmark_position(self, landmark_id: int, 
                             frame_shape: Tuple[int, int, int]) -> Optional[Tuple[int, int]]:
        """
        Get pixel coordinates of a specific landmark.
        
        Args:
            landmark_id: MediaPipe landmark index (0-20)
            frame_shape: Shape of the frame (height, width, channels)
            
        Returns:
            Tuple of (x, y) pixel coordinates, or None if no hand detected
        """
        if not self.hand_detected or self.landmarks is None:
            return None
            
        # Get normalized landmark coordinates (0.0 to 1.0)
        landmark = self.landmarks.landmark[landmark_id]
        
        # Convert to pixel coordinates
        h, w, _ = frame_shape
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        
        return (x, y)
    
    def get_all_landmarks(self, frame_shape: Tuple[int, int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Get pixel coordinates of all 21 hand landmarks.
        
        Args:
            frame_shape: Shape of the frame (height, width, channels)
            
        Returns:
            List of (x, y) tuples for all landmarks, or None if no hand detected
        """
        if not self.hand_detected or self.landmarks is None:
            return None
            
        h, w, _ = frame_shape
        positions = []
        
        for landmark in self.landmarks.landmark:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            positions.append((x, y))
            
        return positions
    
    def calculate_distance(self, point1_id: int, point2_id: int) -> Optional[float]:
        """
        Calculate Euclidean distance between two landmarks.
        
        This uses normalized coordinates (0.0 to 1.0) so the distance is
        independent of frame resolution.
        
        Args:
            point1_id: First landmark index
            point2_id: Second landmark index
            
        Returns:
            Normalized distance between the two points, or None if no hand detected
        """
        if not self.hand_detected or self.landmarks is None:
            return None
            
        # Get normalized coordinates
        p1 = self.landmarks.landmark[point1_id]
        p2 = self.landmarks.landmark[point2_id]
        
        # Calculate Euclidean distance in normalized space
        distance = math.sqrt(
            (p1.x - p2.x) ** 2 + 
            (p1.y - p2.y) ** 2 + 
            (p1.z - p2.z) ** 2  # Include z-depth for better accuracy
        )
        
        if config.PRINT_DISTANCES:
            print(f"Distance between {point1_id} and {point2_id}: {distance:.4f}")
            
        return distance
    
    def is_pinching(self, finger_tip_id: int, threshold: float) -> bool:
        """
        Detect if a finger is pinching with the thumb.
        
        Args:
            finger_tip_id: Landmark ID of the finger tip (e.g., INDEX_TIP)
            threshold: Distance threshold for pinch detection
            
        Returns:
            True if pinching, False otherwise
        """
        distance = self.calculate_distance(config.HandLandmark.THUMB_TIP, finger_tip_id)
        
        if distance is None:
            return False
            
        return distance < threshold
    
    def get_cursor_position(self, frame_shape: Tuple[int, int, int]) -> Optional[Tuple[int, int]]:
        """
        Get smoothed cursor position based on index finger tip.
        
        This implements exponential moving average for smooth cursor movement.
        
        Args:
            frame_shape: Shape of the frame (height, width, channels)
            
        Returns:
            Smoothed (x, y) pixel coordinates, or None if no hand detected
        """
        current_pos = self.get_landmark_position(config.HandLandmark.INDEX_TIP, frame_shape)
        
        if current_pos is None:
            self.previous_index_pos = None
            return None
            
        # Apply smoothing using exponential moving average
        if self.previous_index_pos is None:
            # First detection, no smoothing needed
            smoothed_pos = current_pos
        else:
            # Smooth the movement
            # new_pos = alpha * current + (1 - alpha) * previous
            alpha = config.SMOOTHING_FACTOR
            smoothed_x = int(alpha * current_pos[0] + (1 - alpha) * self.previous_index_pos[0])
            smoothed_y = int(alpha * current_pos[1] + (1 - alpha) * self.previous_index_pos[1])
            smoothed_pos = (smoothed_x, smoothed_y)
            
        # Update previous position
        self.previous_index_pos = smoothed_pos
        
        return smoothed_pos
    
    def detect_left_click(self) -> bool:
        """
        Detect left click gesture (index finger + thumb pinch).
        
        Returns:
            True if left click gesture detected, False otherwise
        """
        return self.is_pinching(config.HandLandmark.INDEX_TIP, config.LEFT_CLICK_THRESHOLD)
    
    def detect_right_click(self) -> bool:
        """
        Detect right click gesture (middle finger + thumb pinch).
        
        Returns:
            True if right click gesture detected, False otherwise
        """
        return self.is_pinching(config.HandLandmark.MIDDLE_TIP, config.RIGHT_CLICK_THRESHOLD)

    def detect_double_click(self) -> bool:
        """
        Detect double click gesture (ring finger + thumb pinch).
        
        Returns:
            True if double click gesture detected, False otherwise
        """
        return self.is_pinching(config.HandLandmark.RING_TIP, config.DOUBLE_CLICK_THRESHOLD)
    
    def detect_drag(self) -> bool:
        """
        Detect drag gesture (same as left click, but held).
        
        Returns:
            True if drag gesture detected, False otherwise
        """
        return self.is_pinching(config.HandLandmark.INDEX_TIP, config.DRAG_THRESHOLD)
        
    def detect_one_finger_gesture(self) -> bool:
        """
        Detect if strictly ONLY the index finger is extended.
        (Middle, Ring, Pinky must be curled).
        
        Returns:
            True if only index finger is shown
        """
        if not self.hand_detected or self.landmarks is None:
            return False
            
        # Helper to check if finger is curled (Tip below PIP joint)
        def is_curled(tip_idx, pip_idx):
            # Note: in MediaPipe, Y increases downwards. 
            # So Tip Y > PIP Y means tip is below knuckle (curled)
            return self.landmarks.landmark[tip_idx].y > self.landmarks.landmark[pip_idx].y

        # Check Index is extended (Tip above PIP)
        index_extended = self.landmarks.landmark[config.HandLandmark.INDEX_TIP].y < \
                        self.landmarks.landmark[config.HandLandmark.INDEX_PIP].y
                        
        # Check others are curled
        middle_curled = is_curled(config.HandLandmark.MIDDLE_TIP, config.HandLandmark.MIDDLE_PIP)
        ring_curled = is_curled(config.HandLandmark.RING_TIP, config.HandLandmark.RING_PIP)
        pinky_curled = is_curled(config.HandLandmark.PINKY_TIP, config.HandLandmark.PINKY_PIP)
        
        return index_extended and middle_curled and ring_curled and pinky_curled
    
    def detect_scroll(self) -> Optional[str]:
        """
        Detect scroll gesture (two fingers extended vertically).
        
        This checks if index and middle fingers are extended and separated,
        indicating a scroll gesture.
        
        Returns:
            'ready' if fingers are in scroll position, None otherwise
        """
        if not self.hand_detected:
            return None
            
        # Calculate distance between index and middle finger tips
        distance = self.calculate_distance(
            config.HandLandmark.INDEX_TIP,
            config.HandLandmark.MIDDLE_TIP
        )
        
        if distance is None:
            return None
            
        # Check if fingers are sufficiently separated for scroll
        if distance > config.SCROLL_THRESHOLD:
            return 'ready'
            
        return None
    
    def get_scroll_amount(self, frame_shape: Tuple[int, int, int]) -> Optional[int]:
        """
        Calculate scroll amount based on middle finger vertical movement.
        
        Args:
            frame_shape: Shape of the frame (height, width, channels)
            
        Returns:
            Scroll amount in pixels (positive = up, negative = down), or None
        """
        # Get middle finger position
        middle_pos = self.get_landmark_position(config.HandLandmark.MIDDLE_TIP, frame_shape)
        
        if middle_pos is None:
            return None
            
        # Calculate scroll based on vertical position
        # Top of frame = scroll up, bottom = scroll down
        h, w, _ = frame_shape
        center_y = h // 2
        
        # Distance from center, normalized
        distance_from_center = (center_y - middle_pos[1]) / h
        
        # Convert to scroll amount
        scroll_amount = int(distance_from_center * config.SCROLL_SENSITIVITY * 10)
        
        return scroll_amount
    
    def release(self):
        """Release MediaPipe resources."""
        if self.hands:
            self.hands.close()
