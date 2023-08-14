import RPi.GPIO as GPIO
import time
import math

trig = 23
echo = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
speed_of_sound = 331.3 * math.sqrt(1 + (20 / 273.15)) * 50

while(True):
    try:
        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig, False)

        while GPIO.input(echo) == 0:
            pulse_start = time.time()

        while GPIO.input(echo) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * speed_of_sound  # Speed of sound: 343 m/s

        distance = int(distance)

        print(f'Distance: {distance}')
        time.sleep(0.25)
        
    except KeyboardInterrupt:
        GPIO.cleanup()
        break