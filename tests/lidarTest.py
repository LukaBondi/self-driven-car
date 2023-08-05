from rplidar import RPLidar
from math import floor
import numpy as np
import time

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(PORT_NAME)

dist_data = np.zeros(210, dtype='int16')
max_dist = 1500

try:
    print(lidar.get_info())
    print(lidar.get_health())
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:

            # Floor the angle, set the limit to 359 then convert it pi radians
            angle = min([359, floor(angle)]) 
            

            if angle < 75 or angle >= 285: # Filtering out the unnecessary angles 
                continue

            if distance > max_dist: # Filtering out the unnecessary distances
                continue
            
            # print(f'Angle: {angle}, Dist: {distance}')

            # Fitting the angle range to the range [0, 180) (Integers only)
            dist_data[angle - 75] = floor(distance)

        print(f'{dist_data}\n\n\n\n\n') 

        # Resetting the distance values.
        dist_data = np.zeros(210, dtype='int16')

except KeyboardInterrupt:
    print('Stopping.')
    
except IndexError:
    print(angle)

lidar.stop()
lidar.disconnect()
