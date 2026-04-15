import json
import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

CONFIG_PATH = "data/gesture_config.json"

def load_gestures():
    try:
        labels = np.load("data/labels.npy", allow_pickle=True)
        return list(labels)
    except:
        return []

ACTIONS = [
    "none",
    "click",
    "double_click",
    "right_click",
    "scroll_up",
    "scroll_down",
    "move_mouse",
    "desktop",
    "launchpad",
    "mission_control",
    "next_app",
    "prev_app",
    "volume_up",
    "volume_down",
    "mute",
    "screenshot"
]

class GesturePanel(QWidget):
    def __init__(self, selected_gesture=None):
        super().__init__()
        self.selected_gesture = selected_gesture

        self.setWindowTitle("🧠 Gesture Customization Panel")
        self.setGeometry(300, 200, 500, 500)

        # Glass effect
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(20, 20, 40, 180);
                color: cyan;
                border-radius: 15px;
            }
        """)

        # ✅ MAIN LAYOUT (FIXED)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.setLayout(self.layout)

        # 🔥 TITLE
        title = QLabel("⚡ Gesture Mapping")
        title.setFont(QFont("Menlo", 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(title)

        # 🔄 RELOAD BUTTON
        self.reload_btn = QPushButton("🔄 Reload Gestures")
        self.layout.addWidget(self.reload_btn)
        self.reload_btn.clicked.connect(self.reload_gestures)

        # 🎯 GESTURE CONTAINER (VERY IMPORTANT)
        self.gesture_layout = QVBoxLayout()
        self.gesture_layout.setSpacing(10)
        self.gesture_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addLayout(self.gesture_layout)

        self.mapping = {}

        # Load gestures initially
        self.load_gesture_rows()

        # 💾 BUTTONS
        self.save_btn = QPushButton("💾 Save")
        self.load_btn = QPushButton("📂 Load")

        self.layout.addWidget(self.save_btn)
        self.layout.addWidget(self.load_btn)

        self.save_btn.clicked.connect(self.save_config)
        self.load_btn.clicked.connect(self.load_config)

    # 🔥 LOAD GESTURE ROWS
    def load_gesture_rows(self):
        self.gestures = load_gestures()

        for gesture in self.gestures:
            row_layout = QHBoxLayout()

            label = QLabel(gesture)

            # Highlight selected gesture
            if gesture == self.selected_gesture:
                label.setStyleSheet("color: yellow; font-weight: bold;")

            combo = QComboBox()
            combo.addItems(ACTIONS)

            row_layout.addWidget(label)
            row_layout.addWidget(combo)

            # ✅ ADD TO GESTURE LAYOUT (FIXED)
            self.gesture_layout.addLayout(row_layout)

            self.mapping[gesture] = combo

    def save_config(self):
        data = {}

        for gesture, combo in self.mapping.items():
            data[gesture] = combo.currentText()

        with open(CONFIG_PATH, "w") as f:
            json.dump(data, f, indent=4)

        print("✅ Config Saved")

    def load_config(self):
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)

            for gesture, action in data.items():
                if gesture in self.mapping:
                    self.mapping[gesture].setCurrentText(action)
        except:
            pass

    def reload_gestures(self):
        # 🔒 Prevent spam clicking
        self.reload_btn.setEnabled(False)

        # 🔥 CLEAR OLD ROWS COMPLETELY
        while self.gesture_layout.count():
            item = self.gesture_layout.takeAt(0)

            if item:
                layout = item.layout()

                if layout:
                    while layout.count():
                        child = layout.takeAt(0)
                        if child.widget():
                            child.widget().deleteLater()

                    layout.deleteLater()

        # 🔥 RESET
        self.mapping.clear()

        # 🔁 LOAD AGAIN
        self.load_gesture_rows()

        print("🔄 Gestures Reloaded CLEAN")

        # 🔓 Enable button again
        self.reload_btn.setEnabled(True)