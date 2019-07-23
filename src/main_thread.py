import csv
import datetime
import os
import sys
import time
from threading import Thread
from sensors import Sensors

class MainThread(Thread):

    running = None
    console = None
    production = None

    sampling_rate = None
    folder = None
    file = None

    sensors = None

    def __init__(self, production=True):
        Thread.__init__(self)
        self.running = False
        self.console = not(production)
        self.production = production

    def run(self):
           
        with open(self.file, "w+") as csvfile:
            
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            row = self.sensors.getCSVLabel()
            spamwriter.writerow(row)

            while self.running:
                
                row = self.sensors.getCSVData()
                spamwriter.writerow(row)

                if self.console:
                    self.sensors.printData(row)

                time.sleep(self.sampling_rate)

    def startSensors(self):

        self.sampling_rate = 0.01 if self.production else 0.5 # 100 Hz or 2 Hz
        self.folder = "../../data"
        self.file = self.folder + "/mpu-data-set " + datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H-%M-%S') + ".csv"

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        self.sensors = Sensors()  

    def resetSensors(self):

        if self.sensors:
            self.sensors.reset()

    def startSampling(self):
        self.running = True
        self.start()

    def stopSampling(self):
        self.running = False
        self.join()

    def showSamplingSettings(self):
        print("Mode: " + ("production" if self.production else "development"))
        print("Sampling Rate: " + str(self.sampling_rate))
        print("Console Enabled: " + str(self.console))
        print("Data Folder: " + self.folder)
        print("File: " + self.file)
        print("")

    def showSamplingCurrent(self):
        data = self.sensors.getCSVData()
        self.sensors.printData(data)