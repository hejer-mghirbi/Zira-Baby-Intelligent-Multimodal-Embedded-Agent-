import cv2
import numpy as np
import time
import random
import threading


class FaceDisplay:
    def __init__(self):
        self.state = "idle"

        # ======================
        # BLINK SYSTEM
        # ======================
        self.last_blink = time.time()
        self.blink_duration = 0.15
        self.is_blinking = False

        # ======================
        # MOUTH ANIMATION CONTROL
        # ======================
        self.mouth_open = 20
        self.mouth_direction = 1
        self.last_mouth_update = time.time()

        # ======================
        # THREAD CONTROL
        # ======================
        self.running = True
        self.thread = threading.Thread(target=self._render_loop, daemon=True)
        self.thread.start()

    # ======================
    # STATE CONTROL
    # ======================
    def set_state(self, state):
        self.state = state

    # ======================
    # BLINK LOGIC
    # ======================
    def _update_blink(self):
        current_time = time.time()

        if current_time - self.last_blink > random.uniform(2, 4):
            self.is_blinking = True
            self.last_blink = current_time

        if self.is_blinking and current_time - self.last_blink > self.blink_duration:
            self.is_blinking = False

    # ======================
    # MOUTH ANIMATION (SMOOTH)
    # ======================
    def _update_mouth(self):
        if self.state != "speaking":
            self.mouth_open = 20
            return

        now = time.time()

        if now - self.last_mouth_update > 0.1:
            self.mouth_open += self.mouth_direction * 5

            if self.mouth_open > 40:
                self.mouth_direction = -1
            elif self.mouth_open < 15:
                self.mouth_direction = 1

            self.last_mouth_update = now

    # ======================
    # RENDER FACE
    # ======================
    def _draw_face(self):
        self._update_blink()
        self._update_mouth()

        img = np.ones((400, 400, 3), dtype=np.uint8) * 240

        left_eye = (130, 150)
        right_eye = (270, 150)

        # eye behavior
        if self.state == "listening":
            radius = 35
        elif self.state == "thinking":
            radius = 20
        else:
            radius = 28

        # blinking
        if self.is_blinking:
            cv2.line(img, (100, 150), (160, 150), (0, 0, 0), 5)
            cv2.line(img, (240, 150), (300, 150), (0, 0, 0), 5)
        else:
            cv2.circle(img, left_eye, radius, (0, 0, 0), -1)
            cv2.circle(img, right_eye, radius, (0, 0, 0), -1)

            offset = 0
            if self.state == "thinking":
                offset = -5
            elif self.state == "listening":
                offset = 5

            cv2.circle(img, (left_eye[0] + offset, left_eye[1]), 8, (255, 255, 255), -1)
            cv2.circle(img, (right_eye[0] + offset, right_eye[1]), 8, (255, 255, 255), -1)

        # mouth
        if self.state == "speaking":
            cv2.ellipse(img, (200, 280), (60, self.mouth_open), 0, 0, 360, (0, 0, 0), -1)

        elif self.state == "thinking":
            cv2.line(img, (160, 280), (240, 280), (0, 0, 0), 3)

        else:
            cv2.ellipse(img, (200, 280), (60, 20), 0, 0, 180, (0, 0, 0), 3)

        return img

    # ======================
    # MAIN LOOP (CRITICAL FIX)
    # ======================
    def _render_loop(self):
        while self.running:
            img = self._draw_face()

            cv2.imshow("Zira baby", img)

            # REQUIRED for OpenCV refresh
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.running = False
                break

        cv2.destroyAllWindows()

    # ======================
    # STOP CLEANLY
    # ======================
    def stop(self):
        self.running = False