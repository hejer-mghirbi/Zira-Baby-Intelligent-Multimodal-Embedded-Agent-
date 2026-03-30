# movement/motor_controller.py

import RPi.GPIO as GPIO
import time


class MotorController:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # =========================
        # MOTOR PINS
        # =========================
        self.IN1 = 17
        self.IN2 = 27
        self.IN3 = 22
        self.IN4 = 23

        self.ENA = 18  # PWM left
        self.ENB = 19  # PWM right

        # Setup pins
        pins = [self.IN1, self.IN2, self.IN3, self.IN4, self.ENA, self.ENB]
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)

        # =========================
        # PWM SETUP
        # =========================
        self.pwm_left = GPIO.PWM(self.ENA, 1000)   # 1kHz
        self.pwm_right = GPIO.PWM(self.ENB, 1000)

        self.pwm_left.start(0)
        self.pwm_right.start(0)

        self.speed = 60  # default speed (0–100)

    # =========================
    # INTERNAL HELPERS
    # =========================

    def _set_speed(self, speed):
        self.speed = max(0, min(100, speed))
        self.pwm_left.ChangeDutyCycle(self.speed)
        self.pwm_right.ChangeDutyCycle(self.speed)

    def _stop_motors(self):
        GPIO.output(self.IN1, 0)
        GPIO.output(self.IN2, 0)
        GPIO.output(self.IN3, 0)
        GPIO.output(self.IN4, 0)

    # =========================
    # MOVEMENT FUNCTIONS
    # =========================

    def forward(self, speed=None):
        if speed:
            self._set_speed(speed)

        GPIO.output(self.IN1, 1)
        GPIO.output(self.IN2, 0)

        GPIO.output(self.IN3, 1)
        GPIO.output(self.IN4, 0)

    def backward(self, speed=None):
        if speed:
            self._set_speed(speed)

        GPIO.output(self.IN1, 0)
        GPIO.output(self.IN2, 1)

        GPIO.output(self.IN3, 0)
        GPIO.output(self.IN4, 1)

    def left(self, speed=None):
        if speed:
            self._set_speed(speed)

        # Left wheels backward, right forward
        GPIO.output(self.IN1, 0)
        GPIO.output(self.IN2, 1)

        GPIO.output(self.IN3, 1)
        GPIO.output(self.IN4, 0)

    def right(self, speed=None):
        if speed:
            self._set_speed(speed)

        # Left wheels forward, right backward
        GPIO.output(self.IN1, 1)
        GPIO.output(self.IN2, 0)

        GPIO.output(self.IN3, 0)
        GPIO.output(self.IN4, 1)

    def stop(self):
        self._stop_motors()

    # =========================
    # CLEANUP (VERY IMPORTANT)
    # =========================

    def cleanup(self):
        self.stop()
        self.pwm_left.stop()
        self.pwm_right.stop()
        GPIO.cleanup()