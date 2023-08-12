from parts.actuator import motorController, servoController
import numpy as np
import cv2

from config import config
cfg = config()

motor = motorController(cfg.IN1, cfg.IN2, cfg.EN)
steering = servoController(cfg.STEERING_GPIO, cfg.SERVO_MIN_ANGLE, cfg.SERVO_MAX_ANGLE, 
    cfg.SERVO_MIN_PULSE_WIDTH, cfg.SERVO_MAX_PULSE_WIDTH)

# Drive controller  
def drive(self, speed: int = 0, angle: int = 90, direction: int = 0):
    motor.setDirection(direction)
    motor.setSpeed(speed)
    steering.setAngle(angle)

# Basic PID class
class PIDController:
    def __init__(self, Kp, Ki, Kd, tolerance=1):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.tolerance = 1
        self.prev_error = 0
        self.integral = 0

    def compute(self, setpoint, current_value):
        error = setpoint - current_value
        self.integral += error
        derivative = error - self.prev_error

        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        self.prev_error = error

        return output

    def atSetPoint(self):
        if abs(self.prev_error) < self.tolerance:
            return True
        else:
            return False

# Returns the bounding-box of the biggest contour in the given mask
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
