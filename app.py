import os
import pyautogui
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Disable PyAutoGUI failsafe for smoother movement, 
# but keep it in mind (move mouse to corner to stop)
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0  # Minimize delay for real-time control

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gesturax_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Smoothing parameters
ALPHA = 0.5  # Smoothing factor (0 to 1, higher = more responsive, lower = smoother)
prev_x, prev_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

@app.route('/')
def index():
    return "GESTURAX Backend is running. Please open index.html in your browser."

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('gesture_data')
def handle_gesture_data(data):
    global prev_x, prev_y
    
    # Extract data
    x = data.get('x')
    y = data.get('y')
    gesture = data.get('gesture')  # 'none', 'pinch', 'scroll'
    
    if x is not None and y is not None:
        # Scale coordinates (MediaPipe X is mirrored by default in JS, so we might need to flip it here or in JS)
        # Assuming JS sends (1-x) for mirroring if needed, or we handle it here.
        target_x = int(x * SCREEN_WIDTH)
        target_y = int(y * SCREEN_HEIGHT)
        
        # Apply smoothing
        curr_x = int(ALPHA * target_x + (1 - ALPHA) * prev_x)
        curr_y = int(ALPHA * target_y + (1 - ALPHA) * prev_y)
        
        # Move mouse
        pyautogui.moveTo(curr_x, curr_y, _pause=False)
        
        prev_x, prev_y = curr_x, curr_y

    # Handle Gestures
    if gesture == 'pinch':
        pyautogui.click()
    elif gesture == 'scroll_up':
        pyautogui.scroll(100)
    elif gesture == 'scroll_down':
        pyautogui.scroll(-100)

if __name__ == '__main__':
    print(f"Screen Resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print("Failsafe: Move mouse to any corner of the screen to abort.")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
