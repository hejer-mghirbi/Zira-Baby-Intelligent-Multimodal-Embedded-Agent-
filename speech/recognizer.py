from vosk import Model, KaldiRecognizer
import sounddevice as sd
import json


class SpeechRecognizer:
    def __init__(self, model_path, sample_rate=16000):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, sample_rate)
        self.sample_rate = sample_rate

        # Open stream ONCE (important)
        self.stream = sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=8000,
            dtype='int16',
            channels=1
        )
        self.stream.start()

    # =========================
    # LISTEN FUNCTION
    # =========================
    def listen(self):
        """Blocking listen, returns recognized text"""

        try:
            while True:
                data, _ = self.stream.read(4000)
                data = bytes(data)

                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").strip()

                    # Filter empty / noise
                    if text and len(text) > 1:
                        return text

        except Exception as e:
            print("[Recognizer Error]", e)
            return ""

    # =========================
    # CLEANUP (IMPORTANT)
    # =========================
    def close(self):
        try:
            self.stream.stop()
            self.stream.close()
        except:
            pass