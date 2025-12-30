# Hand Gesture Cursor Control

A hybrid human-computer interaction system that allows you to control your laptop cursor using hand gestures detected via webcam, while maintaining full compatibility with traditional mouse/trackpad input.

## Features

- **Non-intrusive**: Does not disable or interfere with normal mouse/trackpad behavior
- **Dynamic Toggle**: Enable or disable gesture control with a simple keyboard shortcut
- **Real-time Processing**: Low-latency hand tracking using MediaPipe
- **Accessibility-Friendly**: Visual feedback and smooth cursor movements
- **Multiple Gestures**: 
  - Pointing gesture for cursor movement
  - Pinch gesture for left click
  - Two fingers extended for right click
  - Full hand open for scrolling

## Installation

1. Install Python 3.8 or higher
2. Create and activate virtual environment (recommended):
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
.\venv\Scripts\activate.bat  # Windows CMD
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Testing

Before running the main application, you can test if everything is set up correctly:

```bash
python test_hand_cursor.py
```

This test script will:
- Check if all dependencies are installed
- Verify camera access
- Test MediaPipe hand detection
- Test PyAutoGUI cursor control
- Quick hand detection test with visual feedback

## Usage

1. Activate virtual environment:
```bash
.\venv\Scripts\Activate.ps1  # PowerShell
# or
.\venv\Scripts\activate.bat  # CMD
```
2. Run the application:
```bash
python hand_cursor.py
```

### Controls

- **Space Bar**: Toggle gesture control on/off
- **Q**: Quit the application

### Gestures

- **Pointing Gesture**: Move cursor (index finger extended, other fingers closed)
  - Cursor follows index finger position directly
  - Move hand to move cursor on screen
  
- **Pinch Gesture**: Left click (thumb and index finger touching)
  - Immediate click when pinch is detected
  
- **Two Fingers Extended**: Right click (index and middle fingers both extended)
  - Other fingers should be closed
  
- **Full Hand Open**: Scroll (all fingers extended)
  - Move hand up to scroll up
  - Move hand down to scroll down

### How It Works

1. The system captures video from your default webcam
2. MediaPipe detects hand landmarks in real-time
3. Gestures are interpreted and converted to cursor movements/clicks
4. Cursor movement uses absolute positioning - follows index finger position directly
5. Traditional mouse/trackpad input continues to work normally (hybrid system)

## Technical Details

- Uses MediaPipe Hands for robust hand landmark detection
- Implements smoothing algorithms to reduce cursor jitter
- Absolute positioning for cursor movement (finger position maps directly to screen)
- Configurable sensitivity and movement scaling via config.py
- Real-time gesture recognition with priority system (scroll > click > move)
