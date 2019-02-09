from sensors import Sensors
import time, sys, csv, os

try:

    sleep = 0.01 # 100 Hz
    # sleep = 0.5

    if not os.path.exists("data"):
        os.makedirs("data")

    sensors = Sensors()  

    fileName = input("Nome do arquivo CSV: ")
    fileName = "data/" + fileName + ".csv"

    with open(fileName, "w+") as csvfile:
        
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        row = sensors.getCSVLabel()
        spamwriter.writerow(row)

        while True:
            row = sensors.getCSVData()
            spamwriter.writerow(row)
            time.sleep(sleep)

except KeyboardInterrupt:
    print("Quit")
    sys.exit()
