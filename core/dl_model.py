import numpy as np
import tensorflow as tf

class DLModel:
    def __init__(self):
        try:
            self.model = tf.keras.models.load_model("data/gesture_dl_model.h5")
            self.labels = np.load("data/labels.npy", allow_pickle=True)
        except Exception as e:
            print("❌ MODEL LOAD ERROR:", e)
            self.model = None

    def predict(self, landmarks):
        if self.model is None:
            return "no_model"
        print("Model loaded:", self.model is not None)
        row = []
        for lm in landmarks:
            row.extend([lm.x, lm.y, lm.z])

        row = np.array([row])

        pred = self.model.predict(row, verbose=0)
        class_id = np.argmax(pred)

        return self.labels[class_id]