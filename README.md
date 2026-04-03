🤖 Zira Baby – Multimodal Embodied AI Agent

Zira Baby is a multimodal embodied AI system running on a Raspberry Pi.
It integrates speech recognition, computer vision, text-to-speech, and physical mobility into a unified interactive robot.

The system is designed as part of a final-year engineering project (PFA), aligned with Industry 5.0 concepts of human-machine interaction.

🎯 Features
🎤 Offline speech recognition using Vosk
🧠 Intent-based command processing
👁 Real-time object detection using OpenCV (MobileNet SSD)
🔊 Offline text-to-speech using pyttsx3
😊 Animated face displayed on Raspberry Pi touchscreen
🚗 Voice-controlled robot mobility (forward, backward, left, right)
⚡ Multithreaded architecture for real-time interaction
🧠 System Architecture

The system is modular and composed of the following components:

speech/        → Speech recognition (Vosk)
command/       → Intent processing & decision layer
vision/        → Object detection (MobileNet SSD)
tts/           → Speech synthesis
screen/        → Animated face UI
movement/      → Motor control (L298N)
config/        → Configuration files
main.py        → System orchestration
🔄 Workflow
User speaks a command
Speech is converted to text
Intent is detected
System triggers corresponding action:
movement
vision analysis
speech response
Face UI updates (listening, thinking, speaking)
🧠 AI Models Used
🎤 Speech Recognition
Model: Vosk (offline)
Advantage: lightweight, works without internet
👁 Computer Vision
Model: MobileNet SSD (Caffe, via OpenCV DNN)
Detects indoor objects:
person, chair, sofa, tvmonitor, bottle, diningtable, pottedplant
⚙️ Hardware Requirements
Raspberry Pi (recommended: Pi 4)
Raspberry Pi Camera or USB webcam
Microphone
Speaker
L298N Motor Driver
4 DC Motors + wheels
External battery
Raspberry Pi Touch Display
🧪 Installation & Setup
1. Clone repository
git clone https://github.com/your-username/zira-baby.git
cd zira-baby
2. Install dependencies
pip install opencv-python vosk pyttsx3 sounddevice numpy
3. Download Vosk model

Download a model from:
https://alphacephei.com/vosk/models

Then update path in:

config/settings.py
4. Run the system
python main.py
🎮 Example Commands
“Hello”
“Take a picture”
“What do you see”
“Move forward”
“Turn left”
“Stop”
⚠️ Limitations
Keyword-based intent recognition (not conversational)
Moderate latency on Raspberry Pi
Limited object detection accuracy (MobileNet SSD)
No autonomous navigation yet
🚀 Future Improvements
Upgrade to YOLO Nano for better detection
Add autonomous navigation (obstacle avoidance)
Improve NLP with lightweight AI models
Enhance emotional interaction (face + voice)
👩‍💻 Author

Final Year Engineering Project
Field: Embedded Systems & AI
