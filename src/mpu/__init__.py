from sensors import Sensors
import datetime, time, sys, os, csv

## SETTINGS
CONSOLE = True
PRODUCTION = False

# DEFAULT
SAMPLING_RATE = 0.01 if PRODUCTION else 0.5 # 100 Hz or 2 Hz
FOLDER = "../../data"
FILE = FOLDER + "/data-set " + datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H-%M-%S') + ".csv"

def showSettings():
    print("Sensor Data Collect")
    print("Mode: " + ("production" if PRODUCTION else "dev"))
    print("Sampling Rate: " + str(SAMPLING_RATE))
    print("Console Enabled: " + str(CONSOLE))
    print("Data Folder: " + FOLDER)
    print("File: " + FILE)
    print("")

def showInit():
    print("\nInit")
    showSettings()

def showQuit():
    print("\nQuit")
    showSettings()

try:

    showInit()

    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)

    sensors = Sensors()  

    with open(FILE, "w+") as csvfile:
        
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        row = sensors.getCSVLabel()
        spamwriter.writerow(row)

        while True:
            
            row = sensors.getCSVData()
            spamwriter.writerow(row)

            if CONSOLE:
                sensors.printData(row)

            time.sleep(SAMPLING_RATE)

except KeyboardInterrupt:
    showQuit()
    sys.exit()
