import cv2
import mediapipe as mp
import sys

def test_camera():
    print("Testing camera...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Camera not accessible!")
        print("   Please check:")
        print("   - Is your webcam connected?")
        print("   - Is another application using the camera?")
        return False
    
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Cannot read from camera!")
        cap.release()
        return False
    
    print("[OK] Camera is working!")
    print(f"   Resolution: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
    cap.release()
    return True

def test_mediapipe():
    print("\nTesting MediaPipe hand detection...")
    try:
        import mediapipe as mp
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        print("[OK] MediaPipe initialized successfully!")
        return True
    except Exception as e:
        print(f"[ERROR] MediaPipe initialization failed!")
        print(f"   Error: {e}")
        return False

def test_pyautogui():
    print("\nTesting PyAutoGUI...")
    try:
        import pyautogui
        screen_width, screen_height = pyautogui.size()
        print("[OK] PyAutoGUI is working!")
        print(f"   Screen size: {screen_width}x{screen_height}")
        return True
    except Exception as e:
        print(f"[ERROR] PyAutoGUI test failed!")
        print(f"   Error: {e}")
        return False

def test_dependencies():
    print("\nTesting dependencies...")
    dependencies = {
        'cv2': 'opencv-python',
        'mediapipe': 'mediapipe',
        'numpy': 'numpy',
        'pyautogui': 'pyautogui',
        'pynput': 'pynput'
    }
    
    all_ok = True
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"[OK] {package} is installed")
        except ImportError:
            print(f"[ERROR] {package} is NOT installed")
            print(f"   Run: pip install {package}")
            all_ok = False
    
    return all_ok

def quick_hand_test():
    print("\n" + "="*50)
    print("Quick Hand Detection Test")
    print("="*50)
    print("Show your hand to the camera...")
    print("Press 'q' to quit this test")
    print("="*50)
    
    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )
    mp_draw = mp.solutions.drawing_utils
    
    hand_detected = False
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            hand_detected = True
            for landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
            cv2.putText(frame, "HAND DETECTED!", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No hand detected - Show your hand", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('Hand Detection Test', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        frame_count += 1
        if frame_count > 30 and not hand_detected:
            print("\n[WARNING] No hand detected after 30 frames")
            print("   Make sure:")
            print("   - Your hand is visible in the camera")
            print("   - There's good lighting")
            print("   - Your hand is not too close or too far from camera")
    
    cap.release()
    cv2.destroyAllWindows()
    
    if hand_detected:
        print("\n[OK] Hand detection is working!")
    else:
        print("\n[WARNING] Hand was not detected. Check lighting and camera position.")
    
    return hand_detected

def main():
    print("="*50)
    print("Hand Cursor Control System - Test Suite")
    print("="*50)
    
    if not test_dependencies():
        print("\n[ERROR] Please install missing dependencies first!")
        print("   Run: pip install -r requirements.txt")
        sys.exit(1)
    
    if not test_camera():
        print("\n[ERROR] Camera test failed!")
        sys.exit(1)
    
    if not test_mediapipe():
        print("\n[ERROR] MediaPipe test failed!")
        sys.exit(1)
    
    if not test_pyautogui():
        print("\n[ERROR] PyAutoGUI test failed!")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("All basic tests passed! [OK]")
    print("="*50)
    
    response = input("\nDo you want to test hand detection? (y/n): ")
    if response.lower() == 'y':
        quick_hand_test()
    
    print("\n" + "="*50)
    print("Testing complete!")
    print("="*50)
    print("\nTo run the full application:")
    print("  python hand_cursor.py")
    print("\nControls:")
    print("  - SPACE: Toggle gesture control on/off")
    print("  - Q: Quit application")
    print("  - Pointing gesture: Move cursor")
    print("  - Pinch gesture: Left click")
    print("  - Fist gesture: Right click")

if __name__ == "__main__":
    main()
