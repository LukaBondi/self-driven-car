from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep

pigpio_factory = PiGPIOFactory()
servo =AngularServo(7, min_angle=0, max_angle=270, min_pulse_width=0.0005, max_pulse_width=0.0025, pin_factory=pigpio_factory)
servo.angle = 180
sleep(2)
servo.angle = 90
sleep(2)
servo.angle = 135
sleep(2)
# servo.angle = 95
# sleep(2)

