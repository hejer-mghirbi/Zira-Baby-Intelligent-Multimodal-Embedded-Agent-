class CommandProcessor:
    def __init__(self, speaker, camera, motor_controller=None):
        self.speaker = speaker
        self.camera = camera
        self.motor = motor_controller

        # Memory (VERY IMPORTANT for "AI feel")
        self.last_seen_objects = []

        # =========================
        # INTENTS (structured)
        # =========================
        self.intents = {
            "greet": ["hello", "hi", "hey"],
            "capture_image": ["take a picture", "capture image", "photo", "picture"],
            "analyze_scene": ["what do you see", "scan", "analyze", "look around"],
            "move_forward": ["move forward", "go forward", "advance"],
            "move_backward": ["move backward", "go backward"],
            "turn_left": ["turn left", "go left"],
            "turn_right": ["turn right", "go right"],
            "stop_movement": ["stop moving", "stop"],
            "shutdown": ["exit", "shutdown"]
        }

        # =========================
        # ACTION MAP
        # =========================
        self.actions = {
            "greet": self.greet,
            "capture_image": self.capture_image,
            "analyze_scene": self.analyze_scene,
            "move_forward": self.move_forward,
            "move_backward": self.move_backward,
            "turn_left": self.turn_left,
            "turn_right": self.turn_right,
            "stop_movement": self.stop_movement,
            "shutdown": self.stop_system
        }

    # =========================
    # MAIN PROCESS FUNCTION
    # =========================
    def process(self, text):
        text = text.lower()

        intent = self.match_intent(text)

        if intent:
            return self.actions[intent]()
        else:
            return self.unknown_command()

    # =========================
    # INTENT MATCHING
    # =========================
    def match_intent(self, text):
        for intent, patterns in self.intents.items():
            for pattern in patterns:
                if pattern in text:
                    return intent
        return None

    # =========================
    # ACTIONS
    # =========================

    def greet(self):
        self.speaker.speak("Hello, I am Zira baby. How can I help you?")

    def capture_image(self):
        self.speaker.speak("Taking a picture now")
        frame = self.camera.capture_image()

        if frame is None:
            self.speaker.speak("I could not access the camera")
        else:
            self.speaker.speak("Image captured successfully")

    def analyze_scene(self):
        self.speaker.speak("Analyzing the room")

        objects = self.camera.analyze_scene()
        self.last_seen_objects = objects  # store memory

        if not objects:
            self.speaker.speak("I do not detect anything important")
        else:
            if "person" in objects:
                self.speaker.speak("I see a person in front of me")
            else:
                detected = ", ".join(objects[:3])
                self.speaker.speak(f"I can see {detected}")

    # =========================
    # MOVEMENT (SAFE VERSION)
    # =========================

    def move_forward(self):
        if self.motor:
            self.speaker.speak("Moving forward")
            self.motor.forward()
        else:
            self.speaker.speak("Motor controller not connected")

    def move_backward(self):
        if self.motor:
            self.speaker.speak("Moving backward")
            self.motor.backward()
        else:
            self.speaker.speak("Motor controller not connected")

    def turn_left(self):
        if self.motor:
            self.speaker.speak("Turning left")
            self.motor.left()
        else:
            self.speaker.speak("Motor controller not connected")

    def turn_right(self):
        if self.motor:
            self.speaker.speak("Turning right")
            self.motor.right()
        else:
            self.speaker.speak("Motor controller not connected")

    def stop_movement(self):
        if self.motor:
            self.speaker.speak("Stopping movement")
            self.motor.stop()
        else:
            self.speaker.speak("Nothing to stop")

    # =========================
    # SYSTEM CONTROL
    # =========================

    def stop_system(self):
        self.speaker.speak("Stopping system. Goodbye")
        self.camera.release()

        if self.motor:
            self.motor.stop()

        exit()

    # =========================
    # FALLBACK
    # =========================

    def unknown_command(self):
        self.speaker.speak("I did not understand the command")