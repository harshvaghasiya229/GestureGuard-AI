import joblib
from config import MODEL_PATH

class GestureModel:
    def __init__(self):
        try:
            self.model = joblib.load(MODEL_PATH)
        except:
            self.model = None

    def predict(self, landmarks):
        if self.model is None:
            return "no_model"

        row = []
        for lm in landmarks:
            row.extend([lm.x, lm.y, lm.z])

        return self.model.predict([row])[0]