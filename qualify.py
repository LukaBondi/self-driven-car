import imp
from camera import camera
import functions as ft
import threading
import time
import cv2

cam = camera()
def main():
    vs = threading.Thread(target=cam.update, daemon=True)
    vs.start()
    ft.drive(0, 95, 0)  
    time.sleep(1)
    print('[INFO] Waiting for the button to be pressed')
    while ft.getBtState(): # Not pressed
        pass
    time.sleep(0.5)
    print('[INFO] GO!')

    timeIt = time.time()
    numLines = 0
    mode = 0
    while numLines < 12:
        if not ft.getBtState():
            print(f'[INFO] Total time: {time.time() - timeIt:.2f}s')
            return

        # Acquire a frame from the camera
        ret, frame = cam.get()
        if not ret:
            continue
        frame = cv2.flip(frame, -1)

        # Image processing
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        crop = hsv[:, 300:340]

        maskBL = cv2.inRange(crop, ft.lowerBL, ft.upperBL)
        maskOR = cv2.inRange(crop, ft.lowerOR, ft.upperOR) 

        # Contours            
        bx, by, bw, bh = ft.findContour(maskBL, 400, '')
        ox, oy, ow, oh = ft.findContour(maskOR, 400, '')

        if False:
            continue

        if mode == 0: # Check line
            if by > 300:
                ft.turnTimer(0.8, [80, 95, 1])
                ft.turnTimer(0.8, [80, 115, 1])
                numLines += 1
                print(f'Passed {numLines}, mode = {mode}')
                mode = 1
            elif oy > 300:
                ft.turnTimer(0.8, [80, 95, 1])
                ft.turnTimer(0.8, [80, 65, 1])
                numLines += 1
                print(f'Passed {numLines}, mode = {mode}')
                mode = 2
            elif not ft.sensorDetect():
                ft.drive(80, 95, 1)
                time.sleep(0.01)
        
        elif mode == 1: # blue
            if by > 300:
                ft.turnTimer(0.8, [80, 95, 1])
                ft.turnTimer(0.8, [80, 115, 1])
                print(f'Passed {numLines}, mode = {mode}')
                numLines += 1
            elif not ft.sensorDetect():
                ft.drive(80, 95, 1)
                time.sleep(0.01)

        elif mode == 2: 
            if oy > 300:
                ft.turnTimer(0.8, [80, 95, 1])
                ft.turnTimer(0.8, [80, 65, 1])
                print(f'Passed {numLines}, mode = {mode}')
                numLines += 1
            elif not ft.sensorDetect(invert=True):
                ft.drive(80, 95, 1)
                time.sleep(0.01)
    
    delay = time.time()
    while time.time() - delay < 1:
        if mode == 2:
            if not ft.sensorDetect(invert=True):
                ft.drive(80, 95, 1)
                time.sleep(0.01)
        elif not ft.sensorDetect():
            ft.drive(80, 95, 1)
            time.sleep(0.01)

    print(f'[INFO] Total time: {time.time() - timeIt:.2f}s')

try:
    run = True
    while run:
        print('\n[INFO] Running...')
        main()
        delay = time.time()
        while time.time() - delay < 3:
            if not ft.getBtState():
                run = False
                break

except KeyboardInterrupt:
    pass
    #cv2.imwrite('a.jpg', frame)
except Exception as e:
    print(e)

print('[INFO] Exiting...')
ft.shutdown()
cam.shutdown()