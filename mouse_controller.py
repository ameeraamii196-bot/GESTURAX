import pyautogui
import numpy as np
import time

class MouseController:
    def __init__(self, smoothing_factor=5):
        self.screen_width, self.screen_height = pyautogui.size()
        self.smoothing_factor = smoothing_factor
        self.prev_x, self.prev_y = 0, 0
        self.curr_x, self.curr_y = 0, 0
        pyautogui.FAILSAFE = False # Disable failsafe to prevent crashes at corners

    def move_cursor(self, x, y, frame_width, frame_height, margin=100):
        """
        Moves the cursor based on hand position.
        x, y: Coordinates from the hand tracker (in frame pixels)
        frame_width, frame_height: Dimensions of the camera frame
        margin: Margin around the frame to map to screen edges
        """
        # 1. Convert coordinates
        # Interpolate x from [margin, frame_width-margin] to [0, screen_width]
        # Interpolate y from [margin, frame_height-margin] to [0, screen_height]
        
        x_mapped = np.interp(x, (margin, frame_width - margin), (0, self.screen_width))
        y_mapped = np.interp(y, (margin, frame_height - margin), (0, self.screen_height))

        # 2. Smoothing
        self.curr_x = self.prev_x + (x_mapped - self.prev_x) / self.smoothing_factor
        self.curr_y = self.prev_y + (y_mapped - self.prev_y) / self.smoothing_factor

        # 3. Move Mouse
        pyautogui.moveTo(self.curr_x, self.curr_y)
        
        self.prev_x, self.prev_y = self.curr_x, self.curr_y

    def click(self, action):
        if action == 'left':
            pyautogui.click()
        elif action == 'right':
            pyautogui.click(button='right')
        elif action == 'drag_start':
            pyautogui.mouseDown()
        elif action == 'drag_end':
            pyautogui.mouseUp()
        elif action == 'scroll_up':
            pyautogui.scroll(300)
        elif action == 'scroll_down':
            pyautogui.scroll(-300)
        elif action == 'double':
            pyautogui.doubleClick()
