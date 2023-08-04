import RPi.GPIO as GPIO
import time

in1, in2, en = 19, 16, 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT) # In 1
GPIO.setup(in2, GPIO.OUT) # In 2
GPIO.setup(en, GPIO.OUT) # En
pwm = GPIO.PWM(en, 1000)
pwm.start(50)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.HIGH)
time.sleep(2)
GPIO.output(in1, GPIO.HIGH)
GPIO.output(in2, GPIO.LOW)
time.sleep(2)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
time.sleep(2)
GPIO.cleanup()