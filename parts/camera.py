import cv2

class camera:
    def __init__(self, port=0):
        self.vs = cv2.VideoCapture(port)
        self.img = None

    def update(self):
        while True:
            _, self.img = self.vs.read()

    def run(self):
        return self.img

    def shutdown(self):
        self.vs.release()
