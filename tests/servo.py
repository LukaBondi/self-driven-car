from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep

pigpio_factory = PiGPIOFactory()
servo =AngularServo(7, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025, pin_factory=pigpio_factory)

servo.angle = 90
sleep(1)

## Steering servo ##

# servo.angle = 50 # Left
# sleep(1)
# servo.angle = 95 # Straight
# sleep(2)
# servo.angle = 130 # Right
# sleep(2)

## Steering servo ##

## Camera servo ##

# servo.angle = 0 # Left
# sleep(1)
# servo.angle = 45 # Slightly-Left
# sleep(1)
# servo.angle = 82 # Straight
# sleep(2)
# servo.angle = 130 # Slightly-Right
# sleep(1)
# servo.angle = 170 # Right
# sleep(2)

## Camera servo ##
