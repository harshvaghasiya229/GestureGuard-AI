import cv2
import time
import mediapipe as mp

from mediapipe.tasks.python import vision
from mediapipe.tasks import python
from config import TASK_MODEL_PATH

class HandDetector:
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path=TASK_MODEL_PATH)

        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=2,
            min_hand_detection_confidence=0.4
        )

        self.detector = vision.HandLandmarker.create_from_options(options)

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        timestamp = int(time.time() * 1000)
        return self.detector.detect_for_video(mp_image, timestamp)

    # 🔥 ADD THIS
    def close(self):
        if self.detector:
            self.detector.close()
            self.detector = None