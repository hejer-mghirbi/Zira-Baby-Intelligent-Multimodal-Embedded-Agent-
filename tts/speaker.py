import pyttsx3
import threading
import queue


class Speaker:
    def __init__(self, face=None):
        self.face = face

        # =========================
        # SPEECH QUEUE (IMPORTANT)
        # =========================
        self.queue = queue.Queue()

        # =========================
        # ENGINE INIT (ONLY ONCE)
        # =========================
        self.engine = pyttsx3.init()

        self.voice_id = None
        self.rate = 165

        voices = self.engine.getProperty('voices')

        for v in voices:
            if "Zira" in v.name:
                self.voice_id = v.id
                break

        if self.voice_id:
            self.engine.setProperty('voice', self.voice_id)

        self.engine.setProperty('rate', self.rate)

        # =========================
        # THREAD CONTROL
        # =========================
        self.running = True

        self.thread = threading.Thread(target=self._speech_loop, daemon=True)
        self.thread.start()

    # =========================
    # PUBLIC SPEAK METHOD
    # =========================
    def speak(self, text):
        print("Zira baby:", text)
        self.queue.put(text)

    # =========================
    # INTERNAL SPEECH LOOP
    # =========================
    def _speech_loop(self):
        while self.running:
            text = self.queue.get()

            if text is None:
                continue

            try:
                if self.face:
                    self.face.set_state("speaking")

                self.engine.say(text)
                self.engine.runAndWait()

                if self.face:
                    self.face.set_state("idle")

            except Exception as e:
                print("[TTS Error]", e)

    # =========================
    # STOP CLEANLY
    # =========================
    def stop(self):
        self.running = False
        self.queue.put(None)

        try:
            self.engine.stop()
        except:
            pass