import RPi.GPIO as GPIO
import time
import math


class camera:
    def __init__(self, trig, echo, temp=20):
        self.trig = trig
        self.echo = echo

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(trig, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)

        self.speed_of_sound = 331.3 * math.sqrt(1 + (temp / 273.15)) * 50

        self.prev_dist = 0
        self.distance = 0

        self.running = True

    def update(self):
        while self.running:
            GPIO.output(self.trig, True)
            time.sleep(0.00001)
            GPIO.output(self.trig, False)

            while GPIO.input(self.echo) == 0:
                pulse_start = time.time()

            while GPIO.input(self.echo) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            dist = pulse_duration * self.speed_of_sound  # Speed of sound: 343 m/s

            if self.distance > 500:
                dist = self.prev_dist

            self.distance = round(dist, 2)

    def get(self):
        return self.distance

    def shutdown(self):
        self.running = False
        time.sleep(0.5)
        GPIO.cleanup()
