from registers import AK8963_ADDRESS, MPU9050_ADDRESS_68, MPU9050_ADDRESS_69, GFS_1000, AFS_8G, AK8963_BIT_16, AK8963_MODE_C8HZ
from mpu_9250 import MPU9250
import time

class Sensors:

    mpu_0x68 = None
    mpu_0x69 = None

    def __init__(self):

        self.mpu_0x68 = MPU9250(AK8963_ADDRESS, MPU9050_ADDRESS_68, MPU9050_ADDRESS_68, 1)
        self.mpu_0x69 = MPU9250(AK8963_ADDRESS, MPU9050_ADDRESS_69, None, 1)

        self.mpu_0x68.configure(GFS_1000, AFS_8G, AK8963_BIT_16, AK8963_MODE_C8HZ)
        self.mpu_0x69.configure(GFS_1000, AFS_8G, AK8963_BIT_16, AK8963_MODE_C8HZ)

    def getSensorsNames(self):

        return [
            hex(self.mpu_0x68.address_mpu_master),
            hex(self.mpu_0x68.address_mpu_slave) + "_AUX_" + hex(self.mpu_0x68.address_mpu_master),
            hex(self.mpu_0x69.address_mpu_master),
            hex(self.mpu_0x69.address_mpu_slave) + "_AUX_" + hex(self.mpu_0x69.address_mpu_master),
        ]

    def getAllData(self):

        return { 
            "timestamp": time.time(),
            "accelerometer": [
                self.retryReturn(self.mpu_0x68.readAccelerometerMaster),
                self.retryReturn(self.mpu_0x68.readAccelerometerSlave),
                self.retryReturn(self.mpu_0x69.readAccelerometerMaster),
                self.retryReturn(self.mpu_0x69.readAccelerometerSlave),
            ], 
            "gyroscope": [
                self.retryReturn(self.mpu_0x68.readGyroscopeMaster),
                self.retryReturn(self.mpu_0x68.readGyroscopeSlave),
                self.retryReturn(self.mpu_0x69.readGyroscopeMaster),
                self.retryReturn(self.mpu_0x69.readGyroscopeSlave),
            ], 
            "magnetometer": [
                self.retryReturn(self.mpu_0x68.readMagnetometerMaster),
                self.retryReturn(self.mpu_0x68.readMagnetometerSlave),
                self.retryReturn(self.mpu_0x69.readMagnetometerMaster),
                self.retryReturn(self.mpu_0x69.readMagnetometerSlave),
            ],
            "temperature": [
                self.retryReturn(self.mpu_0x68.readTemperatureMaster),
                self.retryReturn(self.mpu_0x68.readTemperatureSlave),
                self.retryReturn(self.mpu_0x69.readTemperatureMaster),
                self.retryReturn(self.mpu_0x69.readTemperatureSlave),
            ] 
        }

    def getCSVLabel(self):

        sensors = ["ACC", "GYRO", "MAG"]
        axes = ["X", "Y", "Z"]


        mpu = self.getSensorsNames()

        labels = [
            "timestamp",

            # ACC
            "ACC_X_" + mpu[0],
            "ACC_Y_" + mpu[0],
            "ACC_Z_" + mpu[0],

            "ACC_X_" + mpu[1],
            "ACC_Y_" + mpu[1],
            "ACC_Z_" + mpu[1],

            "ACC_X_" + mpu[2],
            "ACC_Y_" + mpu[2],
            "ACC_Z_" + mpu[2],

            "ACC_X_" + mpu[3],
            "ACC_Y_" + mpu[3],
            "ACC_Z_" + mpu[3],

            # GYRO
            "GYRO_X_" + mpu[0],
            "GYRO_Y_" + mpu[0],
            "GYRO_Z_" + mpu[0],

            "GYRO_X_" + mpu[1],
            "GYRO_Y_" + mpu[1],
            "GYRO_Z_" + mpu[1],

            "GYRO_X_" + mpu[2],
            "GYRO_Y_" + mpu[2],
            "GYRO_Z_" + mpu[2],

            "GYRO_X_" + mpu[3],
            "GYRO_Y_" + mpu[3],
            "GYRO_Z_" + mpu[3],

            # MAG
            "MAG_X_" + mpu[0],
            "MAG_Y_" + mpu[0],
            "MAG_Z_" + mpu[0],

            "MAG_X_" + mpu[1],
            "MAG_Y_" + mpu[1],
            "MAG_Z_" + mpu[1],

            "MAG_X_" + mpu[2],
            "MAG_Y_" + mpu[2],
            "MAG_Z_" + mpu[2],

            "MAG_X_" + mpu[3],
            "MAG_Y_" + mpu[3],
            "MAG_Z_" + mpu[3],

            # TEMP

            "TEMP_" + mpu[0],
            "TEMP_" + mpu[1],
            "TEMP_" + mpu[2],
            "TEMP_" + mpu[3],
        ]

        return labels
    
    def getCSVData(self):

        data = self.getAllData()

        return [
            data['timestamp'],

            # ACC
            data['accelerometer'][0]['x'],
            data['accelerometer'][0]['y'],
            data['accelerometer'][0]['z'],

            data['accelerometer'][1]['x'],
            data['accelerometer'][1]['y'],
            data['accelerometer'][1]['z'],

            data['accelerometer'][2]['x'],
            data['accelerometer'][2]['y'],
            data['accelerometer'][2]['z'],

            data['accelerometer'][3]['x'],
            data['accelerometer'][3]['y'],
            data['accelerometer'][3]['z'],

            # GYRO
            data['gyroscope'][0]['x'],
            data['gyroscope'][0]['y'],
            data['gyroscope'][0]['z'],

            data['gyroscope'][1]['x'],
            data['gyroscope'][1]['y'],
            data['gyroscope'][1]['z'],

            data['gyroscope'][2]['x'],
            data['gyroscope'][2]['y'],
            data['gyroscope'][2]['z'],

            data['gyroscope'][3]['x'],
            data['gyroscope'][3]['y'],
            data['gyroscope'][3]['z'],

            # MAG
            data['magnetometer'][0]['x'],
            data['magnetometer'][0]['y'],
            data['magnetometer'][0]['z'],

            data['magnetometer'][1]['x'],
            data['magnetometer'][1]['y'],
            data['magnetometer'][1]['z'],

            data['magnetometer'][2]['x'],
            data['magnetometer'][2]['y'],
            data['magnetometer'][2]['z'],

            data['magnetometer'][3]['x'],
            data['magnetometer'][3]['y'],
            data['magnetometer'][3]['z'],

            # TEMP
            data['temperature'][0],
            data['temperature'][1],
            data['temperature'][2],
            data['temperature'][3],
        ]

    def printData(self, row):

        format = "{: 4.17f}"
        mpu = self.getSensorsNames()
        
        print(
            "---------------------------------------------------------------------------------------------------------", "\n",
            "Time: ", row[0], "\n",
            "---------------------------------------------------------------------------------------------------------", "\n",
            "MPU = ", (mpu[0]).center(20), " | ", (mpu[1]).center(20), " | ", (mpu[2]).center(20), " | ", (mpu[3]).center(20), "\n",
            "---------------------------------------------------------------------------------------------------------", "\n",
            "A_X = ", format.format(row[1]), " | ", format.format(row[4]), " | ", format.format(row[7]), " | ", format.format(row[10]), "\n",
            "A_Y = ", format.format(row[2]), " | ", format.format(row[5]), " | ", format.format(row[8]), " | ", format.format(row[11]), "\n",
            "A_Z = ", format.format(row[3]), " | ", format.format(row[6]), " | ", format.format(row[9]), " | ", format.format(row[12]), "\n",
            "---------------------------------------------------------------------------------------------------------", "\n",
            "G_X = ", format.format(row[13]), " | ", format.format(row[16]), " | ", format.format(row[19]), " | ", format.format(row[22]), "\n",
            "G_Y = ", format.format(row[14]), " | ", format.format(row[17]), " | ", format.format(row[20]), " | ", format.format(row[23]), "\n",
            "G_Z = ", format.format(row[15]), " | ", format.format(row[18]), " | ", format.format(row[21]), " | ", format.format(row[24]), "\n",
            "---------------------------------------------------------------------------------------------------------", "\n",
            "M_X = ", format.format(row[25]), " | ", format.format(row[28]), " | ", format.format(row[31]), " | ", format.format(row[34]), "\n",
            "M_Y = ", format.format(row[26]), " | ", format.format(row[29]), " | ", format.format(row[32]), " | ", format.format(row[35]), "\n",
            "M_Z = ", format.format(row[27]), " | ", format.format(row[30]), " | ", format.format(row[33]), " | ", format.format(row[36]), "\n",
            "---------------------------------------------------------------------------------------------------------", "\n",
            "T = ", format.format(row[37]), " | ", format.format(row[38]), " | ", format.format(row[39]), " | ", format.format(row[40]), "\n",
            "---------------------------------------------------------------------------------------------------------", "\n",
        )

    def retryReturn(self, function, retry=1):

        try:
            return function()
        
        except OSError:

            if(retry <= 3): 
                return self.retryReturn(function, retry + 1)
            
            else:
                return self.getDataError() 