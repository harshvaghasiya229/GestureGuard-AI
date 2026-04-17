# 🧠 GestureGuard-AI

GestureGuard-AI is an advanced, AI-powered computer vision application that allows you to control your computer system completely hands-free using real-time hand gesture recognition. By leveraging state-of-the-art machine learning models and highly precise hand landmark tracking, GestureGuard-AI transforms your hand movements into system commands—from simple mouse tracking to complex system shortcuts.

## ✨ Key Features

- **Real-Time Hand Tracking**: Built on top of Google's MediaPipe, providing robust and incredibly fast hand landmark detection.
- **Custom Gesture Recognition Model**: Uses machine learning (Scikit-Learn/DL) trained on custom coordinate mappings to predict hand gestures accurately.
- **System Automation**: Translates detected gestures into system-level actions via PyAutoGUI (Mouse Move, Clicks, Scrolling) and native macOS commands (Volume Control, Mission Control, Launchpad).
- **Responsive HUD UI**: Features a sleek, futuristic, transparent "Iron Man" style Heads-Up Display (HUD) built with PyQt6.
- **Live Action Mapping**: Easily assign recognized gestures to any system action directly from the UI.
- **Built-in Gesture Recorder**: Record your own custom gestures quickly, allowing for endless customization and personalization of the AI model.
- **Jitter Smoothing**: Includes a custom smoothing algorithm to stabilize mouse movements and eliminate jitters.

## 🛠️ Technology Stack

- **Python 3.x**
- **Computer Vision**: OpenCV (`cv2`), MediaPipe
- **Machine Learning**: Scikit-Learn (Model `gesture_model.pkl`)
- **User Interface**: PyQt6
- **System Integration**: PyAutoGUI, macOS AppleScript (via `subprocess`)

## 📂 Project Structure

```
gesture_ai_system/
├── core/                   # Core business logic and AI
│   ├── controller.py       # Maps gestures to system actions
│   ├── detector.py         # MediaPipe hand detection logic
│   ├── dl_model.py         # Deep Learning model wrapper
│   └── gesture_model.py    # Hand gesture classification 
├── data/                   # Data storage for configs and models
│   ├── gesture_config.json # Action mappings
│   └── ...
├── ui/                     # PyQt6 User Interface components
│   ├── main_window.py      # Primary HUD and video feed
│   ├── gesture_panel.py    # Action assignment panel
│   └── recording_window.py # Interface to record new gestures
├── utils/                  # Helper utilities
│   └── smoothing.py        # Coordinate stabilization
├── main.py                 # Application entry point
├── config.py               # Global system configurations
└── requirements.txt        # Python dependencies
```

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have Python 3.9+ installed on your machine. This application also assumes you have a functional webcam.
*Note: Some system actions (e.g., volume control, mission control) are currently optimized for macOS.*

### 2. Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/your-username/GestureGuard-AI.git
cd gesture_ai_system

# Create and activate a virtual environment (Recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Running the System

Start the application by running:

```bash
python main.py
```

## 🎮 Usage

1. **Launch the app**: The HUD will appear showing your webcam feed along with tracked hand landmarks.
2. **Assign Actions**: Click the `⚡ Assign Action` button to map recognized gestures (e.g., "Peace Sign", "Fist") to your desired system command.
3. **Record New Gestures**: Want to teach the AI a new move? Click the `🎥 Add Gesture` button to open the recording panel, capture some data, and expand the model's vocabulary!
4. **Hands-free Control**: Perform the gestures in front of the camera. To stop/close the application, click the `❌ Close` button or hit `Command+Q` (macOS).

## 🔒 Permissions Breakdown (macOS)
Since GestureGuard-AI controls your mouse and executes system actions, you may need to grant your Terminal/IDE specific privacy permissions in macOS `System Settings > Privacy & Security`:
- **Camera Access** (For video feed)
- **Accessibility** (For PyAutoGUI mouse/keyboard control)
- **Automation** (For AppleScript volume/system control)

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

---
*Created by [Harsh Vaghasiya, Manan Chocha]*
