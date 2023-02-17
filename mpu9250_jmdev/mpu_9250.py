#####################################################################
# Author: Jeferson Menegazzo                                        #
# Year: 2021                                                        #
# License: CC BY-NC-ND 4.0                                          #
#####################################################################

"""
Based on:
https://github.com/nickcoutsos/MPU-6050-Python/blob/master/MPU6050.py
https://github.com/Tijndagamer/mpu6050/blob/master/mpu6050/mpu6050.py
https://github.com/FaBoPlatform/FaBo9AXIS-MPU9250-Python/blob/master/FaBo9Axis_MPU9250/MPU9250.py
https://github.com/kriswiner/MPU6050/blob/master/MPU6050IMU.ino
https://github.com/kriswiner/MPU6050/wiki/Simple-and-Effective-Magnetometer-Calibration
https://github.com/kriswiner/MPU9250/blob/master/MPU9250_MS5637_AHRS_t3.ino
"""

class MPU9250:

    def __init__(self, smbus_lib="smbus"):

        global smbus

        if smbus_lib == "smbus":
            import smbus
        elif smbus_lib == "smbus2":
            import smbus2 as smbus
        elif smbus_lib == "smbus_fake":
            from mpu9250_jmdev.smbus_fake import FakeSmbus as smbus
        else:
            raise Exception(smbus_lib + " is not a valid choice for the 'smbus_lib' parameter")

    def print(self):
        print(smbus)
