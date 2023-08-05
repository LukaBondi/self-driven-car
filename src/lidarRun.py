from lidar import lidar
import threading
import time
import cv2

lidarPart = lidar()
lidarThread = threading.Thread(target=lidarPart.update, daemon=True)
lidarThread.start()
def main():
    pass
    # ft.drive(0, 95, 0)  
    # print(lidarPart.run())
    # time.sleep(1)
    # print('[INFO] GO!')

    # timeIt = time.time() 
    
    # print(f'[INFO] Total time: {time.time() - timeIt:.2f}s')



try:
    run = True
    while run:
        # print('\n[INFO] Running...')
        main()

except KeyboardInterrupt:
    pass
    #cv2.imwrite('a.jpg', frame)
except Exception as e:
    print(e)

print('[INFO] Exiting...')
lidarPart.shutdown()