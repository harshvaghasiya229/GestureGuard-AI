import cv2
import time
import csv
import mediapipe as mp

from mediapipe.tasks.python import vision
from mediapipe.tasks import python

# ---------- SETUP ----------
base_options = python.BaseOptions(model_asset_path="hand_landmarker.task")

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

gesture_name = input("Enter gesture name: ")

with open("gesture_data.csv", "a", newline="") as f:
    writer = csv.writer(f)

    print("Collecting data... Press ESC to stop")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        timestamp = int(time.time() * 1000)

        result = detector.detect_for_video(mp_image, timestamp)

        if result.hand_landmarks:
            landmarks = result.hand_landmarks[0]

            row = []
            for lm in landmarks:
                row.extend([lm.x, lm.y, lm.z])

            row.append(gesture_name)
            writer.writerow(row)

            print("Captured")

        cv2.imshow("Collecting", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()