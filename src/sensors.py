from registers import AK8963_ADDRESS, MPU9050_ADDRESS_68, MPU9050_ADDRESS_69, GFS_1000, AFS_8G, AK8963_BIT_16, AK8963_MODE_C8HZ
from mpu_9250 import MPU9250
import time

class Sensors:

    mpu_0x68 = None
    mpu_0x69 = None

    def __init__(self):
        self.mpu_0x68 = MPU9250(AK8963_ADDRESS, MPU9050_ADDRESS_68, MPU9050_ADDRESS_68, 1)
        self.mpu_0x69 = MPU9250(AK8963_ADDRESS, MPU9050_ADDRESS_69, None, 1)
        self.configure()
        
    def configure(self):
        self.mpu_0x68.configure(GFS_1000, AFS_8G, AK8963_BIT_16, AK8963_MODE_C8HZ)
        self.mpu_0x69.configure(GFS_1000, AFS_8G, AK8963_BIT_16, AK8963_MODE_C8HZ)

    def reset(self):
        self.mpu_0x68.reset()
        self.mpu_0x69.reset()

    def getSensorAddress(self):

        return [
            "0x69_master",
            "0x68_master",
            "0x68_slave_of_0x68"
        ]

    def SensorTypes(self):

        return [
            "timestamp",
            "acc",
            "gyro",
            "mag"
        ]

    def getAllData(self):

        sensorTypes = self.SensorTypes()
        sensorAddress = self.getSensorAddress()
        
        return { 
            sensorTypes[0]: time.time(),
            sensorTypes[1]: {
                sensorAddress[0]: self.retryReturn(self.mpu_0x69.readAccelerometerMaster),
                sensorAddress[1]: self.retryReturn(self.mpu_0x68.readAccelerometerMaster),
                sensorAddress[2]: self.retryReturn(self.mpu_0x68.readAccelerometerSlave)
            },
            sensorTypes[2]: {
                sensorAddress[0]: self.retryReturn(self.mpu_0x69.readGyroscopeMaster),
                sensorAddress[1]: self.retryReturn(self.mpu_0x68.readGyroscopeMaster),
                sensorAddress[2]: self.retryReturn(self.mpu_0x68.readGyroscopeSlave)
            }, 
            sensorTypes[3]: {
                sensorAddress[0]: self.retryReturn(self.mpu_0x69.readMagnetometerMaster),
                sensorAddress[1]: self.retryReturn(self.mpu_0x68.readMagnetometerMaster),
                sensorAddress[2]: self.retryReturn(self.mpu_0x68.readMagnetometerSlave)
            }
        }

    def getCSVLabel(self):

        labels = []
        dataAxes = ["x", "y", "z"]
        sensorTypes = self.SensorTypes()
        sensorAddress = self.getSensorAddress()

        labels.append(sensorTypes[0])
        sensorTypes.pop(0)

        for types in sensorTypes:
            for address in sensorAddress:
                for axis in dataAxes:
                    labels.append(types + "_" + axis + "_" + address)
        
        return labels
    
    def getCSVData(self):

        data = []
        rawData = self.getAllData()
        dataAxes = ["x", "y", "z"]
        sensorTypes = self.SensorTypes()
        sensorAddress = self.getSensorAddress()

        data.append(rawData[sensorTypes[0]])
        sensorTypes.pop(0)

        for types in sensorTypes:
            for address in sensorAddress:
                for axis in dataAxes:
                    data.append(rawData[types][address][axis])

        return data

    def printData(self, csvData):

        sensorAddress = self.getSensorAddress()

        print(
            "--------------------------------------------------------------------------------", "\n",
            "Time: ", csvData[0], "\n",
            "--------------------------------------------------------------------------------", "\n",
            "MPU = ", self.formatLabel(sensorAddress[0]), " | ", self.formatLabel(sensorAddress[1]), " | ", self.formatLabel(sensorAddress[2]), "\n",
            "--------------------------------------------------------------------------------", "\n",
            "A_X = ", self.formatValue(csvData[1]),  " | ", self.formatValue(csvData[4]),  " | ", self.formatValue(csvData[7]),  "\n",
            "A_Y = ", self.formatValue(csvData[2]),  " | ", self.formatValue(csvData[5]),  " | ", self.formatValue(csvData[8]),  "\n",
            "A_Z = ", self.formatValue(csvData[3]),  " | ", self.formatValue(csvData[6]),  " | ", self.formatValue(csvData[9]),  "\n",
            "--------------------------------------------------------------------------------", "\n",
            "G_X = ", self.formatValue(csvData[10]), " | ", self.formatValue(csvData[13]), " | ", self.formatValue(csvData[16]), "\n",
            "G_Y = ", self.formatValue(csvData[11]), " | ", self.formatValue(csvData[14]), " | ", self.formatValue(csvData[17]), "\n",
            "G_Z = ", self.formatValue(csvData[12]), " | ", self.formatValue(csvData[15]), " | ", self.formatValue(csvData[18]), "\n",
            "--------------------------------------------------------------------------------", "\n",
            "M_X = ", self.formatValue(csvData[19]), " | ", self.formatValue(csvData[22]), " | ", self.formatValue(csvData[25]), "\n",
            "M_Y = ", self.formatValue(csvData[20]), " | ", self.formatValue(csvData[23]), " | ", self.formatValue(csvData[26]), "\n",
            "M_Z = ", self.formatValue(csvData[21]), " | ", self.formatValue(csvData[24]), " | ", self.formatValue(csvData[27]), "\n",
            "--------------------------------------------------------------------------------", "\n",
        )
    
    def formatValue(self, value):
        format = "{: 4.17f}"
        return format.format(value)

    def formatLabel(self, value):
        return value.center(20)

    def retryReturn(self, function, retry=1):

        try:
            return function()
        
        except OSError:

            if(retry <= 3): 
                return self.retryReturn(function, retry + 1)
            
            else:
                return self.getDataError() 