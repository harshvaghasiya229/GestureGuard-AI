import cv2
import time
import csv
import mediapipe as mp

from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap

from core.detector import HandDetector

class RecordingWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🎥 Gesture Recorder")
        self.setGeometry(200, 200, 800, 600)

        self.layout = QVBoxLayout()

        # Camera
        self.video_label = QLabel()
        self.layout.addWidget(self.video_label)

        # Input gesture name
        self.gesture_input = QLineEdit()
        self.gesture_input.setPlaceholderText("Enter gesture name (e.g. thumbs_up)")
        self.layout.addWidget(self.gesture_input)

        # Buttons
        self.start_btn = QPushButton("🟢 Start Recording")
        self.stop_btn = QPushButton("🔴 Stop Recording")

        self.layout.addWidget(self.start_btn)
        self.layout.addWidget(self.stop_btn)

        # Status
        self.status_label = QLabel("Samples: 0")
        self.layout.addWidget(self.status_label)

        self.setLayout(self.layout)

        # Logic
        self.cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
        self.detector = HandDetector()

        self.recording = False
        self.sample_count = 0

        self.start_btn.clicked.connect(self.start_recording)
        self.stop_btn.clicked.connect(self.stop_recording)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def start_recording(self):
        self.gesture_name = self.gesture_input.text()

        if not self.gesture_name:
            self.status_label.setText("❌ Enter gesture name")
            return

        self.recording = True
        self.sample_count = 0
        self.file = open("data/gesture_data.csv", "a", newline="")
        self.writer = csv.writer(self.file)

    def stop_recording(self):
        self.recording = False
        if hasattr(self, "file"):
            self.file.close()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        result = self.detector.detect(frame)

        if result.hand_landmarks:
            landmarks = result.hand_landmarks[0]

            # draw points
            for lm in landmarks:
                x = int(lm.x * frame.shape[1])
                y = int(lm.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            if self.recording:
                row = []
                for lm in landmarks:
                    row.extend([lm.x, lm.y, lm.z])

                row.append(self.gesture_name)
                self.writer.writerow(row)

                self.sample_count += 1
                self.status_label.setText(f"📊 Samples: {self.sample_count}")

        # show frame
        h, w, ch = frame.shape
        img = QImage(frame.data, w, h, ch * w, QImage.Format.Format_BGR888)
        self.video_label.setPixmap(QPixmap.fromImage(img))

    def closeEvent(self, event):
        self.cap.release()
        event.accept()