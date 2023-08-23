from parts.actuator import motorController, servoController
import numpy as np
import time
import cv2

from config import config
cfg = config()

motor = motorController(cfg.IN1, cfg.IN2, cfg.EN)
steering = servoController(cfg.STEERING_GPIO, cfg.SERVO_MIN_ANGLE, cfg.SERVO_MAX_ANGLE, 
    cfg.SERVO_MIN_PULSE_WIDTH, cfg.SERVO_MAX_PULSE_WIDTH)

# Drive controller  
def drive(speed: int = 0, angle: int = 90, direction: int = 0):
    motor.setDirection(direction)
    motor.setSpeed(speed)
    steering.setAngle(angle)

def driveTimer(timeMe, args=[0, cfg.STEERING_MIDDLE, 1]):
    timeS = time.time()
    while time.time() - timeS < timeMe:
        drive(*args)
        time.sleep(0.01)

# Basic PID class
class PIDController:
    def __init__(self, Kp, Ki, Kd, tolerance=1):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.tolerance = tolerance
        self.prev_error = 0
        self.integral = 0
        self.atSP = False

    def compute(self, current_value, setpoint):
        error = current_value - setpoint
        self.integral += error
        derivative = error - self.prev_error

        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        self.prev_error = error

        if abs(error) < self.tolerance:
            self.atSP = True
        else: 
            self.atSP = False
            
        return output

    def atSetPoint(self):
        return self.atSP

# Returns the value after clamping (Adapted from std::clamp in C++)
def clamp(value, minVal, maxVal):
    return max(min(value, maxVal), minVal)

def getLidarAvg(arr: np.array) -> float:
    arr = np.unique(arr)

    if(len(arr) > 1): 
        arr = np.delete(arr, np.where(arr == 120))

    return round(np.average(arr), 2)

# Returns the mask of the given image with the given color bounds
def getMask(image, lower: np.array, upper: np.array):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    return mask

# Returns the bounding-box of the biggest contour in the given mask
def findContour(mask, setArea=1000, name='something'):
    x, y, w, h, retArea = 0, 0, 0, 0, 0
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour) 
        if area >= setArea:
            retArea = area
            x, y, w, h = cv2.boundingRect(contour)
            if name != '':
                print(f'~~~\nFound {name}!\nX: {x}, Y: {y}, W: {w}, H: {h}, Area: {area}\n~~~')
            break
    
    return x, y, w, h, retArea
