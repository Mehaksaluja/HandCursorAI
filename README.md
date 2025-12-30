# Hand Gesture Cursor Control

A hybrid human-computer interaction system that allows you to control your laptop cursor using hand gestures detected via webcam, while maintaining full compatibility with traditional mouse/trackpad input.

## Features

- **Non-intrusive**: Does not disable or interfere with normal mouse/trackpad behavior
- **Dynamic Toggle**: Enable or disable gesture control with a simple keyboard shortcut
- **Real-time Processing**: Low-latency hand tracking using MediaPipe
- **Accessibility-Friendly**: Visual feedback and smooth cursor movements
- **Multiple Gestures**: 
  - Pointing gesture for cursor movement
  - Pinch gesture for clicking
  - Fist gesture for dragging

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
- **Pointing Gesture**: Move cursor (index finger extended, other fingers closed)
- **Pinch Gesture**: Left click (thumb and index finger touching)
- **Fist**: Right click (all fingers closed)

### How It Works

1. The system captures video from your default webcam
2. MediaPipe detects hand landmarks in real-time
3. Gestures are interpreted and converted to cursor movements/clicks
4. When gesture control is enabled, movements are relative to a calibration point
5. Traditional mouse/trackpad input continues to work normally

## Technical Details

- Uses MediaPipe Hands for robust hand landmark detection
- Implements smoothing algorithms to reduce cursor jitter
- Calibration system for personalized control zones
- Configurable sensitivity and movement scaling
