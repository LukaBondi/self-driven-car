import time
import cv2

class camera:
    def __init__(self, port=0, flip=False):
        self.vs = cv2.VideoCapture(port)
        self.running = True
        self.flip = flip
        self.img = None

    def update(self):
        while self.running:
            _, image = self.vs.read()
            if self.flip:
                self.img = cv2.flip(image, -1)
            else:
                self.img = image

    def get(self):
        return self.img

    def shutdown(self):
        self.running = False
        time.sleep(0.5)
        self.vs.release()
