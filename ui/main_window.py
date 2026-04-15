import cv2
import time
import pyautogui

from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap, QPainter, QColor, QPen, QFont
from PyQt6.QtWidgets import QPushButton

from core.detector import HandDetector
from core.dl_model import DLModel
from core.controller import Controller
from utils.smoothing import Smoother
from ui.recording_window import RecordingWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🧠 AI Gesture HUD")
        self.setGeometry(100, 100, 1000, 700)
        self.current_gesture = "none"
        # Transparent Iron Man UI
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.video_label = QLabel(self)
        self.video_label.setGeometry(50, 50, 900, 550)

        self.status_label = QLabel(self)
        self.status_label.setGeometry(50, 620, 900, 40)
        self.status_label.setStyleSheet("color: cyan;")
        self.status_label.setFont(QFont("Consolas", 14))
        
        # 🎥 Add Gesture Button
        self.add_gesture_btn = QPushButton("🎥 Add Gesture", self)
        self.add_gesture_btn.setGeometry(50, 10, 150, 30)
        self.add_gesture_btn.setStyleSheet("background-color: cyan; color: black;")

        # ❌ Close Button
        self.close_btn = QPushButton("❌ Close", self)
        self.close_btn.setGeometry(850, 10, 100, 30)
        self.close_btn.setStyleSheet("background-color: red; color: white;")
        
        # 🎮 Assign button
        self.assign_btn = QPushButton("⚡ Assign Action", self)
        self.assign_btn.setGeometry(220, 10, 180, 30)
        self.assign_btn.setStyleSheet("background-color: orange; color: black;")

        self.assign_btn.clicked.connect(self.open_assign_panel)
        # Connect
        self.add_gesture_btn.clicked.connect(self.open_recorder)
        self.close_btn.clicked.connect(self.close_app)
        self.cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

        self.detector = HandDetector()
        self.model = DLModel()
        self.controller = Controller()
        self.smoother = Smoother()

        self.prev_time = time.time()
        self.fps = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.prev_gesture = None
        self.gesture_count = 0
        self.required_frames = 5   # must hold gesture for 5 frames

    def paintEvent(self, event):
        painter = QPainter(self)

        # Glass panel
        painter.setBrush(QColor(10, 10, 30, 180))
        painter.setPen(QPen(QColor(0, 255, 255), 2))
        painter.drawRoundedRect(20, 20, 960, 660, 20, 20)

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        result = self.detector.detect(frame)

        gesture = "No Gesture"
        action = "No Action"

        if result.hand_landmarks:
            for i, landmarks in enumerate(result.hand_landmarks):

                # 🎯 Draw landmarks
                for lm in landmarks:
                    x = int(lm.x * frame.shape[1])
                    y = int(lm.y * frame.shape[0])
                    cv2.circle(frame, (x, y), 5, (0, 255, 255), -1)

                # 🎯 Center point (wrist)
                h, w, _ = frame.shape
                cx = int(landmarks[0].x * w)
                cy = int(landmarks[0].y * h)
                cv2.circle(frame, (cx, cy), 10, (0, 255, 255), 2)

                # 🔗 Draw connections
                for j in range(len(landmarks) - 1):
                    p1 = landmarks[j]
                    p2 = landmarks[j + 1]

                    x1, y1 = int(p1.x * w), int(p1.y * h)
                    x2, y2 = int(p2.x * w), int(p2.y * h)

                    cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)

                # 🧠 AI Prediction
                gesture = self.model.predict(landmarks)
                self.current_gesture = gesture

                print("Detected gesture:", gesture)

                # 🖱️ Mouse position (index finger)
                index = landmarks[8]
                screen_w, screen_h = pyautogui.size()

                x = int(index.x * screen_w)
                y = int(index.y * screen_h)

                sx, sy = self.smoother.smooth(x, y)

                # 🔥 Stability check
                if gesture == self.prev_gesture:
                    self.gesture_count += 1
                else:
                    self.gesture_count = 0

                self.prev_gesture = gesture

                # 🎮 Execute action if stable
                if self.gesture_count > self.required_frames:
                    self.controller.execute(gesture, sx, sy)

                # 🧠 Get mapped action
                config = self.controller.load_config()
                action = config.get(gesture, "none")

        # ⚡ FPS Calculation
        current_time = time.time()
        self.fps = int(1 / (current_time - self.prev_time + 1e-5))
        self.prev_time = current_time

       # 🧊 HUD Panel (bigger + centered properly)
        cv2.rectangle(frame, (10, 10), (500, 140), (0, 0, 0), -1)

        # 🧠 Gesture
        cv2.putText(frame, f"Gesture: {gesture}", (30, 45),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

        # 🎮 Action
        cv2.putText(frame, f"Action: {action}", (30, 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

        # ⚡ FPS
        cv2.putText(frame, f"FPS: {self.fps}", (30, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # 🖼️ Convert to Qt Image
        h, w, ch = frame.shape
        img = QImage(frame.data, w, h, ch * w, QImage.Format.Format_BGR888)

        self.video_label.setPixmap(QPixmap.fromImage(img))
        self.status_label.setText(f"{gesture} | {action}")
    
    def open_assign_panel(self):
        from ui.gesture_panel import GesturePanel
        self.panel = GesturePanel(selected_gesture=self.current_gesture)
        self.panel.show()

    def closeEvent(self, event):
        self.cap.release()
        self.detector.close()
        event.accept()
    
    def open_recorder(self):
        self.recorder = RecordingWindow()
        self.recorder.show()

    def close_app(self):
        self.close()