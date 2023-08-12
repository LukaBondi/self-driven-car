from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pigpio_factory = PiGPIOFactory()

def motorController():
    def __init__(self, in1=19, in2=16, en=13, freq=1000):
        GPIO.setup(in1, GPIO.OUT) # In 1
        GPIO.setup(in2, GPIO.OUT) # In 2
        GPIO.setup(en, GPIO.OUT) # En

        self.in1 = in1
        self.in2 = in2
        self.pwm = GPIO.PWM(en, freq)
        self.pwm.start(0)
        
    def setDirection(self, direction: int):
        if direction > 0:
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)
        elif direction < 0:
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
        else:
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.LOW)
        
    def setSpeed(self, speed: int):
        if speed > 100:
            speed = 100
        elif speed < 0:
            speed = 0

        self.pwm.ChangeDutyCycle(speed)
        
def servoController():
    def __init__(self, port=7, minAngle=0, maxAngle=180, min_pulse_width=0.0005, max_pulse_width=0.0025):

        self.servo =AngularServo(port, min_angle=minAngle, max_angle=maxAngle, min_pulse_width=min_pulse_width, 
                        max_pulse_width=max_pulse_width, pin_factory=pigpio_factory)
        
    def setAngle(self, angle: int):
        self.servo.angle = angle


