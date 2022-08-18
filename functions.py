from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
import RPi.GPIO as GPIO
import numpy as np
import time
import cv2

pigpio_factory = PiGPIOFactory()

sL, sR, bt = 22, 23, 11 
in1, in2, en = 19, 16, 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(sL, GPIO.IN) # Sensor left
GPIO.setup(sR, GPIO.IN) # Sensor right
GPIO.setup(bt, GPIO.IN, pull_up_down=GPIO.PUD_UP) # button
GPIO.setup(in1, GPIO.OUT) # In 1
GPIO.setup(in2, GPIO.OUT) # In 2
GPIO.setup(en, GPIO.OUT) # En

motor = GPIO.PWM(en, 1000)
motor.start(0) 
servo = AngularServo(8, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0025, pin_factory=pigpio_factory)

# Lines
lowerBL = np.array([90,144,30])
upperBL = np.array([151,255,98])
lowerOR = np.array([0,8,0])
upperOR = np.array([31,168,146])

def drive(speed = 0, angle = 102, direction = 0):
    if speed == 0 or direction == 0: # No movement
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        time.sleep(0.5)

    if speed > 100:
        speed = 100
    elif speed < 0:
        speed = 0

    if angle > 125:
        angle = 125
    elif angle < 55:
        angle = 55

    motor.ChangeDutyCycle(speed)
    servo.angle = angle
    if direction > 0: # Forward
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
    elif direction < 0: # Backward
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)

def sensorDetect(invert=False):
    # Sensor inputs
    sensorL = GPIO.input(sL)    
    sensorR = GPIO.input(sR) 

    # Sensor logic
    if not sensorL and not sensorR: # 11
        if invert:
            drive(80, 55, 1) # Forward right
        else:
            drive(80, 125, 1) # Forward left
    elif sensorL and not sensorR: # 01
        drive(80, 125, 1) # Forward left
    elif not sensorL and sensorR: # 10
        drive(80, 55, 1) # Forward right
    else:
        return False
    time.sleep(0.1)
    return True

def turnTimer(times, dArgs=[0, 102, 0]):
    timeS = time.time()
    while time.time() - timeS < times:
        # Turning
        drive(*dArgs)
        time.sleep(0.01)
            
        #if sensorDetect():
        #    break

def findContour(mask, setArea=1000, name='something'):
    x, y, w, h = 0, 0, 0, 0
    image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour) 
        if area >= setArea:
            x, y, w, h = cv2.boundingRect(contour)
            if name != '':
                print(f'~~~\nFound {name}!\nX: {x}, Y: {y}, W: {w}, H: {h}, Area: {area}\n~~~')
            break
    
    return x, y, w, h

def getBtState():
    return GPIO.input(bt)

def shutdown():
    drive(0, 95, 0) # Forward center
    time.sleep(0.5)
    GPIO.cleanup()