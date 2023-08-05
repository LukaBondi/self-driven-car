from rplidar import RPLidar
from math import floor
import numpy as np
import time

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)

dist_data = np.zeros(180, dtype='int16')
max_dist = 1000

try:
    print(lidar.get_info())
    print(lidar.get_health())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:

            # Floor the angle, set the limit to 359 then convert it pi radians
            angle = min([359, floor(angle)]) 
            

            if angle >= 90 and angle < 270: # Filtering out the unnecessary angles 
                continue

            if distance > max_dist: # Filtering out the unnecessary distances
                continue

            # Modifying the angle range to [-89, 90] (Integers only)
            if angle >= 270:
                angle = abs(angle - 360)
            elif angle < 90:
                angle *= -1
            
            # print(f'Angle: {angle}, Dist: {distance}, Y_dist: {y_dist:.2f}')

            # Fitting the angle range to the range [0, 180) (Integers only)
            dist_data[angle + 89] = floor(distance)

        print(f'{dist_data}\n\n\n\n\n') 

        # Resetting the distance values.
        dist_data = np.zeros(180, dtype='int16')

except KeyboardInterrupt:
    print('Stopping.')

lidar.stop()
lidar.disconnect()