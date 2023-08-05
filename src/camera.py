import cv2

class camera:
    def __init__(self, port=0):
        self.vs = cv2.VideoCapture(port)
        self.running = True
        self.img = None

    def update(self):
        while self.running:
            _, self.img = self.vs.read()

    def run(self):
        return self.img

    def shutdown(self):
        self.running = False
        self.vs.release()
