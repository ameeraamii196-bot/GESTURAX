import cv2
import time
import numpy as np
import math
from hand_tracker import HandTracker
from mouse_controller import MouseController

def main():
    # 1. Initialization
    wCam, hCam = 640, 480
    frame_margin = 150 # Frame margin for mouse movement
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera index 0 could not be opened. Trying index 1...")
        cap = cv2.VideoCapture(1)
        if not cap.isOpened():
             print("Error: Could not open any webcam. Please check connections.")
             return

    cap.set(3, wCam)
    cap.set(4, hCam)

    tracker = HandTracker(max_hands=1, detection_con=0.7)
    mouse = MouseController(smoothing_factor=5)

    p_time = 0.0
    
    # State variables
    dragging = False
    scroll_y_prev = 0.0
    last_click_time = 0.0
    
    while True:
        # 2. Find Hand Landmarks
        success, img = cap.read()
        if not success:
            print("Error: Could not access the webcam. Please ensure it is connected and not used by another application.")
            time.sleep(3)
            break
            
        img = cv2.flip(img, 1) # Flip horizontally for mirror view
        img = tracker.find_hands(img)
        lm_list = tracker.find_position(img, draw=False)

        if len(lm_list) != 0:
            x1, y1 = lm_list[8][1:] # Index Finger Tip
            x2, y2 = lm_list[12][1:] # Middle Finger Tip
            x_thumb, y_thumb = lm_list[4][1:] # Thumb Tip

            # 3. Check which fingers are up
            fingers = []
            
            # Thumb
            # Heuristic: Compare Tip x to IP x (assuming right hand/flipped)
            if lm_list[4][1] < lm_list[3][1]:
                fingers.append(1) # Open
            else:
                fingers.append(0) # Bent

            # Index
            if lm_list[8][2] < lm_list[6][2]:
                fingers.append(1)
            else:
                fingers.append(0)
            
            # Middle
            if lm_list[12][2] < lm_list[10][2]:
                fingers.append(1)
            else:
                fingers.append(0)
                
            # Ring
            if lm_list[16][2] < lm_list[14][2]:
                fingers.append(1)
            else:
                fingers.append(0)
                
            # Pinky
            if lm_list[20][2] < lm_list[18][2]:
                fingers.append(1)
            else:
                fingers.append(0)

            # 4. Mode Selection & Actions
            
            # Use Index Finger Tip for all mouse movements
            # General Condition: Index must be up to track
            if fingers[1] == 1:
                
                # Mode: Scrolling (Index + Middle Up and Close)
                dist_index_middle = math.hypot(x1 - x2, y1 - y2)
                if fingers[2] == 1 and dist_index_middle < 40:
                     # Scroll Mode
                     current_scroll_y = (y1 + y2) / 2
                     if scroll_y_prev != 0:
                         diff = current_scroll_y - scroll_y_prev
                         if diff > 5: 
                              mouse.click('scroll_down')
                         elif diff < -5:
                              mouse.click('scroll_up')
                     
                     scroll_y_prev = current_scroll_y
                     
                     # Visual Feedback
                     cv2.circle(img, (x1, y1), 15, (0, 255, 255), cv2.FILLED) 
                     cv2.circle(img, (x2, y2), 15, (0, 255, 255), cv2.FILLED)

                # Mode: Double Click (Middle Finger Bent Alone - i.e. Index Up, Middle Down, Ring Up, Pinky Up)
                elif fingers[2] == 0 and fingers[3] == 1 and fingers[4] == 1:
                     scroll_y_prev = 0
                     if time.time() - last_click_time > 1.0:
                        cv2.putText(img, "Double Click", (20, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                        mouse.click('double')
                        last_click_time = time.time()

                # Mode: Move & Left Click (Index Up, Normal State)
                else:
                    scroll_y_prev = 0
                    
                    # 1. Move Cursor
                    cv2.rectangle(img, (frame_margin, frame_margin), (wCam - frame_margin, hCam - frame_margin), (255, 0, 255), 2)
                    mouse.move_cursor(x1, y1, wCam, hCam, frame_margin)
                    
                    # 2. Left Click / Drag (Thumb Bent)
                    if fingers[0] == 0: # Thumb is bent
                        cv2.circle(img, (x_thumb, y_thumb), 15, (0, 255, 0), cv2.FILLED)
                        if not dragging:
                            mouse.click('drag_start')
                            dragging = True
                    else: # Thumb is open
                        if dragging:
                            mouse.click('drag_end')
                            dragging = False


        # 5. Frame Rate
        c_time = time.time()
        fps = 1 / (c_time - p_time)
        p_time = c_time
        cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # 6. Display
        cv2.imshow("Virtual Mouse", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
