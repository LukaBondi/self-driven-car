import numpy as np
import cv2

vs = cv2.VideoCapture(0)

while True:
    _, frame = vs.read()
    frame = cv2.flip(frame, -1)
    #print(_)
    if _:
        print("Saved!")
        cv2.imwrite("/home/pi/self-driven-car/tmp-files/test.jpg", frame)
        break
vs.release()
