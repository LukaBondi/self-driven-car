import numpy as np
import cv2

vs = cv2.VideoCapture(0)
_, frame = vs.read()
frame = cv2.flip(frame, -1)
cv2.imwrite("a.jpg", frame)
vs.release()
