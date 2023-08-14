from adafruit_rplidar import RPLidar, RPLidarException
from math import floor
import numpy as np
import time

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)

dist_data = np.array([120]*210, dtype='int16')
max_dist = 1500

try:
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:

            # Floor the angle, set the limit to 359 then convert it pi radians
            angle = min([359, floor(angle)]) 
            

            if angle < 75 or angle >= 285: # Filtering out the unnecessary angles 
                continue

            if distance > max_dist: # Filtering out the unnecessary distances
                distance = max_dist
            
            # print(f'Angle: {angle}, Dist: {distance}')

            # Fitting the angle range to the range [0, 180) (Integers only)
            dist_data[angle - 75] = floor(distance)

        # print(f'{dist_data}\n\n\n\n\n') 
        rightArr = np.unique(dist_data[0:70])
        leftArr = np.unique(dist_data[71:140])
        frontArr = np.unique(dist_data[141:210])
        
        # rightAvg = round(np.average(np.delete(rightArr, np.where(rightArr == 120))), 2)
        # leftAvg = round(np.average(np.delete(leftArr, np.where(leftArr == 120))), 2)
        # frontAvg = round(np.average(np.delete(frontArr, np.where(frontArr == 120))), 2)

        print(f'{rightArr}\n{leftArr}\n{frontArr}\n\n')
        print()

        # Resetting the distance values.
        dist_data = np.array([120]*210, dtype='int16')

except KeyboardInterrupt:
    print('Stopping.')
    
except IndexError:
    print(angle)

lidar.stop()
lidar.disconnect()
