import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time
import math
import os

class HandTracker:
    def __init__(self, mode=False, max_hands=1, detection_con=0.5, track_con=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.track_con = track_con

        # Define model path - verify it exists or warn
        model_path = 'hand_landmarker.task'
        if not os.path.exists(model_path):
            print(f"Warning: {model_path} not found. Please ensure it is in the same directory.")
        
        # New API Setup
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=self.max_hands,
            min_hand_detection_confidence=self.detection_con,
            min_hand_presence_confidence=self.detection_con, # Approximation
            min_tracking_confidence=self.track_con
        )
        try:
            self.landmarker = vision.HandLandmarker.create_from_options(options)
        except Exception as e:
            print(f"Failed to create HandLandmarker: {e}. Ensure 'hand_landmarker.task' is present and valid.")
            self.landmarker = None
            
        self.results = None

        # Standard Hand Connections
        self.HAND_CONNECTIONS = [
            (0, 1), (1, 2), (2, 3), (3, 4),
            (0, 5), (5, 6), (6, 7), (7, 8),
            (5, 9), (9, 10), (10, 11), (11, 12),
            (9, 13), (13, 14), (14, 15), (15, 16),
            (13, 17), (17, 18), (18, 19), (19, 20),
            (0, 17)
        ]

    def find_hands(self, img, draw=True):
        if self.landmarker is None:
            return img

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Create MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        
        # Detect
        self.results = self.landmarker.detect(mp_image)
        results = self.results

        # Draw
        hand_landmarks = getattr(results, 'hand_landmarks', None)
        if hand_landmarks:
            for hand_lms in hand_landmarks:
                if draw:
                    self.draw_landmarks_manually(img, hand_lms)
                    
        return img
    
    def draw_landmarks_manually(self, img, landmarks):
        h, w, c = img.shape
        # Draw connections
        for p1_idx, p2_idx in self.HAND_CONNECTIONS:
             x1 = int(landmarks[p1_idx].x * w)
             y1 = int(landmarks[p1_idx].y * h)
             x2 = int(landmarks[p2_idx].x * w)
             y2 = int(landmarks[p2_idx].y * h)
             cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
             
        # Draw points
        for lm in landmarks:
             cx, cy = int(lm.x * w), int(lm.y * h)
             cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

    def find_position(self, img, hand_no=0, draw=True):
        lm_list = []
        results = self.results
        hand_landmarks = getattr(results, 'hand_landmarks', None)
        if hand_landmarks:
            try:
                if hand_no < len(hand_landmarks):
                    my_hand = hand_landmarks[hand_no]
                    for id, lm in enumerate(my_hand):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lm_list.append([id, cx, cy])
                        if draw:
                            cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            except IndexError:
                pass
        return lm_list

def main():
    # Simple test code
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    p_time = 0
    c_time = 0

    print("Starting loop...")
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read frame")
            break
            
        img = tracker.find_hands(img)
        lm_list = tracker.find_position(img)
        if len(lm_list) != 0:
            print(lm_list[8]) # Print index finger tip position

        c_time = time.time()
        fps = 1 / (c_time - p_time) if c_time > p_time else 0
        p_time = c_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
