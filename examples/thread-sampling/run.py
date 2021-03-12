#####################################################################
# Author: Jeferson Menegazzo                                        #
# Year: 2020                                                        #
# License: CC BY-NC-ND 4.0                                          #
#####################################################################

from sensors import Sensors

# Simple comand-line interface
def __init__():

    sensors = None # type: Sensors

    while True:

        print("""
        [1] Sensors - Create/Recreate
        [2] Sensors - Apply Configuration
        [3] Sensors - Reset Configuration
        [4] Sensors - Calibrate
        [5] Sampling - Start
        [6] Sampling - Stop
        [7] Sampling - View Current
        [0] Exit
        """)

        option = input("Choice: ")

        if option == "0":

            if not(sensors is None) and sensors.running:
                sensors.stop()

            print("Exiting")
            break

        elif option == "1":
            sensors = Sensors()
            print("Sensors created")

        elif sensors is None:
            print("Not created sensors")

        elif option == "2":
            sensors.configure()
            print("Configuration applied to sensors")

        elif option == "3":
            sensors.reset()
            print("Sensor configurations reseted")

        elif option == "4":
            sensors.calibrate()
            print("Calibrated sensors")

        elif option == "5":
            sensors.start()
            print("Sampling started")

        elif option == "6":
            sensors.stop()
            print("Sampling stoped")

        elif option == "7":
            sensors.showCurrent()

        else:
            print("Invalid Choice.")

if __name__ == "__main__":

    try:
        __init__()
    except KeyboardInterrupt:
        print("Exit")
