# GESTURAX - AI Gesture Control System

GESTURAX is a real-time, web-based system that allows you to control your computer's mouse and system actions using hand gestures captured via a webcam.

## 🚀 Features

- **Real-time Tracking**: Powered by MediaPipe Hands for high-precision hand landmark detection.
- **Low-Latency Communication**: Uses Socket.io to stream coordinates from the browser to a Python backend.
- **Intelligent Scaling**: Automatically maps a central "active zone" in the webcam feed to your full screen resolution, making it easy to reach corners.
- **Smoothing**: Implements exponential smoothing to ensure jitter-free cursor movement.
- **Premium Dashboard**: A modern, dark-themed UI showing the live video feed with a skeleton overlay and gesture indicators.

## 🖐️ Gesture Mapping

| Gesture | Action |
| :--- | :--- |
| **Index Finger Movement** | Mouse Cursor Movement |
| **Pinch (Thumb + Index)** | Left Mouse Click |
| **Two Fingers Up (Index + Middle)** | Scroll Mode (based on height) |

## 🛠️ Tech Stack

- **Frontend**: HTML5, Vanilla CSS, JavaScript, MediaPipe Hands, Socket.io-client.
- **Backend**: Python, Flask, Flask-SocketIO, PyAutoGUI.

## 📖 How to Use

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Backend**:
   ```bash
   python app.py
   ```
3. **Open the Dashboard**:
   Open `index.html` in Chrome or Edge.
4. **Safety Failsafe**:
   If the cursor behaves unexpectedly, move your physical mouse to **any corner of the screen** to immediately stop the script.

---
*Created by Antigravity AI Coding Assistant.*
