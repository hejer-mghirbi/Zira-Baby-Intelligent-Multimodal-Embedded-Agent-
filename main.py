import threading
import queue
import time

from speech.recognizer import SpeechRecognizer
from command.processor import CommandProcessor
from tts.speaker import Speaker
from vision.camera import Camera
from config.settings import MODEL_PATH
from screen.face import FaceDisplay

# =========================
# INITIALIZATION
# =========================
face = FaceDisplay()
recognizer = SpeechRecognizer(MODEL_PATH)
speaker = Speaker(face)
camera = Camera()
processor = CommandProcessor(speaker, camera)

print("System ready. Speak...")

# =========================
# QUEUES (communication)
# =========================
speech_queue = queue.Queue()
vision_queue = queue.Queue()

# =========================
# THREADS
# =========================

def speech_loop():
    """Continuously listens for speech and pushes text to queue"""
    while True:
        try:
            face.set_state("listening")
            text = recognizer.listen()

            if text and text.strip() != "":
                speech_queue.put(text)

        except Exception as e:
            print("[Speech Error]", e)


def vision_loop():
    """Continuously runs object detection"""
    while True:
        try:
            objects = camera.detect_objects()  # you must have this method

            if objects is not None:
                vision_queue.put(objects)

            # Reduce CPU usage (important on Raspberry Pi)
            time.sleep(1)

        except Exception as e:
            print("[Vision Error]", e)


# =========================
# START THREADS
# =========================
threading.Thread(target=speech_loop, daemon=True).start()
threading.Thread(target=vision_loop, daemon=True).start()

# =========================
# MAIN LOOP (NON-BLOCKING)
# =========================
last_objects = []

while True:

    # -------------------------
    # HANDLE SPEECH INPUT
    # -------------------------
    if not speech_queue.empty():
        text = speech_queue.get()

        face.set_state("thinking")
        print("You said:", text)

        processor.process(text)

    # -------------------------
    # HANDLE VISION INPUT
    # -------------------------
    if not vision_queue.empty():
        objects = vision_queue.get()
        last_objects = objects

        print("Detected:", objects)

        # OPTIONAL: Awareness behavior
        if "person" in objects:
            speaker.say("I see someone")

    # Small delay to stabilize CPU
    time.sleep(0.01)