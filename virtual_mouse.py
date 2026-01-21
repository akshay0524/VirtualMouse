"""
Virtual Mouse System - Main Application
========================================
Real-time hand gesture-based mouse control using computer vision.

This application uses:
- OpenCV for webcam capture and display
- MediaPipe for hand landmark detection
- PyAutoGUI for system mouse control

Features:
- Cursor movement (index finger tracking)
- Left click (index + thumb pinch)
- Right click (middle + thumb pinch)
- Drag & drop (hold pinch)
- Scroll (two fingers vertical movement)

Author: Senior CV Engineer
Date: 2026-01-21
"""

import cv2
import time
import numpy as np
from typing import Optional
import config
from hand_tracker import HandTracker
from mouse_controller import MouseController


class VirtualMouse:
    """
    Main application class for the virtual mouse system.
    
    This class orchestrates the hand tracker and mouse controller,
    managing the main application loop and gesture state machine.
    """
    
    def __init__(self):
        """Initialize the virtual mouse system."""
        print("=" * 60)
        print("Virtual Mouse System Initializing...")
        print("=" * 60)
        
        # Initialize components
        self.hand_tracker = HandTracker()
        self.mouse_controller = MouseController()
        
        # Initialize webcam
        self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, config.CAMERA_FPS)
        
        # Verify camera opened successfully
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera. Please check camera connection.")
        
        # Get actual camera dimensions
        self.camera_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.camera_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"Camera initialized: {self.camera_width}x{self.camera_height}")
        print(f"Screen resolution: {self.mouse_controller.screen_width}x{self.mouse_controller.screen_height}")
        
        # FPS calculation
        self.prev_time = 0
        self.fps = 0
        
        # Frame counter for frame skipping
        self.frame_count = 0
        
        # Gesture state tracking
        self.current_gesture = "None"
        self.gesture_performed = False
        
        # Scroll state
        self.scroll_active = False
        self.scroll_activation_start = 0
        
        print("\nSystem ready!")
        print("\nGesture Controls:")
        print("  • Move cursor: Point with index finger")
        print("  • Left click: Pinch index finger + thumb")
        print("  • Right click: Pinch middle finger + thumb")
        print("  • Scroll: Extend index + middle fingers, move vertically")
        print("\nPress 'Q' to quit")
        print("=" * 60)
    
    def calculate_fps(self) -> float:
        """
        Calculate current FPS.
        
        Returns:
            Current frames per second
        """
        current_time = time.time()
        fps = 1 / (current_time - self.prev_time) if self.prev_time > 0 else 0
        self.prev_time = current_time
        return fps
    
    def draw_ui(self, frame: np.ndarray):
        """
        Draw UI elements on the frame.
        
        Args:
            frame: Frame to draw on
        """
        # Draw FPS
        if config.SHOW_FPS:
            fps_text = f"FPS: {int(self.fps)}"
            cv2.putText(
                frame, fps_text,
                (10, 30),
                config.FONT, config.FONT_SCALE,
                config.COLOR_FPS_TEXT, config.FONT_THICKNESS
            )
        
        # Draw gesture status
        if config.SHOW_GESTURE_STATUS:
            gesture_text = f"Gesture: {self.current_gesture}"
            cv2.putText(
                frame, gesture_text,
                (10, 60),
                config.FONT, config.FONT_SCALE,
                config.COLOR_GESTURE_TEXT, config.FONT_THICKNESS
            )
            
            # Draw drag status
            if self.mouse_controller.is_dragging:
                drag_text = "DRAGGING"
                cv2.putText(
                    frame, drag_text,
                    (10, 90),
                    config.FONT, config.FONT_SCALE,
                    (0, 0, 255), config.FONT_THICKNESS
                )
        
        # Draw control area boundary
        cv2.rectangle(
            frame,
            (config.FRAME_REDUCTION, config.FRAME_REDUCTION),
            (self.camera_width - config.FRAME_REDUCTION, 
             self.camera_height - config.FRAME_REDUCTION),
            (255, 0, 0), 2
        )
        
        # Draw instructions
        instructions = "Press 'Q' to quit | 'R' to reset"
        cv2.putText(
            frame, instructions,
            (10, self.camera_height - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            (255, 255, 255), 1
        )
    
    def process_gestures(self):
        """
        Process detected hand gestures and control mouse.
        
        This is the main gesture recognition and action logic.
        """
        # Reset gesture state
        self.current_gesture = "None"
        self.gesture_performed = False
        
        # Update cooldowns
        self.mouse_controller.update_cooldowns()
        
        # =========================================================================
        # PRIORITY 1: SCROLL (Hold Index Finger Only for 1 Second)
        # =========================================================================
        is_one_finger = self.hand_tracker.detect_one_finger_gesture()
        
        if is_one_finger:
            # Gesture detected, check timer
            if self.scroll_activation_start == 0:
                self.scroll_activation_start = time.time()
            
            # Check if held for 1 second
            if time.time() - self.scroll_activation_start > 1.0:
                self.current_gesture = "SCROLL MODE (Move Index Up/Down)"
                self.scroll_active = True
                
                # Use INDEX finger for scroll tracking (since it's the one up)
                index_pos = self.hand_tracker.get_landmark_position(
                    config.HandLandmark.INDEX_TIP,
                    (self.camera_height, self.camera_width, 3)
                )
                
                if index_pos is not None:
                    # Perform scroll based on vertical movement
                    if self.mouse_controller.scroll_vertical(index_pos[1]):
                        self.gesture_performed = True
                
                # Freeze cursor while scrolling
                return
            else:
                self.current_gesture = f"Hold to Scroll... {1.0 - (time.time() - self.scroll_activation_start):.1f}s"
        else:
            # Gesture lost - Reset everything
            self.scroll_activation_start = 0
            if self.scroll_active:
                self.mouse_controller.reset_scroll_tracking()
                self.scroll_active = False

        # =========================================================================
        # CURSOR MOVEMENT (Only if not scrolling)
        # =========================================================================
        # Get cursor position and move mouse
        cursor_pos = self.hand_tracker.get_cursor_position(
            (self.camera_height, self.camera_width, 3)
        )
        
        if cursor_pos is not None:
            self.mouse_controller.move_cursor(
                cursor_pos,
                self.camera_width,
                self.camera_height
            )
            self.current_gesture = "Tracking"
        
        # =========================================================================
        # CLICKS & DRAG
        # =========================================================================
        
        # Check for right click (middle + thumb pinch)
        if self.hand_tracker.detect_right_click():
            self.current_gesture = "Right Click"
            if self.mouse_controller.right_click():
                self.gesture_performed = True
            return

        # Double click removed for simplicity and stability
        
        # Drag gesture DISABLED per user request for smoother clicking
        # All index+thumb pinches will now be treated as clicks only
        self.mouse_controller.handle_drag_gesture(False)
        
        # Check for left click (index + thumb pinch)
        # Only if not dragging
        if not self.mouse_controller.is_dragging:
            if self.hand_tracker.detect_left_click():
                self.current_gesture = "Left Click"
                if self.mouse_controller.left_click():
                    self.gesture_performed = True
                return
    
    def run(self):
        """
        Main application loop.
        
        This method runs the continuous capture-process-display loop.
        """
        try:
            while True:
                # Capture frame
                success, frame = self.cap.read()
                
                if not success:
                    print("Failed to capture frame. Retrying...")
                    continue
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Increment frame counter
                self.frame_count += 1
                
                # Process every Nth frame based on FRAME_SKIP setting
                if self.frame_count % config.FRAME_SKIP == 0:
                    # Detect hands and draw landmarks
                    frame = self.hand_tracker.find_hands(frame, draw=True)
                    
                    # Process gestures if hand detected
                    if self.hand_tracker.hand_detected:
                        self.process_gestures()
                    else:
                        # No hand detected - reset states
                        self.current_gesture = "No Hand Detected"
                        self.mouse_controller.emergency_stop()
                
                # Calculate FPS
                self.fps = self.calculate_fps()
                
                # Draw UI elements
                self.draw_ui(frame)
                
                # Display frame
                cv2.imshow("Virtual Mouse - Hand Tracking", frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q') or key == ord('Q'):
                    print("\nShutting down...")
                    break
                elif key == ord('r') or key == ord('R'):
                    print("\nResetting system state...")
                    self.mouse_controller.emergency_stop()
                    self.hand_tracker.previous_index_pos = None
                    print("System reset complete")
                
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
        except Exception as e:
            print(f"\n\nError occurred: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources."""
        print("\nCleaning up resources...")
        
        # Release camera
        if self.cap is not None:
            self.cap.release()
        
        # Close windows
        cv2.destroyAllWindows()
        
        # Release hand tracker
        self.hand_tracker.release()
        
        # Ensure mouse is released
        self.mouse_controller.emergency_stop()
        
        print("Cleanup complete. Goodbye!")


def main():
    """Main entry point."""
    try:
        # Create and run virtual mouse
        virtual_mouse = VirtualMouse()
        virtual_mouse.run()
        
    except RuntimeError as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting tips:")
        print("1. Ensure your webcam is connected and not in use by another application")
        print("2. Check camera permissions in your system settings")
        print("3. Try changing CAMERA_INDEX in config.py (0, 1, 2, etc.)")
        
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
