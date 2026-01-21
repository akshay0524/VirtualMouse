"""
Mouse Controller Module for Virtual Mouse System
================================================
This module handles all system-level mouse control operations including
cursor movement, clicking, dragging, and scrolling.

Author: Senior CV Engineer
Date: 2026-01-21
"""

import pyautogui
import numpy as np
from typing import Tuple, Optional
import config


class MouseController:
    """
    System mouse controller with gesture-based actions.
    
    This class provides a clean interface for controlling the system mouse
    cursor using coordinates from the hand tracker.
    """
    
    def __init__(self):
        """Initialize mouse controller and get screen dimensions."""
        # Get screen resolution
        self.screen_width, self.screen_height = pyautogui.size()
        
        # PyAutoGUI safety settings
        # Disable fail-safe (moving mouse to corner won't raise exception)
        # Set to True during development for safety
        pyautogui.FAILSAFE = False
        
        # CRITICAL: Disable the built-in 0.1 second pause after every PyAutoGUI call
        # This eliminates "stutter" and makes movement butter smooth
        pyautogui.PAUSE = 0
        
        # State tracking
        self.is_dragging = False
        self.drag_start_pos = None
        
        # Cooldown counters for debouncing
        self.left_click_cooldown = 0
        self.right_click_cooldown = 0
        self.double_click_cooldown = 0
        self.scroll_cooldown = 0
        self.drag_hold_counter = 0
        
        # Previous scroll position for delta calculation
        self.previous_scroll_y = None
        
        if config.DEBUG_MODE:
            print(f"Screen resolution: {self.screen_width}x{self.screen_height}")
    
    def map_coordinates(self, camera_x: int, camera_y: int, 
                       camera_width: int, camera_height: int) -> Tuple[int, int]:
        """
        Map camera coordinates to screen coordinates.
        
        This function:
        1. Flips X coordinate (camera is mirrored)
        2. Applies frame reduction to prevent edge sticking
        3. Maps to screen resolution
        4. Applies cursor speed multiplier
        
        Args:
            camera_x: X coordinate from camera (0 to camera_width)
            camera_y: Y coordinate from camera (0 to camera_height)
            camera_width: Width of camera frame
            camera_height: Height of camera frame
            
        Returns:
            Tuple of (screen_x, screen_y) coordinates
        """
        # Flip X coordinate for natural mirror effect
        # REMOVED: Camera frame is already flipped in virtual_mouse.py
        # camera_x = camera_width - camera_x
        
        # Apply frame reduction to create usable area
        # This prevents cursor from getting stuck at screen edges
        reduced_width = camera_width - 2 * config.FRAME_REDUCTION
        reduced_height = camera_height - 2 * config.FRAME_REDUCTION
        
        # Normalize to 0-1 range within reduced frame
        norm_x = (camera_x - config.FRAME_REDUCTION) / reduced_width
        norm_y = (camera_y - config.FRAME_REDUCTION) / reduced_height
        
        # Clamp to valid range
        norm_x = max(0.0, min(1.0, norm_x))
        norm_y = max(0.0, min(1.0, norm_y))
        
        # Map to screen coordinates
        screen_x = int(norm_x * self.screen_width * config.CURSOR_SPEED)
        screen_y = int(norm_y * self.screen_height * config.CURSOR_SPEED)
        
        # Ensure coordinates are within screen bounds
        screen_x = max(0, min(self.screen_width - 1, screen_x))
        screen_y = max(0, min(self.screen_height - 1, screen_y))
        
        return (screen_x, screen_y)
    
    def move_cursor(self, camera_pos: Tuple[int, int], 
                   camera_width: int, camera_height: int):
        """
        Move cursor to position based on camera coordinates.
        
        Args:
            camera_pos: (x, y) position from camera
            camera_width: Width of camera frame
            camera_height: Height of camera frame
        """
        # Map camera coordinates to screen coordinates
        screen_x, screen_y = self.map_coordinates(
            camera_pos[0], camera_pos[1],
            camera_width, camera_height
        )
        
        # Move cursor instantly (duration=0)
        pyautogui.moveTo(screen_x, screen_y, duration=0)
    
    def update_cooldowns(self):
        """
        Update all cooldown counters.
        
        This should be called once per frame to decrement cooldown timers.
        """
        if self.left_click_cooldown > 0:
            self.left_click_cooldown -= 1
            
        if self.right_click_cooldown > 0:
            self.right_click_cooldown -= 1
            
        if self.double_click_cooldown > 0:
            self.double_click_cooldown -= 1
            
        if self.scroll_cooldown > 0:
            self.scroll_cooldown -= 1
    
    def left_click(self) -> bool:
        """
        Perform left click if not in cooldown.
        
        Returns:
            True if click was performed, False if in cooldown
        """
        if self.left_click_cooldown > 0:
            return False
            
        # Perform click
        pyautogui.click()
        
        # Set cooldown
        self.left_click_cooldown = config.CLICK_COOLDOWN_FRAMES
        
        if config.DEBUG_MODE:
            print("Left click performed")
            
        return True
    
    def right_click(self) -> bool:
        """
        Perform right click if not in cooldown.
        
        Returns:
            True if click was performed, False if in cooldown
        """
        if self.right_click_cooldown > 0:
            return False
            
        # Perform right click
        pyautogui.rightClick()
        
        # Set cooldown
        self.right_click_cooldown = config.CLICK_COOLDOWN_FRAMES
        
        if config.DEBUG_MODE:
            print("Right click performed")
            
        return True

    def double_click(self) -> bool:
        """
        Perform double click if not in cooldown.
        
        Returns:
            True if click was performed, False if in cooldown
        """
        if self.double_click_cooldown > 0:
            return False
            
        # Perform double click
        pyautogui.doubleClick()
        
        # Set cooldown
        self.double_click_cooldown = config.CLICK_COOLDOWN_FRAMES
        
        if config.DEBUG_MODE:
            print("Double click performed")
            
        return True
    
    def start_drag(self):
        """
        Start drag operation.
        
        This holds down the left mouse button.
        """
        if not self.is_dragging:
            pyautogui.mouseDown()
            self.is_dragging = True
            self.drag_start_pos = pyautogui.position()
            
            if config.DEBUG_MODE:
                print(f"Drag started at {self.drag_start_pos}")
    
    def stop_drag(self):
        """
        Stop drag operation.
        
        This releases the left mouse button.
        """
        if self.is_dragging:
            pyautogui.mouseUp()
            drag_end_pos = pyautogui.position()
            self.is_dragging = False
            
            if config.DEBUG_MODE:
                print(f"Drag stopped at {drag_end_pos}")
            
            self.drag_start_pos = None
    
    def handle_drag_gesture(self, is_pinching: bool):
        """
        Handle drag gesture with activation delay.
        
        This prevents accidental drags from quick clicks by requiring
        the pinch to be held for a minimum number of frames.
        
        Args:
            is_pinching: Whether the drag gesture is currently active
        """
        if is_pinching:
            # Increment hold counter
            self.drag_hold_counter += 1
            
            # Start drag after activation delay
            if self.drag_hold_counter >= config.DRAG_ACTIVATION_FRAMES:
                self.start_drag()
        else:
            # Reset counter and stop drag
            self.drag_hold_counter = 0
            if self.is_dragging:
                self.stop_drag()
    
    def scroll(self, amount: int) -> bool:
        """
        Perform scroll if not in cooldown.
        
        Args:
            amount: Scroll amount (positive = up, negative = down)
            
        Returns:
            True if scroll was performed, False if in cooldown or amount is 0
        """
        if self.scroll_cooldown > 0 or amount == 0:
            return False
            
        # Perform scroll
        # PyAutoGUI scroll: positive = up, negative = down
        pyautogui.scroll(amount)
        
        # Set cooldown
        self.scroll_cooldown = config.SCROLL_COOLDOWN_FRAMES
        
        if config.DEBUG_MODE:
            print(f"Scrolled: {amount}")
            
        return True
    
    def scroll_vertical(self, current_y: int) -> bool:
        """
        Scroll based on vertical hand movement.
        
        Args:
            current_y: Current Y position of scroll reference point
            
        Returns:
            True if scroll was performed, False otherwise
        """
        if self.previous_scroll_y is None:
            self.previous_scroll_y = current_y
            return False
            
        # Calculate vertical movement
        delta_y = self.previous_scroll_y - current_y
        
        # Convert to scroll amount
        # Positive delta = hand moved up = scroll up
        # Use SCROLL_SENSITIVITY from config (higher = less movement needed)
        scroll_amount = int(delta_y * config.SCROLL_SENSITIVITY)
        
        # Update previous position
        self.previous_scroll_y = current_y
        
        # Perform scroll
        return self.scroll(scroll_amount)
    
    def reset_scroll_tracking(self):
        """Reset scroll position tracking."""
        self.previous_scroll_y = None
    
    def get_current_position(self) -> Tuple[int, int]:
        """
        Get current cursor position.
        
        Returns:
            Tuple of (x, y) screen coordinates
        """
        return pyautogui.position()
    
    def emergency_stop(self):
        """
        Emergency stop all mouse operations.
        
        This releases any held buttons and resets state.
        """
        if self.is_dragging:
            self.stop_drag()
            
        self.drag_hold_counter = 0
        self.left_click_cooldown = 0
        self.right_click_cooldown = 0
        self.scroll_cooldown = 0
        self.reset_scroll_tracking()
        
        if config.DEBUG_MODE:
            print("Emergency stop executed")
