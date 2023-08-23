import RPi.GPIO as GPIO
import time
import math


class ultrasonic:
    def __init__(self, trig, echo: list, temp=20):
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
        # while self.running:
        GPIO.output(self.trig, True)
        time.sleep(0.001)
        GPIO.output(self.trig, False)

        timeS = time.time()
        pulse_start = time.time()
        while GPIO.input(self.echo) == 0 and time.time() - timeS < 0.25:# and pulse_start < 0.025:
            pulse_start = time.time()

        timeS = time.time()
        pulse_end = time.time()
        while GPIO.input(self.echo) == 1 and time.time() - timeS < 0.25:# and pulse_end < 0.01:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        # print(self.speed_of_sound)
        dist = pulse_duration * self.speed_of_sound  # Speed of sound: 343 m/s

        # if self.distance > 500:
        #     dist = self.prev_dist

        self.distance = round(dist, 2)

    def get(self):
        self.update()
        return self.distance

    def shutdown(self):
        self.running = False
        time.sleep(0.5)
        GPIO.cleanup()
