"""
https://github.com/nickcoutsos/MPU-6050-Python/blob/master/MPU6050.py
https://github.com/Tijndagamer/mpu6050/blob/master/mpu6050/mpu6050.py
https://github.com/FaBoPlatform/FaBo9AXIS-MPU9250-Python/blob/master/FaBo9Axis_MPU9250/MPU9250.py
https://github.com/kriswiner/MPU9250
"""

import smbus, time
from registers import *

class MPU9250:

    # Settings
    address_ak = None
    address_mpu_master = None
    address_mpu_slave = None
    bus = None

    # Sensor Resolution - Scale Factor
    gres = None # Gyroscope
    ares = None # Accelerometer
    mres = None # Magnetometer

    # Magnometer Sensitivity
    magXcoef = None
    magYcoef = None
    magZcoef = None

    # Master and Slave Biases
    gbias = [0,0,0]
    gbias_slave = [0,0,0]
    abias = [0,0,0]
    abias_slave = [0,0,0]

    # Constructor
    # @param [in] self - The object pointer.
    # @param [in] address_mpu_master - MPU-9250 I2C address.
    # @param [in] address_ak - AK8963 I2C slave address.
    # @param [in] address_mpu_slave - MPU-9250 I2C slave address.
    # @param [in] bus - I2C bus board (default:Board Revision 2[1]).
    def __init__(self, address_ak, address_mpu_master, address_mpu_slave, bus):
        self.address_ak = address_ak
        self.address_mpu_master = address_mpu_master
        self.address_mpu_slave = address_mpu_slave
        self.bus = smbus.SMBus(bus)
       
    # Configure MPU
    # @param [in] self - The object pointer.
    # @param [in] gfs - Gyroscope full scale select (default:GFS_250[+250dps]).
    # @param [in] afs - Accelerometer full scale select (default:AFS_2G[2g]).
    # @param [in] mfs - Magnetometer scale select (default:AK8963_BIT_16[16bit])
    # @param [in] mode - Magnetometer mode select (default:AK8963_MODE_C8HZ[Continous 8Hz])
    def configure(self, gfs=GFS_250, afs=AFS_2G, mfs=AK8963_BIT_16, mode=AK8963_MODE_C8HZ, retry=1):
    
        try:
            self.calibrateMPU6050()
            self.configureMPU6050(gfs, afs)
            self.configureAK8963(mfs, mode)
        
        except OSError as err:

            if(retry <= 3):
                self.configure(gfs, afs, mfs, mode, retry + 1)

            else:
                raise err

    # Configure MPU-9250
    # @param [in] self - The object pointer.
    # @param [in] gfs - Gyroscope full scale select.
    # @param [in] afs - Accelerometer full scale select.
    def configureMPU6050(self, gfs, afs):

        if gfs == GFS_250:
            self.gres = GYRO_SCALE_MODIFIER_250DEG_DIV
        elif gfs == GFS_500:
            self.gres = GYRO_SCALE_MODIFIER_500DEG_DIV
        elif gfs == GFS_1000:
            self.gres = GYRO_SCALE_MODIFIER_1000DEG_DIV
        elif gfs == GFS_2000:
            self.gres = GYRO_SCALE_MODIFIER_2000DEG_DIV
        else:
            raise Exception('Gyroscope scale modifier not found.')

        if afs == AFS_2G:
            self.ares = ACCEL_SCALE_MODIFIER_2G_DIV
        elif afs == AFS_4G:
            self.ares = ACCEL_SCALE_MODIFIER_4G_DIV
        elif afs == AFS_8G:
            self.ares = ACCEL_SCALE_MODIFIER_8G_DIV
        elif afs == AFS_16G:
            self.ares = ACCEL_SCALE_MODIFIER_16G_DIV
        else:
            raise Exception('Accelerometer scale modifier not found.')

        # sleep off
        self.writeMaster(PWR_MGMT_1, 0x00, 0.1)

        # auto select clock source
        self.writeMaster(PWR_MGMT_1, 0x01, 0.1)

        # DLPF_CFG
        self.writeMaster(CONFIG, 0x00)
        # self.writeMaster(CONFIG, 0x03)
        # self.writeMaster(CONFIG, 0x05)

        # sample rate divider
        self.writeMaster(SMPLRT_DIV, 0x00)
        # self.writeMaster(SMPLRT_DIV, 0x04)        

        # gyro full scale select
        self.writeMaster(GYRO_CONFIG, gfs << 3)

        # accel full scale select
        self.writeMaster(ACCEL_CONFIG, afs << 3)

        # A_DLPFCFG
        self.writeMaster(ACCEL_CONFIG_2, 0x00)
        # self.writeMaster(ACCEL_CONFIG_2, 0x03)
        # self.writeMaster(ACCEL_CONFIG_2, 0x05)

        if self.address_mpu_slave is None:
            
            # BYPASS_EN enable
            self.writeMaster(INT_PIN_CFG, 0x02, 0.1) 

            # Disable master
            self.writeMaster(USER_CTRL, 0x00, 0.1)
      
        else:
 
            # BYPASS_EN disabled
            self.writeMaster(INT_PIN_CFG, 0x00, 0.1)          

            # Enable Master
            self.writeMaster(USER_CTRL, 0x20, 0.1)      
            
            # Write to MPU Slave
            self.setSlaveToWrite()

            # sleep off
            self.writeSlave(PWR_MGMT_1, 0x00, 0.1)

            # auto select clock source
            self.writeSlave(PWR_MGMT_1, 0x01, 0.1)

            # DLPF_CFG
            self.writeSlave(CONFIG, 0x00)
            # self.writeSlave(CONFIG, 0x03)
            # self.writeSlave(CONFIG, 0x05)

            # sample rate divider
            self.writeSlave(SMPLRT_DIV, 0x00)
            # self.writeSlave(SMPLRT_DIV, 0x04)    

            # gyro full scale select
            self.writeSlave(GYRO_CONFIG, gfs << 3)

            # accel full scale select
            self.writeSlave(ACCEL_CONFIG, afs << 3)

            # A_DLPFCFG
            self.writeSlave(ACCEL_CONFIG_2, 0x00)
            # self.writeSlave(ACCEL_CONFIG_2, 0x03)
            # self.writeSlave(ACCEL_CONFIG_2, 0x05)

            # BYPASS_EN enable
            self.writeSlave(INT_PIN_CFG, 0x02, 0.1)

            # Disable master
            self.writeSlave(USER_CTRL, 0x00, 0.1)
  
            # Read from MPU Slave
            self.writeMaster(I2C_SLV0_ADDR, self.address_mpu_slave | 0x80) # 0xE8
            self.writeMaster(I2C_SLV0_REG, ACCEL_OUT)
            self.writeMaster(I2C_SLV0_CTRL, 0x8E) # read 14 bytes  Acc + Gyro + Temp     

    # Configure AK8963
    # @param [in] self - The object pointer.
    # @param [in] mfs - Magneto scale select.
    # @param [in] mode - Magnetometer mode select.
    def configureAK8963(self, mfs, mode):

        if mfs == AK8963_BIT_14:
            self.mres = MAGNOMETER_SCALE_MODIFIER_BIT_14_DIV
        elif mfs == AK8963_BIT_16:
            self.mres = MAGNOMETER_SCALE_MODIFIER_BIT_16_DIV
        else:
            raise Exception('Magnetometer scale modifier not found.')

        data = []

        if self.address_mpu_slave is None:
            
            # set power down mode
            self.writeAK(AK8963_CNTL1, 0x00, 0.1)

            # set read FuseROM mode
            self.writeAK(AK8963_CNTL1, 0x0F, 0.1)

            # read coef data
            data = self.readAK(AK8963_ASAX, 3)

            # set power down mode
            self.writeAK(AK8963_CNTL1, 0x00, 0.1)

            # set scale and continous mode
            self.writeAK(AK8963_CNTL1, (mfs << 4 | mode), 0.1)
        
        else:

            # Set to write MPU Slave
            self.setSlaveToWrite(self.address_ak) 

            # set power down mode
            self.writeSlave(AK8963_CNTL1, 0x00, 0.1)

            # set read FuseROM mode
            self.writeSlave(AK8963_CNTL1, 0x0F, 0.1)

            # Address to read MPU Slave
            self.setSlaveToRead(self.address_ak)

            # read coef data
            data.append(self.readSlave(AK8963_ASAX))
            data.append(self.readSlave(AK8963_ASAY))
            data.append(self.readSlave(AK8963_ASAZ))

            # Set to write MPU Slave
            self.setSlaveToWrite(self.address_ak)

            # set power down mode
            self.writeSlave(AK8963_CNTL1, 0x00, 0.1)

            # set scale and continous mode
            self.writeSlave(AK8963_CNTL1, (mfs << 4 | mode), 0.1)

            # Read from MPU Slave
            self.writeMaster(I2C_SLV1_ADDR, self.address_ak | 0x80)
            self.writeMaster(I2C_SLV1_REG, AK8963_MAGNET_OUT)
            self.writeMaster(I2C_SLV1_CTRL, 0x87) # read 7 bytes

        self.magXcoef = (data[0] - 128) / 256.0 + 1.0
        self.magYcoef = (data[1] - 128) / 256.0 + 1.0
        self.magZcoef = (data[2] - 128) / 256.0 + 1.0
        
    # Reset sensors registers values.
    def reset(self):

        if not(self.address_mpu_slave is None):
            self.resetMPU9250Slave()

        self.resetMPU9250Master()          

    # Reset all master registers to default
    def resetMPU9250Master(self):
        self.writeMaster(PWR_MGMT_1, 0x80, 0.1) 

    # Reset all slave registers to default
    def resetMPU9250Slave(self):
        self.setSlaveToWrite()
        self.writeSlave(PWR_MGMT_1, 0x80, 0.1)

    # Read accelerometer
    #  @param [in] self - The object pointer.
    #  @retval x - x-axis data
    #  @retval y - y-axis data
    #  @retval z - z-axis data
    def readAccelerometerMaster(self):

        try:

            data = self.readMaster(ACCEL_OUT, 6)
            return self.convertAccelerometer(data, self.abias)
    
        except OSError:
            return self.getDataError()       

    def readAccelerometerSlave(self):

        if self.address_mpu_slave is None:
            return self.getDataError()

        else:   

            try:
                
                data = self.readMaster(EXT_SENS_DATA_00, 6)
                return self.convertAccelerometer(data, self.abias_slave)

            except OSError:
                return self.getDataError()
            
    def convertAccelerometer(self, data, abias):
        
        x = ((self.dataConv(data[1], data[0]) / self.ares) - abias[0]) * GRAVITY
        y = ((self.dataConv(data[3], data[2]) / self.ares) - abias[1]) * GRAVITY
        z = ((self.dataConv(data[5], data[4]) / self.ares) - abias[2]) * GRAVITY

        return [x, y, z]
        
    # Read gyroscope
    #  @param [in] self - The object pointer.
    #  @retval x - x-gyro data
    #  @retval y - y-gyro data
    #  @retval z - z-gyro data
    def readGyroscopeMaster(self):
       
        try:
            
            data = self.readMaster(GYRO_OUT, 6)
            return self.convertGyroscope(data, self.gbias)

        except OSError:
            return self.getDataError()

    def readGyroscopeSlave(self):

        if self.address_mpu_slave is None:
            return self.getDataError()

        else:   

            try:
                
                data = self.readMaster(EXT_SENS_DATA_08, 6)
                return self.convertGyroscope(data, self.gbias_slave)

            except OSError:
                return self.getDataError()
                
    def convertGyroscope(self, data, gbias):
        
        x = (self.dataConv(data[1], data[0]) / self.gres) - gbias[0]
        y = (self.dataConv(data[3], data[2]) / self.gres) - gbias[1]
        z = (self.dataConv(data[5], data[4]) / self.gres) - gbias[2]

        return [x, y, z]

    # Read magnetometer
    #  @param [in] self - The object pointer.
    #  @retval x - X-magneto data
    #  @retval y - y-magneto data
    #  @retval z - Z-magneto data
    def readMagnetometerMaster(self):

        try:
            
            data = None

            if self.address_mpu_slave is None:
                data = self.readAK(AK8963_MAGNET_OUT, 7)

            else:   
                data = self.readMaster(EXT_SENS_DATA_14, 7)          

            return self.convertMagnetometer(data)
            
        except OSError:
            return self.getDataError()        

    def readMagnetometerSlave(self):
        return self.getDataError()
    
    def convertMagnetometer(self, data):

        # check overflow
        if (data[6] & 0x08) != 0x08:
            x = (self.dataConv(data[0], data[1]) / self.mres) * self.magXcoef
            y = (self.dataConv(data[2], data[3]) / self.mres) * self.magYcoef
            z = (self.dataConv(data[4], data[5]) / self.mres) * self.magZcoef
            return [x, y, z]
        
        else:
            return self.getDataError()

    # Read temperature
    #  @param [in] self - The object pointer.
    #  @retval temperature - temperature(degrees C)
    def readTemperatureMaster(self):

        try:
            
            data = self.readMaster(TEMP_OUT, 2)
            return self.convertTemperature(data) 

        except OSError:
            return None
        
    def readTemperatureSlave(self):

        try:
            
            data = self.readMaster(EXT_SENS_DATA_06, 2)
            return self.convertTemperature(data)

        except OSError:
            return None

    def convertTemperature(self, data):
        temp = self.dataConv(data[1], data[0])
        temp = (temp / 333.87 + 21.0)
        return temp

    # Get array with data from all sensors
    def getAllData(self): 

        timestamp = time.time()
        
        try:
            
            dataMPU = self.readMaster(FIRST_DATA_POSITION, 28)
            dataAK = self.readMagnetometerMaster()

            accMaster = self.convertAccelerometer(dataMPU[0:6], self.abias)
            # tempMaster = self.convertTemperature(dataMPU[6:8])
            gyroMaster = self.convertGyroscope(dataMPU[8:14], self.gbias)

            if not(self.address_mpu_slave is None):
                accSlave = self.convertAccelerometer(dataMPU[14:20], self.abias_slave)
                # tempSlave = self.convertTemperature(dataMPU[20:22])
                gyroSlave = self.convertGyroscope(dataMPU[22:28], self.gbias_slave)
    
            else:
                accSlave = [0, 0, 0]
                # tempSlave = [0]
                gyroSlave = [0, 0, 0]

            return [timestamp] + accMaster + gyroMaster + accSlave + gyroSlave + dataAK
    
        except OSError:
            return [timestamp, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]       

    # Data when data is not available/error when read
    def getDataError(self):
        return [0, 0, 0]
   
    # Data Convert
    # @param [in] self: The object pointer.
    # @param [in] data1: LSB
    # @param [in] data2: MSB
    # @retval Value: MSB+LSB(int 16bit)
    def dataConv(self, data1, data2):

        value = data1 | (data2 << 8)

        if(value & (1 << 16 - 1)):
            value -= (1 << 16)

        return value

    # Search MPU Device
    #  @param [in] self: The object pointer.
    #  @retval true: device connected
    #  @retval false: device error
    def searchMPUDevice(self):
        who_am_i = self.readMaster(WHO_AM_I, 1)[0]
        return who_am_i == DEVICE_ID

    #  Check MPU data ready
    #  @param [in] self: The object pointer.
    #  @retval true: data is ready
    #  @retval false: data is not ready
    def checkMPUDataReady(self):
        drdy = self.readMaster(INT_STATUS, 1)[0]
        return drdy & 0x01

    #  Check AK data ready
    #  @param [in] self: The object pointer.
    #  @retval true: data is ready
    #  @retval false: data is not ready
    def checkAKDataReady(self):
        drdy = self.readAK(AK8963_ST1, 1)[0]
        return drdy & 0x01

    # Funciona apenas com master e não slave. Necessário posicionar corretamente o MPU antes.
    # Function which accumulates gyro and accelerometer data after device initialization. It calculates the average
    # of the at-rest readings and then loads the resulting offsets into accelerometer and gyro bias registers.
    def calibrateMPU6050(self):

        # reset device
        self.reset()

        # get stable time source; Auto select clock source to be PLL gyroscope reference if ready, else use the internal oscillator, bits 2:0 = 001
        self.writeMaster(PWR_MGMT_1, 0x01)
        self.writeMaster(PWR_MGMT_1, 0x00, 0.2)

        # Configure device for bias calculation
        self.writeMaster(INT_ENABLE, 0x00) # Disable all interrupts
        self.writeMaster(FIFO_EN, 0x00) # Disable FIFO
        self.writeMaster(PWR_MGMT_1, 0x00) # Turn on internal clock source
        self.writeMaster(I2C_MST_CTRL, 0x00) # Disable I2C master
        self.writeMaster(USER_CTRL, 0x00) # Disable FIFO and I2C master modes
        self.writeMaster(USER_CTRL, 0x0C, 0.015) # Reset FIFO and DMP

        # Configure MPU6050 gyro and accelerometer for bias calculation
        self.writeMaster(CONFIG, 0x01) # Set low-pass filter to 188 Hz
        self.writeMaster(SMPLRT_DIV, 0x00) # Set sample rate to 1 kHz
        self.writeMaster(GYRO_CONFIG, 0x00) # Set gyro full-scale to 250 degrees per second, maximum sensitivity
        self.writeMaster(ACCEL_CONFIG, 0x00) # Set accelerometer full-scale to 2 g, maximum sensitivity

        # Configure FIFO to capture accelerometer and gyro data for bias calculation
        self.writeMaster(USER_CTRL, 0x40) # Enable FIFO
        self.writeMaster(FIFO_EN, 0x78, 0.04) # Enable gyro and accelerometer sensors for FIFO  (max size 512 bytes in MPU-9150) # 0.4 - accumulate 40 samples in 40 milliseconds = 480 bytes

        # At end of sample accumulation, turn off FIFO sensor read
        self.writeMaster(FIFO_EN, 0x00) # Disable gyro and accelerometer sensors for FIFO
      
        # read FIFO sample count
        data = self.readMaster(FIFO_COUNTH, 2) 
        fifo_count = self.dataConv(data[1], data[0])
        packet_count = int(fifo_count / 12); # How many sets of full gyro and accelerometer data for averaging

        index = 0
        accel_bias = [0, 0, 0] 
        gyro_bias = [0, 0, 0]

        while index < packet_count:

            # read data for averaging
            data = self.readMaster(FIFO_R_W, 12) 

            # Form signed 16-bit integer for each sample in FIFO
            # Sum individual signed 16-bit biases to get accumulated signed 32-bit biases
            accel_bias[0] += self.dataConv(data[1], data[0]) 
            accel_bias[1] += self.dataConv(data[3], data[2])
            accel_bias[2] += self.dataConv(data[5], data[4])
            gyro_bias[0] += self.dataConv(data[7], data[6])
            gyro_bias[1] += self.dataConv(data[9], data[8])
            gyro_bias[2] += self.dataConv(data[11], data[10])

            index += 1

        # Normalize sums to get average count biases
        accel_bias[0] /= packet_count 
        accel_bias[1] /= packet_count
        accel_bias[2] /= packet_count
        gyro_bias[0] /= packet_count
        gyro_bias[1] /= packet_count
        gyro_bias[2] /= packet_count

        # Remove gravity from the z-axis accelerometer bias calculation
        if accel_bias[2] > 0:
            accel_bias[2] -= ACCEL_SCALE_MODIFIER_2G_DIV
        else:
            accel_bias[2] += ACCEL_SCALE_MODIFIER_2G_DIV

        self.abias = [
            (accel_bias[0] / ACCEL_SCALE_MODIFIER_2G_DIV),
            (accel_bias[1] / ACCEL_SCALE_MODIFIER_2G_DIV),
            (accel_bias[2] / ACCEL_SCALE_MODIFIER_2G_DIV)
        ]

        self.gbias = [
            (gyro_bias[0] / GYRO_SCALE_MODIFIER_250DEG_DIV),
            (gyro_bias[1] / GYRO_SCALE_MODIFIER_250DEG_DIV),
            (gyro_bias[2] / GYRO_SCALE_MODIFIER_250DEG_DIV)
        ]

        if not(self.address_mpu_slave is None):

            # Reset all
            self.reset()

            # BYPASS_EN disabled
            self.writeMaster(INT_PIN_CFG, 0x00, 0.1)          

            # Enable Master
            self.writeMaster(USER_CTRL, 0x20, 0.1)
            
            # Address to write MPU Slave
            self.setSlaveToWrite()

            # get stable time source; Auto select clock source to be PLL gyroscope reference if ready, else use the internal oscillator, bits 2:0 = 001
            self.writeSlave(PWR_MGMT_1, 0x01)
            self.writeSlave(PWR_MGMT_1, 0x00, 0.2)

            # Configure device for bias calculation
            self.writeSlave(INT_ENABLE, 0x00) # Disable all interrupts
            self.writeSlave(FIFO_EN, 0x00) # Disable FIFO
            self.writeSlave(PWR_MGMT_1, 0x00) # Turn on internal clock source
            self.writeSlave(I2C_MST_CTRL, 0x00) # Disable I2C master
            self.writeSlave(USER_CTRL, 0x00) # Disable FIFO and I2C master modes
            self.writeSlave(USER_CTRL, 0x0C, 0.015) # Reset FIFO and DMP

            # Configure MPU6050 gyro and accelerometer for bias calculation
            self.writeSlave(CONFIG, 0x01) # Set low-pass filter to 188 Hz
            self.writeSlave(SMPLRT_DIV, 0x00) # Set sample rate to 1 kHz
            self.writeSlave(GYRO_CONFIG, 0x00) # Set gyro full-scale to 250 degrees per second, maximum sensitivity
            self.writeSlave(ACCEL_CONFIG, 0x00) # Set accelerometer full-scale to 2 g, maximum sensitivity

            # Configure FIFO to capture accelerometer and gyro data for bias calculation
            self.writeSlave(USER_CTRL, 0x40) # Enable FIFO
            self.writeSlave(FIFO_EN, 0x78, 0.04) # Enable gyro and accelerometer sensors for FIFO  (max size 512 bytes in MPU-9150) # 0.4 - accumulate 40 samples in 40 milliseconds = 480 bytes

            # At end of sample accumulation, turn off FIFO sensor read
            self.writeSlave(FIFO_EN, 0x00) # Disable gyro and accelerometer sensors for FIFO
        
            # Slave to read
            self.setSlaveToRead()

            # read FIFO sample count
            data = []
            data.append(self.readSlave(FIFO_COUNTH)) 
            data.append(self.readSlave(FIFO_COUNTL)) 

            fifo_count = self.dataConv(data[1], data[0])
            packet_count = int(fifo_count / 12); # How many sets of full gyro and accelerometer data for averaging

            if fifo_count == 0:
                print("Não foi possível conectar no slave para calibrar")
            
            else:

                index = 0
                accel_bias = [0, 0, 0] 
                gyro_bias = [0, 0, 0]

                while index < packet_count:

                    i = 0
                    data = []

                    while i < 12:
                        data.append(self.readSlave(FIFO_R_W)) # read data for averaging
                        i += 1

                    # Form signed 16-bit integer for each sample in FIFO
                    # Sum individual signed 16-bit biases to get accumulated signed 32-bit biases
                    accel_bias[0] += self.dataConv(data[1], data[0]) 
                    accel_bias[1] += self.dataConv(data[3], data[2])
                    accel_bias[2] += self.dataConv(data[5], data[4])
                    gyro_bias[0] += self.dataConv(data[7], data[6])
                    gyro_bias[1] += self.dataConv(data[9], data[8])
                    gyro_bias[2] += self.dataConv(data[11], data[10])

                    index += 1

                # Normalize sums to get average count biases
                accel_bias[0] /= packet_count 
                accel_bias[1] /= packet_count
                accel_bias[2] /= packet_count
                gyro_bias[0] /= packet_count
                gyro_bias[1] /= packet_count
                gyro_bias[2] /= packet_count

                # Remove gravity from the z-axis accelerometer bias calculation
                if accel_bias[2] > 0:
                    accel_bias[2] -= ACCEL_SCALE_MODIFIER_2G_DIV
                else:
                    accel_bias[2] += ACCEL_SCALE_MODIFIER_2G_DIV

                self.abias_slave = [
                    (accel_bias[0] / ACCEL_SCALE_MODIFIER_2G_DIV),
                    (accel_bias[1] / ACCEL_SCALE_MODIFIER_2G_DIV),
                    (accel_bias[2] / ACCEL_SCALE_MODIFIER_2G_DIV)
                ]

                self.gbias_slave = [
                    (gyro_bias[0] / GYRO_SCALE_MODIFIER_250DEG_DIV),
                    (gyro_bias[1] / GYRO_SCALE_MODIFIER_250DEG_DIV),
                    (gyro_bias[2] / GYRO_SCALE_MODIFIER_250DEG_DIV)
                ]

        self.reset()

    ################################################################## Master Methods ##################################################################

    def writeAK(self, register, value, sleep = 0):

        self.bus.write_byte_data(self.address_ak, register, value)

        if sleep > 0:
            time.sleep(sleep)

    def readAK(self, register, quantity):
        return self.bus.read_i2c_block_data(self.address_ak, register, quantity)

    def writeMaster(self, register, value, sleep = 0):
        
        self.bus.write_byte_data(self.address_mpu_master, register, value)

        if sleep > 0:
            time.sleep(sleep)

    def readMaster(self, register, quantity):
        return self.bus.read_i2c_block_data(self.address_mpu_master, register, quantity)

    ################################################################## Slave Methods ##################################################################

    # Set to write MPU Slave
    def setSlaveToWrite(self, address=None):

        if address is None:
            address = self.address_mpu_slave

        self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_ADDR, address) 

    # Write in slave
    def writeSlave(self, register, value, sleep = 0):
        self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, register)
        self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_DO, value)
        self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)

        if sleep > 0:
            time.sleep(sleep)

    # Set to read MPU Slave
    def setSlaveToRead(self, address=None):

        if address is None:
            address = self.address_mpu_slave

        self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_ADDR, address | 0x80) 

    # Read from slave
    def readSlave(self, register):
        self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, register)
        self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)
        return self.bus.read_byte_data(self.address_mpu_master, I2C_SLV4_DI)
