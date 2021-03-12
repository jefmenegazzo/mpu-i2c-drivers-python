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
    address_mpu_slave=MPU9050_ADDRESS_68, 
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
# abias_slave = mpu.abias_slave # Get the slave accelerometer biases
# gbias = mpu.gbias # Get the master gyroscope biases
# gbias_slave = mpu.gbias_slave # Get the slave gyroscope biases
# magScale = mpu.magScale # Get magnetometer soft iron distortion
# mbias = mpu.mbias # Get magnetometer hard iron distortion
  
# print("|.....MPU9250 in 0x68 Biases.....|")
# print("Accelerometer Master", abias)
# print("Accelerometer Slave", abias_slave)
# print("Gyroscope Master", gbias)
# print("Gyroscope Slave", gbias_slave)
# print("Magnetometer SID", magScale)
# print("Magnetometer HID", mbias)
# print("\n")

##################################################
# Set Calibration                                #
##################################################
# mpu.abias = [0.073846435546875, 0.104925537109375, -0.007580566406250044]
# mpu.abias_slave = [-0.05669294084821429, -0.022966657366071428, 0.34601120721726186]
# mpu.gbias = [0.6832122802734375, -0.2918243408203125, -0.7152557373046875]
# mpu.gbias_slave = [-0.946044921875, -0.13242449079241073, -0.7113502139136905]
# mpu.magScale = [0.6847826086956522, 1.0327868852459017, 1.75]
# mpu.mbias = [8.19041514041514, 8.991651404151403, 14.696359890109889]

##################################################
# Show Values                                    #
##################################################
while True:
   
    print("|.....MPU9250 in 0x68 I2C Bus - Master.....|")
    print("Accelerometer", mpu.readAccelerometerMaster())
    print("Gyroscope", mpu.readGyroscopeMaster())
    print("Magnetometer", mpu.readMagnetometerMaster())
    print("Temperature", mpu.readTemperatureMaster())
    print("\n")

    print("|.....MPU9250 in 0x68 I2C Bus - Slave in 0x68 auxiliary sensor address.....|")
    print("Accelerometer", mpu.readAccelerometerSlave())
    print("Gyroscope", mpu.readGyroscopeSlave())
    print("Temperature", mpu.readTemperatureSlave())
    print("\n")

    time.sleep(1)
