import time
from sampling import Sampling
from registers import AK8963_ADDRESS, MPU9050_ADDRESS_68, MPU9050_ADDRESS_69, GFS_1000, AFS_8G, AK8963_BIT_16, AK8963_MODE_C8HZ

class Sensors:

    mpu_0x68 = None
    mpu_0x69 = None

    def __init__(self,):
        self.mpu_0x68 = Sampling(AK8963_ADDRESS, MPU9050_ADDRESS_68, MPU9050_ADDRESS_68, 1)
        self.mpu_0x69 = Sampling(AK8963_ADDRESS, MPU9050_ADDRESS_69, None, 1)
        self.mpu_0x68.configure(GFS_1000, AFS_8G, AK8963_BIT_16, AK8963_MODE_C8HZ)
        self.mpu_0x69.configure(GFS_1000, AFS_8G, AK8963_BIT_16, AK8963_MODE_C8HZ)    
        
    def reset(self):
        self.mpu_0x68.reset()
        self.mpu_0x69.reset()

    def start(self):
        timeSync = time.time()
        self.mpu_0x68.startSampling(timeSync)
        self.mpu_0x69.startSampling(timeSync)

    def stop(self):
        self.mpu_0x68.stopSampling()
        self.mpu_0x69.stopSampling()

    def showCurrent(self):

        data_0x69 = self.mpu_0x69.mpu.getAllData()
        data_0x68 = self.mpu_0x68.mpu.getAllData()
        
        print(
            "--------------------------------------------------------------------------------", "\n",
            "Time: ", time.time(), "\n",
            "--------------------------------------------------------------------------------", "\n",
            "MPU = ", self.formatLabel("0x69_master"), " | ", self.formatLabel("0x68_master"), " | ", self.formatLabel("0x68_slave_of_0x68"), "\n",
            "--------------------------------------------------------------------------------", "\n",
            "A_X = ", self.formatValue(data_0x69[1]),  " | ", self.formatValue(data_0x68[1]),  " | ", self.formatValue(data_0x68[7]),  "\n",
            "A_Y = ", self.formatValue(data_0x69[2]),  " | ", self.formatValue(data_0x68[2]),  " | ", self.formatValue(data_0x68[8]),  "\n",
            "A_Z = ", self.formatValue(data_0x69[3]),  " | ", self.formatValue(data_0x68[3]),  " | ", self.formatValue(data_0x68[9]),  "\n",
            "--------------------------------------------------------------------------------", "\n",
            "G_X = ", self.formatValue(data_0x69[4]), " | ", self.formatValue(data_0x68[4]), " | ", self.formatValue(data_0x68[10]), "\n",
            "G_Y = ", self.formatValue(data_0x69[5]), " | ", self.formatValue(data_0x68[5]), " | ", self.formatValue(data_0x68[11]), "\n",
            "G_Z = ", self.formatValue(data_0x69[6]), " | ", self.formatValue(data_0x68[6]), " | ", self.formatValue(data_0x68[12]), "\n",
            "--------------------------------------------------------------------------------", "\n",
            "M_X = ", self.formatValue(data_0x69[13]), " | ", self.formatValue(data_0x68[13]), " | ", "", "\n",
            "M_Y = ", self.formatValue(data_0x69[14]), " | ", self.formatValue(data_0x68[14]), " | ", "", "\n",
            "M_Z = ", self.formatValue(data_0x69[15]), " | ", self.formatValue(data_0x68[15]), " | ", "", "\n",
            "--------------------------------------------------------------------------------", "\n",
        )

    def formatValue(self, value):
        format = "{: 4.17f}"
        return format.format(value)

    def formatLabel(self, value):
        return value.center(20)