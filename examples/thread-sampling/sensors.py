#####################################################################
# Author: Jeferson Menegazzo                                        #
# Year: 2020                                                        #
# License: CC BY-NC-ND 4.0                                          #
#####################################################################

import time
import sys
sys.path.append("")

from sampling import Sampling
from mpu9250_jmdev.registers import *

# Class that handles the entire sensor network.
class Sensors:

    sampling_mpu_0x68 = None
    sampling_mpu_0x69 = None

    running = False

    def __init__(self,):
        self.sampling_mpu_0x68 = Sampling(AK8963_ADDRESS, MPU9050_ADDRESS_68, MPU9050_ADDRESS_68, 1, GFS_1000, AFS_8G, AK8963_BIT_16, AK8963_MODE_C100HZ)
        self.sampling_mpu_0x69 = Sampling(AK8963_ADDRESS, MPU9050_ADDRESS_69, None, 1, GFS_1000, AFS_8G, AK8963_BIT_16, AK8963_MODE_C100HZ)
        # self.calibrate()
        
    def configure(self):
        self.sampling_mpu_0x68.configure()
        self.sampling_mpu_0x69.configure()    

    def reset(self):
        self.sampling_mpu_0x68.reset()
        self.sampling_mpu_0x69.reset()
        # self.configure()

    def calibrate(self):
        self.sampling_mpu_0x68.calibrate()
        self.sampling_mpu_0x69.calibrate()
        # self.configure()
 
    def start(self):
        timeSync = time.time()
        self.sampling_mpu_0x68.startSampling(timeSync)
        self.sampling_mpu_0x69.startSampling(timeSync)
        self.running = True

    def stop(self):

        if self.running:
            self.sampling_mpu_0x68.stopSampling()
            self.sampling_mpu_0x69.stopSampling()
            self.running = False

    def showCurrent(self):
        
        def formatValue(array, index):

            format = "{: 4.17f}"

            if len(array) > index:
                return format.format(array[index])
            else:
                "        null        "

        def formatLabel(value):
            return value.center(20)

        data_0x68 = self.sampling_mpu_0x68.getAllData()
        data_0x69 = self.sampling_mpu_0x69.getAllData()
        
        print(
            "----------------------------------------------------------------------------------------------------------", "\n",
            "Time: ", time.time(), "\n",
            "----------------------------------------------------------------------------------------------------------", "\n",
            "MPU = ", formatLabel("0x68_master"), " | ", formatLabel("0x68_slave_of_0x68"), " | ",  formatLabel("0x69_master"), " | ", formatLabel("0x68_slave_of_0x69"), "\n",
            "----------------------------------------------------------------------------------------------------------", "\n",
            "A_X = ", formatValue(data_0x68, 1),  " | ", formatValue(data_0x68, 7),  " | ",         formatValue(data_0x69, 1), " | ",  formatValue(data_0x69, 7), "\n",
            "A_Y = ", formatValue(data_0x68, 2),  " | ", formatValue(data_0x68, 8),  " | ",         formatValue(data_0x69, 2), " | ",  formatValue(data_0x69, 8), "\n",
            "A_Z = ", formatValue(data_0x68, 3),  " | ", formatValue(data_0x68, 9),  " | ",         formatValue(data_0x69, 3), " | ",  formatValue(data_0x69, 9), "\n",
            "----------------------------------------------------------------------------------------------------------", "\n",
            "G_X = ", formatValue(data_0x68, 4), " | ", formatValue(data_0x68, 10), " | ",          formatValue(data_0x69, 4), " | ",  formatValue(data_0x69, 10), "\n",
            "G_Y = ", formatValue(data_0x68, 5), " | ", formatValue(data_0x68, 11), " | ",          formatValue(data_0x69, 5), " | ",  formatValue(data_0x69, 11), "\n",
            "G_Z = ", formatValue(data_0x68, 6), " | ", formatValue(data_0x68, 12), " | ",          formatValue(data_0x69, 6), " | ",  formatValue(data_0x69, 12), "\n",
            "----------------------------------------------------------------------------------------------------------", "\n",
            "M_X = ", formatValue(data_0x68, 13), " | ", "        null        ", " | " ,            formatValue(data_0x69, 13), " | ",  "        null        ", "\n",
            "M_Y = ", formatValue(data_0x68, 14), " | ", "        null        ", " | " ,            formatValue(data_0x69, 14), " | ",  "        null        ", "\n",
            "M_Z = ", formatValue(data_0x68, 15), " | ", "        null        ", " | " ,            formatValue(data_0x69, 15), " | ",  "        null        ", "\n",
            "----------------------------------------------------------------------------------------------------------", "\n",
        )
