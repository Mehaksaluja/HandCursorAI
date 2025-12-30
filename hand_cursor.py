import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time
from collections import deque
from pynput import keyboard
import config

pyautogui.FAILSAFE = False

class HandCursorController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=config.MAX_NUM_HANDS,
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera. Please check your webcam connection.")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAMERA_HEIGHT)
        
        self.gesture_control_enabled = False
        self.running = True
        
        self.movement_history = deque(maxlen=config.SMOOTHING_HISTORY_SIZE)
        self.smoothing_factor = config.SMOOTHING_FACTOR
        
        self.movement_scale = config.MOVEMENT_SCALE
        self.click_threshold = config.CLICK_THRESHOLD
        
        self.screen_width, self.screen_height = pyautogui.size()
        
        self.last_click_time = 0
        self.click_cooldown = config.CLICK_COOLDOWN
        self.dead_zone_threshold = config.DEAD_ZONE_THRESHOLD
        self.current_gesture = None
        
        self.last_scroll_time = 0
        self.scroll_cooldown = 0.05
        self.last_hand_y = None
        
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        
        print("Hand Cursor Control System Initialized")
        print("Press SPACE to toggle gesture control on/off")
        print("Press Q to quit")
    
    def on_key_press(self, key):
        try:
            if key == keyboard.Key.space:
                self.gesture_control_enabled = not self.gesture_control_enabled
                if self.gesture_control_enabled:
                    print("Gesture control ENABLED")
                    self.movement_history.clear()
                else:
                    print("Gesture control DISABLED")
            elif hasattr(key, 'char') and (key.char == 'q' or key.char == 'Q'):
                self.running = False
                return False
        except AttributeError:
            pass
        return True
    
    def get_hand_landmarks(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        return results.multi_hand_landmarks
    
    def calculate_distance(self, point1, point2):
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def is_pointing_gesture(self, landmarks):
        thumb_tip = landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_pip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]
        middle_tip = landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        middle_pip = landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
        ring_tip = landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        ring_pip = landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP]
        pinky_tip = landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
        pinky_pip = landmarks.landmark[self.mp_hands.HandLandmark.PINKY_PIP]
        
        index_extended = index_tip.y < index_pip.y
        
        middle_closed = middle_tip.y > middle_pip.y
        ring_closed = ring_tip.y > ring_pip.y
        pinky_closed = pinky_tip.y > pinky_pip.y
        
        return index_extended and middle_closed and ring_closed and pinky_closed
    
    def is_pinch_gesture(self, landmarks):
        thumb_tip = landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        
        distance = self.calculate_distance(
            [thumb_tip.x, thumb_tip.y],
            [index_tip.x, index_tip.y]
        )
        
        return distance < self.click_threshold
    
    def is_right_click_gesture(self, landmarks):
        index_tip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_pip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]
        middle_tip = landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        middle_pip = landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
        ring_tip = landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        ring_pip = landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP]
        pinky_tip = landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
        pinky_pip = landmarks.landmark[self.mp_hands.HandLandmark.PINKY_PIP]
        
        index_extended = index_tip.y < index_pip.y
        middle_extended = middle_tip.y < middle_pip.y
        
        ring_closed = ring_tip.y > ring_pip.y
        pinky_closed = pinky_tip.y > pinky_pip.y
        
        return index_extended and middle_extended and ring_closed and pinky_closed
    
    def is_full_hand_open(self, landmarks):
        thumb_tip = landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        thumb_ip = landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP]
        index_tip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_pip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]
        middle_tip = landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        middle_pip = landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
        ring_tip = landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        ring_pip = landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_PIP]
        pinky_tip = landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
        pinky_pip = landmarks.landmark[self.mp_hands.HandLandmark.PINKY_PIP]
        
        thumb_extended = thumb_tip.y < thumb_ip.y or abs(thumb_tip.y - thumb_ip.y) < 0.05
        index_extended = index_tip.y < index_pip.y
        middle_extended = middle_tip.y < middle_pip.y
        ring_extended = ring_tip.y < ring_pip.y
        pinky_extended = pinky_tip.y < pinky_pip.y
        
        return thumb_extended and index_extended and middle_extended and ring_extended and pinky_extended
    
    def handle_scroll(self, landmarks):
        wrist = landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        current_y = wrist.y
        
        current_time = time.time()
        
        if self.last_hand_y is not None:
            dy = current_y - self.last_hand_y
            
            scroll_threshold = 0.01
            
            if abs(dy) > scroll_threshold and (current_time - self.last_scroll_time) > self.scroll_cooldown:
                scroll_amount = int(dy * -100)
                
                if abs(scroll_amount) > 0:
                    pyautogui.scroll(scroll_amount)
                    self.last_scroll_time = current_time
                    print(f"Scrolling: {scroll_amount}")
        
        self.last_hand_y = current_y
    
    def move_cursor(self, landmarks):
        index_tip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        
        finger_x = index_tip.x
        finger_y = index_tip.y
        
        screen_x = int(finger_x * self.screen_width)
        screen_y = int(finger_y * self.screen_height)
        
        self.movement_history.append((screen_x, screen_y))
        if len(self.movement_history) > 1:
            recent_positions = list(self.movement_history)[-3:]
            avg_x = int(np.mean([p[0] for p in recent_positions]))
            avg_y = int(np.mean([p[1] for p in recent_positions]))
        else:
            avg_x, avg_y = screen_x, screen_y
        
        pyautogui.moveTo(avg_x, avg_y, duration=0.01)
    
    def handle_gestures(self, landmarks):
        current_time = time.time()
        self.current_gesture = None
        
        if self.is_full_hand_open(landmarks):
            self.handle_scroll(landmarks)
            self.current_gesture = "FULL HAND - Scrolling"
        
        elif self.is_pinch_gesture(landmarks):
            if current_time - self.last_click_time > 0.1:
                pyautogui.click()
                self.last_click_time = current_time
                print("Left click")
            self.current_gesture = "PINCH - Clicking"
            self.last_hand_y = None
        
        elif self.is_right_click_gesture(landmarks):
            if current_time - self.last_click_time > 0.1:
                pyautogui.rightClick()
                self.last_click_time = current_time
                print("Right click")
            self.current_gesture = "TWO FINGERS - Right Click"
            self.last_hand_y = None
        
        elif self.is_pointing_gesture(landmarks):
            self.move_cursor(landmarks)
            self.current_gesture = "POINTING - Moving Cursor"
            self.last_hand_y = None
        else:
            self.current_gesture = "No gesture detected"
            self.last_hand_y = None
    
    def draw_ui(self, frame):
        height, width = frame.shape[:2]
        
        status_color = (0, 255, 0) if self.gesture_control_enabled else (0, 0, 255)
        status_text = "GESTURE CONTROL: ON" if self.gesture_control_enabled else "GESTURE CONTROL: OFF"
        cv2.putText(frame, status_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
        
        if self.gesture_control_enabled and self.current_gesture:
            if "Moving" in self.current_gesture or "Scrolling" in self.current_gesture:
                gesture_color = (0, 255, 255)
            elif "Clicking" in self.current_gesture:
                gesture_color = (255, 255, 0)
            else:
                gesture_color = (255, 255, 255)
            cv2.putText(frame, f"Gesture: {self.current_gesture}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, gesture_color, 2)
        
        y_offset = height - 80
        cv2.putText(frame, "SPACE: Toggle ON/OFF | Q: Quit", (10, y_offset),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        if self.gesture_control_enabled:
            y_offset += 20
            cv2.putText(frame, "Pointing=Move | Pinch=Click | 2 Fingers=Right Click | Full Hand=Scroll", (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
        else:
            y_offset += 20
            cv2.putText(frame, "Press SPACE to enable gesture control", (10, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
    
    def run(self):
        try:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to read from camera")
                    break
                
                frame = cv2.flip(frame, 1)
                
                hand_landmarks = self.get_hand_landmarks(frame)
                
                if hand_landmarks:
                    for landmarks in hand_landmarks:
                        self.mp_draw.draw_landmarks(
                            frame, landmarks, self.mp_hands.HAND_CONNECTIONS
                        )
                        
                        if self.gesture_control_enabled:
                            self.handle_gestures(landmarks)
                
                self.draw_ui(frame)
                
                cv2.imshow('Hand Cursor Control', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False
                    break
        
        except KeyboardInterrupt:
            pass
        finally:
            self.cleanup()
    
    def cleanup(self):
        self.cap.release()
        cv2.destroyAllWindows()
        self.listener.stop()
        print("Application closed")

if __name__ == "__main__":
    controller = HandCursorController()
    controller.run()
