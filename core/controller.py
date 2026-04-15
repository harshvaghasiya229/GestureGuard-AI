import json
import pyautogui
import time
import subprocess

CONFIG_PATH = "data/gesture_config.json"

class Controller:
    def __init__(self):
        self.last_action_time = 0
        self.cooldown = 1.0

    def load_config(self):
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except:
            return {}

    def execute(self, gesture, x=None, y=None):
        config = self.load_config()
        
        action = config.get(gesture, "none")
        print("👉 Gesture:", gesture)
        print("👉 Loaded config:", config)

        # ⏱️ cooldown
        if time.time() - self.last_action_time < self.cooldown:
            return

        print(f"Gesture: {gesture} → Action: {action}")
        # 🖱️ MOUSE
        if action == "move_mouse":
            pyautogui.moveTo(x, y)

        elif action == "click":
            pyautogui.click()

        elif action == "double_click":
            pyautogui.doubleClick()

        elif action == "right_click":
            pyautogui.rightClick()

        elif action == "scroll_up":
            pyautogui.scroll(300)

        elif action == "scroll_down":
            pyautogui.scroll(-300)

        # 🖥️ SYSTEM
        elif action == "desktop":
            pyautogui.hotkey("command", "f3")

        elif action == "launchpad":
            pyautogui.press("f4")

        elif action == "mission_control":
            pyautogui.hotkey("ctrl", "up")

        elif action == "next_app":
            pyautogui.hotkey("command", "tab")

        elif action == "prev_app":
            pyautogui.hotkey("command", "shift", "tab")

        # 🔊 VOLUME (macOS)
        elif action == "volume_up":
            subprocess.call(["osascript", "-e", "set volume output volume ((output volume of (get volume settings)) + 5)"])

        elif action == "volume_down":
            subprocess.call(["osascript", "-e", "set volume output volume ((output volume of (get volume settings)) - 5)"])

        elif action == "mute":
            subprocess.call(["osascript", "-e", "set volume with output muted"])

        # 📸 SCREENSHOT
        elif action == "screenshot":
            pyautogui.screenshot("screenshot.png")

        if action != "none":
            self.last_action_time = time.time()