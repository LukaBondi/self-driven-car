from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
import RPi.GPIO as GPIO
import time

pigpio_factory = PiGPIOFactory()
servo = AngularServo(7, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025, pin_factory=pigpio_factory)

in1, in2, en = 19, 16, 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT) # In 1
GPIO.setup(in2, GPIO.OUT) # In 2
GPIO.setup(en, GPIO.OUT) # En
pwm = GPIO.PWM(en, 1000)
pwm.start(100)

try:
    timeS = time.time()
    while(time.time() - timeS < 3):
        servo.angle = 132
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)

    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    time.sleep(0.5)

except KeyboardInterrupt:
    pass

except Exception as e:
    print(e)

GPIO.cleanup()
