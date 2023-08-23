
from parts.ultrasonic import ultrasonic
from parts.actuator import servoController
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

lowRD1 = np.array(cfg.RED_LOWER_BOUND_1)
uppRD1 = np.array(cfg.RED_UPPER_BOUND_1)

lowRD2 = np.array(cfg.RED_LOWER_BOUND_2)
uppRD2 = np.array(cfg.RED_UPPER_BOUND_2)

lowGR = np.array(cfg.GREEN_LOWER_BOUND)
uppGR = np.array(cfg.GREEN_UPPER_BOUND)

direction = cfg.STEERING_MIDDLE

rightUS = ultrasonic(23, 24)
middleUS = ultrasonic(27, 22)
leftUS = ultrasonic(10, 9)
camServo = servoController(cfg.CAM_SERVO_GPIO)

cam = camera(flip=True)
camThread = threading.Thread(target=cam.update, daemon=True)
camThread.start()

pid = ut.PIDController(cfg.BLOCK_KP, cfg.BLOCK_KI, cfg.BLOCK_KD, tolerance=5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(cfg.BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(cfg.WIRE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
time.sleep(1)

camServo.setAngle(cfg.CAM_SERVO_MIDDLE)
ut.drive(0, cfg.STEERING_MIDDLE, 1)
turnBlock = 'green'
turnCheck = False
turning = False
turnCount = 0
resetTurnCount = 0
time.sleep(0.5)
try:
    # Wait for start
    testImg = cam.get()
    xRed, xCentre, xGreen = (testImg.shape[1] * 20) // 100, (testImg.shape[1] * 50) // 100, (testImg.shape[1] * 80) // 100
    print("Wait for start...")
    while GPIO.input(cfg.BUTTON_GPIO):
        ut.drive(0, cfg.STEERING_MIDDLE, 1) 

    direction = GPIO.input(cfg.WIRE_GPIO)
    print(direction)

    time.sleep(0.5)
    while turnCount < 12:
        img = cam.get()
        image = img[120:350]

        maskRD1 = ut.getMask(image, lower=lowRD1, upper=uppRD1)
        maskRD2 = ut.getMask(image, lower=lowRD2, upper=uppRD2)
        maskRD = cv2.bitwise_or(maskRD1, maskRD2)
        maskGR = ut.getMask(image, lower=lowGR, upper=uppGR)

        maskOR = ut.getMask(image, lower=lowOR, upper=uppOR)
        maskBL = ut.getMask(image, lower=lowBL, upper=uppBL)

        xr, yr, wr, hr, ar = ut.findContour(maskRD, setArea=800, name="")
        xg, yg, wg, hg, ag = ut.findContour(maskGR, setArea=800, name="")  
        xo, yo, wo, ho, ao = ut.findContour(maskOR, setArea=1000, name="")  
        xb, yb, wb, hb, ab = ut.findContour(maskBL, setArea=1000, name="")  

        xR = xr + (wr // 2)
        xG = xg + (wg // 2)

        # ~~~~~~~~~ For debugging ~~~~~~~~~ #

        cv2.rectangle(image, (xr, yr), (xr+wr, yr+hr), (0, 0, 255), 2)
        cv2.rectangle(image, (xg, yg), (xg+wg, yg+hg), (0, 255, 0), 2)
        cv2.rectangle(image, (xo, yo), (xo+wo, yo+ho), (255, 0, 0), 2)
        cv2.rectangle(image, (xb, yb), (xb+wb, yb+hb), (0, 127, 255), 2)

        image = cv2.circle(image, (xr + wr//2, yr + hr//2), 3, (0, 0, 255), -1)
        image = cv2.circle(image, (xg + wg//2, yg + hg//2), 3, (0, 255, 0), -1)
        image = cv2.circle(image, (xo + wo//2, yo + ho//2), 3, (255, 0, 0), -1)
        image = cv2.circle(image, (xb + wb//2, yb + hb//2), 3, (0, 127, 255), -1)

        cv2.line(image, (xRed, 0), (xRed, 480), (0, 255, 255), 2)
        cv2.line(image, (xGreen, 0), (xGreen, 480), (255, 255, 0), 2)

        cv2.imwrite("/home/pi/self-driven-car/tmp-files/image.jpg", image)
        cv2.imwrite("/home/pi/self-driven-car/tmp-files/red.jpg", maskRD)
        cv2.imwrite("/home/pi/self-driven-car/tmp-files/green.jpg", maskGR)
        cv2.imwrite("/home/pi/self-driven-car/tmp-files/orange.jpg", maskOR)
        cv2.imwrite("/home/pi/self-driven-car/tmp-files/blue.jpg", maskBL)
    
        # ~~~~~~~~~ For debugging ~~~~~~~~~ #

        rightDist = ut.clamp(rightUS.get(), 2, 80)
        middleDist = ut.clamp(middleUS.get(), 2, 80)
        leftDist = ut.clamp(leftUS.get(), 2, 80)
        
        # Counter clockwise
        if direction:
            if yb > 175 or wb > 300:
                print("Blue: ", xb, yb, wb, hb, ab, xb * hb)
                if not turnCheck:
                    # ut.driveTimer(0.8, [20, cfg.STEERING_MIDDLE, 1])
                    ut.driveTimer(1, [0, cfg.STEERING_MIDDLE, 1])
                    turnCheck = True
                    continue   

            if turnCheck and (wg * hg) != 0: 
                print('green')
                ut.driveTimer(0.2, [20, cfg.STEERING_LEFT, 1])
                ut.driveTimer(0.2, [0, cfg.STEERING_MIDDLE, 1])
                turning = True

            elif turnCheck:
                print('red')
                turning = True
                turnCheck = False
                continue

        # Clockwise
        else:
            if yo > 175 or wo > 300:
                print("Orange: ", xo, yo, wo, ho, ao, xo * ho)
                if not turnCheck:
                    # ut.driveTimer(0.8, [20, cfg.STEERING_MIDDLE, 1])
                    ut.driveTimer(2 [0, cfg.STEERING_MIDDLE, 1])
                    turnCheck = True
                    continue  

            if turnCheck and (wg * hg) != 0: 
                print('green')
                turning = True

            elif turnCheck:
                print('red')
                ut.driveTimer(0.2, [20, cfg.STEERING_RIGHT, 1])
                ut.driveTimer(0.2, [0, cfg.STEERING_MIDDLE, 1])
                turnCheck = False
                continue

        # if turnCheck and time.time() - resetTurnCount > 5:
        #     turnCount += 1
        #     resetTurnCount = time.time()
        #     print(turnCount)

        # print("Red: ", xR, yR, wr, hr, ar)
        # print("Green: ", xG, wg, hg, ag)
        # print("Orange: ", wo, ho, ao)
        # print()

        if ar < ag  and (wg * hg) != 0: 
            if (wg * hg) < 12500:
                error = xG - xGreen
                error = round(pid.compute(error, 0), 2)
                turn_value = ut.clamp(error, -50, 50)
                steer = cfg.STEERING_MIDDLE + turn_value
            else: 
                steer = cfg.STEERING_MIDDLE

        elif ar > ag  and (wr * hr) != 0:
            if (wr * hr) < 12500 and wr < 200:
                error = xR - xRed
                error = round(pid.compute(error, 0), 2)
                turn_value = ut.clamp(error, -50, 50)
                steer = cfg.STEERING_MIDDLE + turn_value
            else: 
                steer = cfg.STEERING_MIDDLE

        else:   
            steer = cfg.STEERING_MIDDLE

        if rightDist < 3 or leftDist < 3:
            error = rightDist - leftDist
            error = round(pid.compute(error, 0), 2)
            turn_value = ut.clamp(error, -40, 40)
            steer = cfg.STEERING_MIDDLE + turn_value

        elif (wg * hg) == 0 and (wr * hr) == 0 and middleDist < 30:
            steer = cfg.STEERING_RIGHT

        ut.drive(20, steer, 1)

except KeyboardInterrupt:
    pass

except Exception as e:
    print(e)

print('[INFO] Exiting...')
ut.drive(0, cfg.STEERING_MIDDLE, 1)
cam.shutdown()
camServo.setAngle(cfg.CAM_SERVO_MIDDLE)
GPIO.cleanup()

