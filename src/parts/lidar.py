from adafruit_rplidar import RPLidar, RPLidarException
from math import floor
import numpy as np
import serial
import glob
import time

class lidar(object):
    def __init__(self, maxDist=1500) -> None:

        # Find the serial port where the lidar is connected
        port_found = False
        temp_list = glob.glob('/dev/ttyUSB*')
        result = []
        for port in temp_list:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
                port_found = True
            except serial.SerialException:
                pass
        if not port_found:
            raise RuntimeError("No RPLidar is connected.")

        self.port = result[0]
        self.lidar = RPLidar(None, self.port, timeout=3)
        self.lidar.clear_input()
        time.sleep(1)

        self.running = True
        self.dist_data = np.array([120]*210, dtype='int16')
        self.max_dist = maxDist # Default max distance


    def update(self):
        try:
            for scan in self.lidar.iter_scans():
                
                if not self.running:
                    break

                data_buffer = np.array([120]*210, dtype='int16')
                for (_, angle, distance) in scan:
                    # Floor the angle, set the limit to 359 then convert it pi radians
                    angle = min([359, floor(angle)]) 
                    

                    if angle < 75 or angle >= 285: # Filtering out the unnecessary angles 
                        continue

                    if distance > self.max_dist: # Filtering out the unnecessary distances
                        continue
                    
                    # print(f'Angle: {angle}, Dist: {distance}')

                    # Fitting the angle range to the range [0, 180) (Integers only)
                    data_buffer[angle - 75] = floor(distance)

                self.dist_data = data_buffer
                #self.lidar.clear_input()

        except RPLidarException as error:
            print(f"Error: {error}")
            self.lidar.stop_motor()
            self.dist_data = np.array([120]*210, dtype='int16')


    # Returns distance data -> angle range: [75, 285]
    def read(self):
        return self.dist_data

    def shutdown(self):
        self.running = False
        time.sleep(1)
        if self.lidar is not None:
            self.lidar.stop()
            self.lidar.stop_motor()
            self.lidar.disconnect()
            self.lidar = None


