
from parts.ultrasonic import ultrasonic
from parts.camera import camera
import RPi.GPIO as GPIO

import utils as ut
import threading
import time

import numpy as np
import cv2

from config import config
cfg = config()

lowOR = np.array(cfg.ORANGE_LOWER_BOUND)
uppOR = np.array(cfg.ORANGE_UPPER_BOUND)

lowBL = np.array(cfg.BLUE_LOWER_BOUND)
uppBL = np.array(cfg.BLUE_UPPER_BOUND)

direction = cfg.STEERING_MIDDLE

rightUS = ultrasonic(23, 24)
middleUS = ultrasonic(27, 22)
leftUS = ultrasonic(10, 9)

cam = camera(flip=True)
camThread = threading.Thread(target=cam.update, daemon=True)
camThread.start()

pid = ut.PIDController(cfg.MIDDLE_KP, cfg.MIDDLE_KI, cfg.MIDDLE_KD, tolerance=10)

GPIO.setmode(GPIO.BCM)
GPIO.setup(cfg.BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

time.sleep(1)


try:
    # Wait for start
    print("Wait for start...")
    while GPIO.input(cfg.BUTTON_GPIO):
        ut.drive(0, cfg.STEERING_MIDDLE, 1) 

    time.sleep(0.1)
    while (True):
        image = cam.get()
        image = image[180:] # Crop out details

        maskOR = ut.getMask(image, lower=lowOR, upper=uppOR)
        maskBL = ut.getMask(image, lower=lowBL, upper=uppBL)
    
        xo, yo, wo, ho, ao = ut.findContour(maskOR, setArea=1500, name="")
        xb, yb, wb, hb, ab = ut.findContour(maskBL, setArea=1500, name="")
        
        cv2.rectangle(image, (xo, yo), (xo+wo, yo+ho), (0, 127, 255), 2)
        cv2.rectangle(image, (xb, yb), (xb+wb, yb+hb), (0, 127, 255), 2)

        # For debugging #

        cv2.imwrite("/home/pi/self-driven-car/src/test.jpg", image)
        # cv2.imwrite("/home/pi/self-driven-car/src/maskOr.jpg", maskOR)
        # cv2.imwrite("/home/pi/self-drive
        # n-car/src/maskBl.jpg", maskBL)

        # ~~~~~~~~~~~~ #
        
        if ao > ab:
            print("Steer right")
            direction = cfg.STEERING_RIGHT
            lowerBound = lowOR
            upperBound = uppOR
            break
        elif ao < ab:
            print("Steer left")
            direction = cfg.STEERING_LEFT
            lowerBound = lowBL
            upperBound = uppBL
            break
        else:
            rightDist = ut.clamp(rightUS.get(), 5, 80)
            leftDist = ut.clamp(leftUS.get(), 5, 80)

            error = rightDist - leftDist
            error = round(pid.compute(error, 0), 2)
            turn_value = ut.clamp(error, -20, 20)

            ut.drive(40, cfg.STEERING_MIDDLE + turn_value, 1)

        time.sleep(0.1)

    # ut.drive(0, cfg.STEERING_MIDDLE, 1)
    # time.sleep(0.25)

    # ut.drive(0, direction, 1)
    # time.sleep(2)

    # ut.drive(0, cfg.STEERING_MIDDLE, 1)
    # time.sleep(0.5)

    turnState = False
    turnCount = 0
    timeS = time.time()
    countdown = time.time()
    while(time.time() - countdown < 1.8):
        if turnCount < 12:
            countdown = time.time()
            if not turnState:
                image = cam.get()
                image = image[180:] # Crop out details

                mask = ut.getMask(image, lower=lowerBound, upper=upperBound)
                x, y, w, h, a = ut.findContour(mask, setArea=1500, name="")

                if w != 0 and h != 0:
                    turnState = True
                    turnCount += 1
                    print(turnCount)
                    timeS = time.time()

            elif turnState and time.time() - timeS > 2.5:
                turnState = False

        rightDist = ut.clamp(rightUS.get(), 5, 100)
        middleDist = ut.clamp(middleUS.get(), 5, 500)
        leftDist = ut.clamp(leftUS.get(), 5, 100)
        # print(middleUS.get())

        error = rightDist - leftDist
        error = round(pid.compute(error, 0), 2)
        turn_value = ut.clamp(error, -15, 15)

        if middleDist < 55:
            ut.drive(100, direction, 1)

            if turnCount == 12:
                turnCount += 1
                countdown = time.time()
                
        elif abs(error) < 100:
            ut.drive(100, cfg.STEERING_MIDDLE + turn_value, 1)
        else:
            ut.drive(0, cfg.STEERING_MIDDLE + turn_value, 1)

        # # print('{} | {} | {}'.format(rightDist, middleDist, leftDist))
        # # time.sleep(0.02)

    ut.drive(0, cfg.STEERING_MIDDLE, 1)
    time.sleep(0.5)

except KeyboardInterrupt:
    pass

# except Exception as e:
#     print(e)

print('[INFO] Exiting...')
cam.shutdown()
GPIO.cleanup()

