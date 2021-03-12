#####################################################################
# Author: Jeferson Menegazzo                                        #
# Year: 2020                                                        #
# License: CC BY-NC-ND 4.0                                          #
#####################################################################

import csv
import datetime
import os
import sys
import time
from threading import Thread
import sys
sys.path.append("")

from mpu9250_jmdev.mpu_9250 import MPU9250

class Sampling(Thread):

    mpu = None
    folder = "../data"
    file = None
    running = False
    sleepStart = 5 # In seconds
    # sampling_rate = 0.01 # 100 Hz

    def __init__(self, address_ak, address_mpu_master, address_mpu_slave, bus, gfs, afs, mfs, mode):
        Thread.__init__(self)
        self.mpu = MPU9250(address_ak, address_mpu_master, address_mpu_slave, bus, gfs, afs, mfs, mode)
    
    def configure(self):
        self.mpu.configure()

    def reset(self):
        self.mpu.reset()

    def calibrate(self):
        self.mpu.calibrate()

    def getAllData(self):
        return self.mpu.getAllData()

    def getAllDataLabels(self):
        return self.mpu.getAllDataLabels()

    def getAllSettings(self):
        return self.mpu.getAllSettings()

    def getAllSettingsLabels(self):
        return self.mpu.getAllSettingsLabels()

    def startSampling(self, timeSync):

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        fileSuffix = str(hex(self.mpu.address_mpu_master)) + " " + datetime.datetime.fromtimestamp(timeSync).strftime('%d-%m-%Y %H-%M-%S') + ".csv"
        self.file = self.folder + "/data-set-mpu-" + fileSuffix
        settings = self.folder + "/settings-mpu-" + fileSuffix
        
        with open(settings, "w+") as csvfile:
            spamwriter = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(self.getAllSettingsLabels())
            spamwriter.writerow(self.getAllSettings())
        
        self.timeSync = timeSync
        self.running = True
        self.start()

    def stopSampling(self):
        self.running = False
        self.join()

    def run(self):

        with open(self.file, "w+") as csvfile:
            
            spamwriter = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)

            # Writing Labels
            row = self.getAllDataLabels()
            spamwriter.writerow(row)

            # Start threads at same time
            sleepTime = self.sleepStart + (self.timeSync - int(self.timeSync))
            time.sleep(sleepTime)

            # lastTime = time.time()

            while self.running:

                row = self.getAllData()
                spamwriter.writerow(row)
                
                # sleepTime = self.sampling_rate - (row[0] - lastTime)
                
                # if(sleepTime > 0):
                #     time.sleep(sleepTime)

                # lastTime = row[0]
