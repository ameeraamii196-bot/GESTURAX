# Virtual Mouse using Hand Gestures

This project implements a virtual mouse system that allows you to control your computer cursor, click, drag, and scroll using hand gestures captured by a webcam.

## Features

- **Cursor Control**: Move the cursor by moving your index finger.
- **Left Click**: Pinch your index finger and thumb together.
- **Drag**: Pinch and hold to drag items.
- **Right Click**: Show both index and middle fingers close together.
- **Scroll**: Show both index and middle fingers apart, and move your hand up/down.

## Prerequisites

- Python 3.7+
- Webcam

## Installation

1. Clone or download this repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the main script:

```bash
python main.py
```

2. A window will open showing the webcam feed.
3. Use the following gestures:

| Action | Gesture | Visual Feedback |
| :--- | :--- | :--- |
| **Move Cursor** | Index finger up, other fingers down | Purple rectangle shows active area |
| **Left Click** | Pinch Index + Thumb (short pinch) | Green circle on fingertip |
| **Drag** | Pinch Index + Thumb (hold) | Green circle on fingertip |
| **Right Click** | Index + Middle fingers up (close together) | Red circle on fingertips |
| **Scroll** | Index + Middle fingers up (apart) | Move hand up/down to scroll |

4. Press `q` to quit the application.

## Troubleshooting

- **Cursor not moving?** Ensure only your index finger is up.
- **Jittery movement?** Adjust lighting or increase `smoothing_factor` in `main.py`.
- **Gestures not recognized?** Ensure your hand is clearly visible and not too close/far from the camera.
