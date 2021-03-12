#####################################################################
# Author: Jeferson Menegazzo                                        #
# Year: 2020                                                        #
# License: CC BY-NC-ND 4.0                                          #
#####################################################################

import sys
sys.path.append("")

import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

##################################################
# Create                                         #
##################################################

mpu = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    address_mpu_slave=None, 
    bus=1, 
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

##################################################
# Configure                                      #
##################################################
mpu.configure() # Apply the settings to the registers.

##################################################
# Calibrate                                      #
##################################################
# mpu.calibrate() # Calibrate sensors
# mpu.configure() # The calibration function resets the sensors, so you need to reconfigure them

##################################################
# Get Calibration                                #
##################################################
# abias = mpu.abias # Get the master accelerometer biases
# gbias = mpu.gbias # Get the master gyroscope biases
# magScale = mpu.magScale # Get magnetometer soft iron distortion
# mbias = mpu.mbias # Get magnetometer hard iron distortion

# print("|.....MPU9250 in 0x68 Biases.....|")
# print("Accelerometer", abias)
# print("Gyroscope", gbias)
# print("Magnetometer SID", magScale)
# print("Magnetometer HID", mbias)
# print("\n")

##################################################
# Set Calibration                                #
##################################################
# mpu.abias = [-0.08004239710365854, 0.458740234375, 0.2116996951219512]
# mpu.gbias = [0.8958025676448171, 0.45292551924542684, 0.866773651867378]
# mpu.magScale = [1.0104166666666667, 0.9797979797979799, 1.0104166666666667]
# mpu.mbias = [2.6989010989010986, 2.7832417582417586, 2.6989010989010986]

##################################################
# Show Values                                    #
##################################################
while True:
   
    print("|.....MPU9250 in 0x68 Address.....|")
    print("Accelerometer", mpu.readAccelerometerMaster())
    print("Gyroscope", mpu.readGyroscopeMaster())
    print("Magnetometer", mpu.readMagnetometerMaster())
    print("Temperature", mpu.readTemperatureMaster())
    print("\n")

    time.sleep(1)
