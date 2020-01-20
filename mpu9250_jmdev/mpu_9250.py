#####################################################################
# Author: Jeferson Menegazzo                                        #
# Year: 2020                                                        #
# License: MIT                                                      #
#####################################################################

"""
Based on:
https://github.com/nickcoutsos/MPU-6050-Python/blob/master/MPU6050.py
https://github.com/Tijndagamer/mpu6050/blob/master/mpu6050/mpu6050.py
https://github.com/FaBoPlatform/FaBo9AXIS-MPU9250-Python/blob/master/FaBo9Axis_MPU9250/MPU9250.py
https://github.com/kriswiner/MPU6050/blob/master/MPU6050IMU.ino
https://github.com/kriswiner/MPU6050/wiki/Simple-and-Effective-Magnetometer-Calibration
https://github.com/kriswiner/MPU9250/blob/master/MPU9250_MS5637_AHRS_t3.ino
"""

try:
    # smbus2 is faster than smbus
    # import smbus
    import smbus2 as smbus
except ImportError:
    print("\n", "Using Fake SMBus", "\n", "Install requirements.", "\n")
    from mpu9250_jmdev.fake_smbus import FakeSmbus as smbus

from mpu9250_jmdev.registers import *
import time

class MPU9250:

    # Address Settings
    address_ak = None
    address_mpu_master = None
    address_mpu_slave = None
    bus = None

    # Sensor Full Scale
    gfs = None # Gyroscope
    afs = None # Accelerometer
    mfs = None # Magnetometer
    mode = None # Magnetometer Mode

    # Sensor Resolution - Scale Factor
    gres = None # Gyroscope
    ares = None # Accelerometer
    mres = None # Magnetometer

    # Factory Magnetometer Calibration and Bias
    magCalibration = [0, 0, 0] 

    # Magnetometer Soft Iron Distortion
    magScale = [1, 1, 1]

    # Master and Slave Biases
    gbias = [0, 0, 0] # Gyroscope Master Bias
    gbias_slave = [0, 0, 0] # Gyroscope Slave Bias
    abias = [0, 0, 0] # Accelerometer Master Bias
    abias_slave = [0, 0, 0] # Accelerometer Slave Bias
    mbias = [0, 0, 0]  # Magnetometer Hard Iron Distortion

    # Constructor
    # @param [in] self - The object pointer.
    # @param [in] address_ak - AK8963 I2C slave address (default:AK8963_ADDRESS[0x0C]).
    # @param [in] address_mpu_master - MPU-9250 I2C address (default:MPU9050_ADDRESS_68[0x68]).
    # @param [in] address_mpu_slave - MPU-9250 I2C slave address (default:[None]).
    # @param [in] bus - I2C bus board (default:Board Revision 2[1]).
    # @param [in] gfs - Gyroscope full scale select (default:GFS_2000[2000dps]).
    # @param [in] afs - Accelerometer full scale select (default:AFS_16G[16g]).
    # @param [in] mfs - Magnetometer scale select (default:AK8963_BIT_16[16bit])
    # @param [in] mode - Magnetometer mode select (default:AK8963_MODE_C100HZ[Continous 100Hz])
    def __init__(self, 
        address_ak=AK8963_ADDRESS, 
        address_mpu_master=MPU9050_ADDRESS_68, 
        address_mpu_slave=None, 
        bus=1, 
        gfs=GFS_2000, 
        afs=AFS_16G, 
        mfs=AK8963_BIT_16, 
        mode=AK8963_MODE_C100HZ
    ):
        self.address_ak = address_ak
        self.address_mpu_master = address_mpu_master
        self.address_mpu_slave = address_mpu_slave
        self.bus = smbus.SMBus(bus)
        self.gfs = gfs
        self.afs = afs
        self.mfs = mfs
        self.mode = mode
       
    # Configure MPU-9250
    # @param [in] self - The object pointer.
    # @param [in] retry - number of retries.
    def configure(self, retry=3):
    
        try:
            self.configureMPU6500(self.gfs, self.afs)
            self.configureAK8963(self.mfs, self.mode)
        
        except OSError as err:

            if(retry > 1):
                self.configure(retry - 1)

            else:
                raise err

    # Configure MPU-6500
    # @param [in] self - The object pointer.
    # @param [in] gfs - Gyroscope full scale select.
    # @param [in] afs - Accelerometer full scale select.
    def configureMPU6500(self, gfs, afs):

        if gfs == GFS_250:
            self.gres = GYRO_SCALE_MODIFIER_250DEG
        elif gfs == GFS_500:
            self.gres = GYRO_SCALE_MODIFIER_500DEG
        elif gfs == GFS_1000:
            self.gres = GYRO_SCALE_MODIFIER_1000DEG
        elif gfs == GFS_2000:
            self.gres = GYRO_SCALE_MODIFIER_2000DEG
        else:
            raise Exception('Gyroscope scale modifier not found.')

        if afs == AFS_2G:
            self.ares = ACCEL_SCALE_MODIFIER_2G
        elif afs == AFS_4G:
            self.ares = ACCEL_SCALE_MODIFIER_4G
        elif afs == AFS_8G:
            self.ares = ACCEL_SCALE_MODIFIER_8G
        elif afs == AFS_16G:
            self.ares = ACCEL_SCALE_MODIFIER_16G
        else:
            raise Exception('Accelerometer scale modifier not found.')

        # sleep off
        self.writeMaster(PWR_MGMT_1, 0x00, 0.1)

        # auto select clock source
        self.writeMaster(PWR_MGMT_1, 0x01, 0.1)

        # DLPF_CFG
        self.writeMaster(CONFIG, 0x00)
        # self.writeMaster(CONFIG, 0x03)

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

        if not(self.hasSlave()):
            
            # BYPASS_EN enable
            self.writeMaster(INT_PIN_CFG, 0x02, 0.1) 

            # Disable master
            self.writeMaster(USER_CTRL, 0x00, 0.1)
      
        else:
 
            # BYPASS_EN disabled
            self.writeMaster(INT_PIN_CFG, 0x00, 0.1)          
            # self.writeMaster(INT_PIN_CFG, 0x22, 0.1)          

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
            self.writeMaster(I2C_SLV0_CTRL, 0x8E) # read 14 bytes  Acc(6) + Gyro(6) + Temp(2)     

    # Configure AK8963
    # @param [in] self - The object pointer.
    # @param [in] mfs - Magnetometer full scale select.
    # @param [in] mode - Magnetometer mode select.
    def configureAK8963(self, mfs, mode):

        if mfs == AK8963_BIT_14:
            self.mres = MAGNOMETER_SCALE_MODIFIER_BIT_14
        elif mfs == AK8963_BIT_16:
            self.mres = MAGNOMETER_SCALE_MODIFIER_BIT_16
        else:
            raise Exception('Magnetometer scale modifier not found.')

        data = []

        if not(self.hasSlave()):
            
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

        self.magCalibration = [
            (data[0] - 128) / 256.0 + 1.0,
            (data[1] - 128) / 256.0 + 1.0,
            (data[2] - 128) / 256.0 + 1.0
        ]
        
    # Resets the values of the sensor registers.
    # @param [in] self - The object pointer.
    # @param [in] retry - number of retries.
    def reset(self, retry=3):

        try:
            
            if self.hasSlave():
                self.resetMPU9250Slave()

            self.resetMPU9250Master()
        
        except OSError as err:

            if(retry > 1):
                self.reset(retry - 1)

            else:
                raise err

    # Reset all master registers to default.
    # @param [in] self - The object pointer.
    def resetMPU9250Master(self):
        self.writeMaster(PWR_MGMT_1, 0x80, 0.1) 

    # Reset all slave registers to default.
    # @param [in] self - The object pointer.
    def resetMPU9250Slave(self):
        self.setSlaveToWrite()
        self.writeSlave(PWR_MGMT_1, 0x80, 0.1)

    # Read accelerometer from master.
    #  @param [in] self - The object pointer.
    #  @retval [x, y, z] - acceleration data.
    def readAccelerometerMaster(self):

        try:

            data = self.readMaster(ACCEL_OUT, 6)
            return self.convertAccelerometer(data, self.abias)
    
        except OSError:
            return self.getDataError()       

    # Read accelerometer from slave.
    #  @param [in] self - The object pointer.
    #  @retval [x, y, z] - acceleration data.
    def readAccelerometerSlave(self):

        if self.hasSlave():   

            try:
                
                data = self.readMaster(EXT_SENS_DATA_00, 6)
                return self.convertAccelerometer(data, self.abias_slave)

            except OSError:
                return self.getDataError()

        else:
            return self.getDataError()
            
    # Convert accelerometer byte block to apply scale factor and biases.
    #  @param [in] self - The object pointer.
    #  @param [in] data - accelerometer 6-byte block.
    #  @param [in] abias - biases.
    #  @retval [x, y, z] - acceleration data.
    def convertAccelerometer(self, data, abias):
        
        x = (self.dataConv(data[1], data[0]) * self.ares) - abias[0]
        y = (self.dataConv(data[3], data[2]) * self.ares) - abias[1]
        z = (self.dataConv(data[5], data[4]) * self.ares) - abias[2]

        return [x, y, z]
        
    # Read gyroscope from master.
    #  @param [in] self - The object pointer.
    #  @retval [x, y, z] - gyroscope data.
    def readGyroscopeMaster(self):
       
        try:
            
            data = self.readMaster(GYRO_OUT, 6)
            return self.convertGyroscope(data, self.gbias)

        except OSError:
            return self.getDataError()

    # Read gyroscope from slave.
    #  @param [in] self - The object pointer.
    #  @retval [x, y, z] - gyroscope data.
    def readGyroscopeSlave(self):

        if self.hasSlave():

            try:
                
                data = self.readMaster(EXT_SENS_DATA_08, 6)
                return self.convertGyroscope(data, self.gbias_slave)

            except OSError:
                return self.getDataError()

        else:
            return self.getDataError()

    # Convert gyroscope byte block to apply scale factor and biases.
    #  @param [in] self - The object pointer.
    #  @param [in] data - gyroscope 6-byte block.
    #  @param [in] gbias - biases.
    #  @retval [x, y, z] - gyroscope data.            
    def convertGyroscope(self, data, gbias):
        
        x = (self.dataConv(data[1], data[0]) * self.gres) - gbias[0]
        y = (self.dataConv(data[3], data[2]) * self.gres) - gbias[1]
        z = (self.dataConv(data[5], data[4]) * self.gres) - gbias[2]

        return [x, y, z]

    # Read magnetometer from master.
    #  @param [in] self - The object pointer.
    #  @retval [x, y, z] - magnetometer data.   
    def readMagnetometerMaster(self):

        try:
            
            data = None

            if self.hasSlave():
                data = self.readMaster(EXT_SENS_DATA_14, 7)          
                
            else:   
                data = self.readAK(AK8963_MAGNET_OUT, 7)

            return self.convertMagnetometer(data)
            
        except OSError:
            return self.getDataError()        

    # Convert magnetometer byte block to apply scale factor, biases and coeficiente.
    #  @param [in] self - The object pointer.
    #  @param [in] data - magnetometer 7-byte block.
    #  @retval [x, y, z] - magnetometer data.   
    def convertMagnetometer(self, data):

        # check overflow
        if (data[6] & 0x08) != 0x08:
            x = (self.dataConv(data[0], data[1]) * self.mres * self.magCalibration[0]) - self.mbias[0]
            y = (self.dataConv(data[2], data[3]) * self.mres * self.magCalibration[1]) - self.mbias[1]
            z = (self.dataConv(data[4], data[5]) * self.mres * self.magCalibration[2]) - self.mbias[2]
            x *= self.magScale[0]
            y *= self.magScale[1]
            z *= self.magScale[2]
            return [x, y, z]
        
        else:
            return self.getDataError()

    # Read temperature from master.
    #  @param [in] self - The object pointer.
    #  @retval temperature - temperature(degrees C).
    def readTemperatureMaster(self):

        try:
            
            data = self.readMaster(TEMP_OUT, 2)
            return self.convertTemperature(data) 

        except OSError:
            return 0

    # Read temperature from slave.
    #  @param [in] self - The object pointer.
    #  @retval temperature - temperature(degrees C).   
    def readTemperatureSlave(self):

        try:
            
            data = self.readMaster(EXT_SENS_DATA_06, 2)
            return self.convertTemperature(data)

        except OSError:
            return 0

    # Convert temperature byte block to apply to a value in measure unit degrees Centigrade (º C).
    #  @param [in] self - The object pointer.
    #  @param [in] data - temperature 2-byte block.
    #  @retval temperature - temperature data.   
    def convertTemperature(self, data):
        temp = self.dataConv(data[1], data[0])
        temp = (temp / 333.87 + 21.0)
        return temp

    # Get array with data from all sensors obtained at same time.
    #  @param [in] self - The object pointer.
    #  @retval [[timestamp], [accMaster], [gyroMaster], [accSlave], [gyroSlave], [dataAK], [tempMaster], [tempSlave] ] - all sensors data.   
    def getAllData(self): 

        timestamp = time.time()
        
        try:
            
            dataMPU = self.readMaster(FIRST_DATA_POSITION, 28)
            dataAK = self.readMagnetometerMaster()
           
            accMaster = self.convertAccelerometer(dataMPU[0:6], self.abias)
            tempMaster = self.convertTemperature(dataMPU[6:8])
            gyroMaster = self.convertGyroscope(dataMPU[8:14], self.gbias)

            if self.hasSlave():
                accSlave = self.convertAccelerometer(dataMPU[14:20], self.abias_slave)
                tempSlave = self.convertTemperature(dataMPU[20:22])
                gyroSlave = self.convertGyroscope(dataMPU[22:28], self.gbias_slave)

            else:               
                accSlave = self.getDataError()
                tempSlave = 0
                gyroSlave = self.getDataError()

            return [timestamp] + accMaster + gyroMaster + accSlave + gyroSlave + dataAK + [tempMaster] + [tempSlave]
    
        except OSError:
            return [timestamp] + self.getDataError() + self.getDataError() + self.getDataError() + self.getDataError() + self.getDataError() + [0, 0]        

    # Get array with labels for data obtained from getAllData.
    #  @param [in] self - The object pointer.
    #  @retval labels.
    def getAllDataLabels(self):
    
        return [
            "timestamp", 
            "master_acc_x", 
            "master_acc_y", 
            "master_acc_z", 
            "master_gyro_x", 
            "master_gyro_y", 
            "master_gyro_z", 
            "slave_acc_x", 
            "slave_acc_y", 
            "slave_acc_z", 
            "slave_gyro_x", 
            "slave_gyro_y", 
            "slave_gyro_z", 
            "mag_x",
            "mag_y",
            "mag_z",
            "master_temp",
            "slave_temp"
        ]

    # When data is not available/error when read, is returned an array with 0.
    #  @param [in] self - The object pointer.
    def getDataError(self):
        return [0, 0, 0]
   
    # Data Convert
    # @param [in] self - The object pointer.
    # @param [in] data1 - LSB
    # @param [in] data2 - MSB
    # @retval Value: MSB+LSB(int 16bit)
    def dataConv(self, data1, data2):

        value = data1 | (data2 << 8)

        if(value & (1 << 16 - 1)):
            value -= (1 << 16)

        return value

    # Search MPU Device master.
    #  @param [in] self - The object pointer.
    #  @retval true - device connected
    #  @retval false - device error
    def searchMPUDevice(self):
        who_am_i = self.readMaster(WHO_AM_I, 1)[0]
        return who_am_i == DEVICE_ID

    #  Check MPU data ready master.
    #  @param [in] self - The object pointer.
    #  @retval true - data is ready
    #  @retval false - data is not ready
    def checkMPUDataReady(self):
        drdy = self.readMaster(INT_STATUS, 1)[0]
        return drdy & 0x01

    #  Check AK data ready.
    #  @param [in] self - The object pointer.
    #  @retval true - data is ready
    #  @retval false - data is not ready
    def checkAKDataReady(self):
        drdy = self.readAK(AK8963_ST1, 1)[0]
        return drdy & 0x01

    #  Check if MPU has slave.
    #  @param [in] self - The object pointer.
    #  @retval true - if has slave (another MPU)
    #  @retval false - if has not slave
    def hasSlave(self):
        return not(self.address_mpu_slave is None)

    # Calibrate all sensors.
    #  @param [in] self - The object pointer.
    #  @param [in] retry - number of retries.
    def calibrate(self, retry=3):

        try:
            print("Calibrating", hex(self.address_mpu_master), "- AK8963")
            self.calibrateAK8963()
            print("Calibrating", hex(self.address_mpu_master), "- MPU6500")
            self.calibrateMPU6500()

        except OSError as err:

            if(retry > 1):
                self.calibrate(retry - 1)

            else:
                raise err

    # This function calibrate MPU6500 and load biases to params in this class.
    # To calibrate, you must correctly position the MPU so that gravity is all along the z axis of the accelerometer.
    # This function accumulates gyro and accelerometer data after device initialization. It calculates the average
    # of the at-rest readings and then loads the resulting offsets into accelerometer and gyro bias registers.
    # This function reset sensor registers. Configure must be called after.
    #  @param [in] self - The object pointer.
    def calibrateMPU6500(self):

        # reset device
        self.reset()

        # get stable time source; Auto select clock source to be PLL gyroscope reference if ready, else use the internal oscillator, bits 2:0 = 001
        self.writeMaster(PWR_MGMT_1, 0x01)
        self.writeMaster(PWR_MGMT_2, 0x00, 0.2)

        # Configure device for bias calculation
        self.writeMaster(INT_ENABLE, 0x00) # Disable all interrupts
        self.writeMaster(FIFO_EN, 0x00) # Disable FIFO
        self.writeMaster(PWR_MGMT_1, 0x00) # Turn on internal clock source
        self.writeMaster(I2C_MST_CTRL, 0x00) # Disable I2C master
        self.writeMaster(USER_CTRL, 0x00) # Disable FIFO and I2C master modes
        self.writeMaster(USER_CTRL, 0x0C, 0.015) # Reset FIFO and DMP

        # Configure MPU6500 gyro and accelerometer for bias calculation
        self.writeMaster(CONFIG, 0x01) # Set low-pass filter to 188 Hz
        self.writeMaster(SMPLRT_DIV, 0x00) # Set sample rate to 1 kHz
        self.writeMaster(GYRO_CONFIG, 0x00) # Set gyro full-scale to 250 degrees per second, maximum sensitivity
        self.writeMaster(ACCEL_CONFIG, 0x00) # Set accelerometer full-scale to 2G, maximum sensitivity

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

        # Output scaled gyro biases for display in the main program
        self.gbias = [
            (gyro_bias[0] / GYRO_SCALE_MODIFIER_250DEG_DIV),
            (gyro_bias[1] / GYRO_SCALE_MODIFIER_250DEG_DIV),
            (gyro_bias[2] / GYRO_SCALE_MODIFIER_250DEG_DIV)
        ]

        # Output scaled accelerometer biases for manual subtraction in the main program
        self.abias = [
            (accel_bias[0] / ACCEL_SCALE_MODIFIER_2G_DIV),
            (accel_bias[1] / ACCEL_SCALE_MODIFIER_2G_DIV),
            (accel_bias[2] / ACCEL_SCALE_MODIFIER_2G_DIV)
        ]

        if self.hasSlave():

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
            self.writeSlave(PWR_MGMT_2, 0x00, 0.2)

            # Configure device for bias calculation
            self.writeSlave(INT_ENABLE, 0x00) # Disable all interrupts
            self.writeSlave(FIFO_EN, 0x00) # Disable FIFO
            self.writeSlave(PWR_MGMT_1, 0x00) # Turn on internal clock source
            self.writeSlave(I2C_MST_CTRL, 0x00) # Disable I2C master
            self.writeSlave(USER_CTRL, 0x00) # Disable FIFO and I2C master modes
            self.writeSlave(USER_CTRL, 0x0C, 0.015) # Reset FIFO and DMP

            # Configure MPU6500 gyro and accelerometer for bias calculation
            self.writeSlave(CONFIG, 0x01) # Set low-pass filter to 188 Hz
            self.writeSlave(SMPLRT_DIV, 0x00) # Set sample rate to 1 kHz
            self.writeSlave(GYRO_CONFIG, 0x00) # Set gyro full-scale to 250 degrees per second, maximum sensitivity
            self.writeSlave(ACCEL_CONFIG, 0x00) # Set accelerometer full-scale to 2G, maximum sensitivity

            # Configure FIFO to capture accelerometer and gyro data for bias calculation
            self.writeSlave(USER_CTRL, 0x40) # Enable FIFO
            self.writeSlave(FIFO_EN, 0x78, 0.04) # Enable gyro and accelerometer sensors for FIFO  (max size 512 bytes in MPU-9150) # 0.4 - accumulate 40 samples in 40 milliseconds = 480 bytes

            # At end of sample accumulation, turn off FIFO sensor read
            self.writeSlave(FIFO_EN, 0x00) # Disable gyro and accelerometer sensors for FIFO
        
            # Slave to read
            self.setSlaveToRead()

            # read FIFO sample count
            data = [
                self.readSlave(FIFO_COUNTH),
                self.readSlave(FIFO_COUNTL)
            ]

            fifo_count = self.dataConv(data[1], data[0])
            packet_count = int(fifo_count / 12); # How many sets of full gyro and accelerometer data for averaging

            if fifo_count == 0:
                print("Could not connect to slave to calibrate")

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

    # This function calibrate AK8963 and load biases to params in this class.
    # This function reset sensor registers. Configure must be called after.
    #  @param [in] self - The object pointer.
    def calibrateAK8963(self):
        
        self.configureAK8963(self.mfs, self.mode)

        index = 0
        sample_count = 0
        mag_bias = [0, 0, 0]
        mag_scale = [0, 0, 0]
        mag_max = [-32767, -32767, -32767]
        mag_min = [32767, 32767, 32767]
        mag_temp = [0, 0, 0]

        # shoot for ~fifteen seconds of mag data
        if (self.mode == AK8963_MODE_C8HZ):
            sample_count = 128; # at 8 Hz ODR, new mag data is available every 125 ms
        
        if (self.mode == AK8963_MODE_C100HZ):
            sample_count = 1500; # at 100 Hz ODR, new mag data is available every 10 ms

        index = 0
        
        while index < sample_count:

            index += 1
            data = None

            if self.hasSlave():
                data = self.readMaster(EXT_SENS_DATA_14, 7) 

            else:   
                data = self.readAK(AK8963_MAGNET_OUT, 7)
                    
            # check overflow
            if (data[6] & 0x08) != 0x08:
                
                mag_temp = [
                    self.dataConv(data[0], data[1]),
                    self.dataConv(data[2], data[3]),
                    self.dataConv(data[4], data[5])
                ]  
      
            else:
                mag_temp = self.getDataError()

            indexAxes = 0

            while indexAxes < 3:

                if (mag_temp[indexAxes] > mag_max[indexAxes]):
                    mag_max[indexAxes] = mag_temp[indexAxes]
    
                if (mag_temp[indexAxes] < mag_min[indexAxes]):
                    mag_min[indexAxes] = mag_temp[indexAxes]

                indexAxes += 1

            if (self.mode == AK8963_MODE_C8HZ):
                time.sleep(0.135) # at 8 Hz ODR, new mag data is available every 125 ms
            
            if (self.mode == AK8963_MODE_C100HZ):
                time.sleep(0.012); # at 100 Hz ODR, new mag data is available every 10 ms

        # Get hard iron correction
        mag_bias[0] = (mag_max[0] + mag_min[0]) / 2 # get average x mag bias in counts
        mag_bias[1] = (mag_max[1] + mag_min[1]) / 2 # get average y mag bias in counts
        mag_bias[2] = (mag_max[2] + mag_min[2]) / 2 # get average z mag bias in counts

        # save mag biases in G for main program
        self.mbias = [
            mag_bias[0] * self.mres * self.magCalibration[0],
            mag_bias[1] * self.mres * self.magCalibration[1],
            mag_bias[2] * self.mres * self.magCalibration[2]
        ]

        # Get soft iron correction estimate
        mag_scale[0] = (mag_max[0] - mag_min[0]) / 2 # get average x axis max chord length in counts
        mag_scale[1] = (mag_max[1] - mag_min[1]) / 2 # get average y axis max chord length in counts
        mag_scale[2] = (mag_max[2] - mag_min[2]) / 2 # get average z axis max chord length in counts

        avg_rad = mag_scale[0] + mag_scale[1] + mag_scale[2]
        avg_rad /= 3.0

        self.magScale = [
            avg_rad / mag_scale[0],
            avg_rad / mag_scale[1],
            avg_rad / mag_scale[2]
        ]

    # Get array with settings from all sensors obtained at same time.
    #  @param [in] self - The object pointer.
    #  @retval [[timestamp], [addresses], [fullScale], [resolution], [gbias], [gbias_slave], [abias], [abias_slave], [magCalibration], [magScale], [mbias] ] - all sensors settings.   
    def getAllSettings(self):
        
        data = [
            time.time(),

            None if self.address_mpu_master is None else str(hex(self.address_mpu_master)),
            None if self.address_mpu_slave is None else str(hex(self.address_mpu_slave)),
            None if self.address_ak is None else str(hex(self.address_ak)),

            self.getGyroscoleFullScaleLabel(),
            self.getAccelerometerFullScaleLabel(),
            self.getMagnetometerFullScaleLabel(),

            self.gres,
            self.ares,
            self.mres
        ] + self.gbias + self.gbias_slave + self.abias + self.abias_slave + self.magCalibration + self.magScale + self.mbias
        
        return data

    # Get array with labels for settings obtained from getAllSettings.
    #  @param [in] self - The object pointer.
    #  @retval labels.
    def getAllSettingsLabels(self):
        
        return [
            "timestamp",

            "address_mpu_master", 
            "address_mpu_slave", 
            "address_ak", 

            "gyroscope_full_scale",
            "accelerometer_full_scale",
            "magnetometer_full_scale",

            "gyroscope_resolution",
            "accelerometer_resolution",
            "magnetometer_resolution",

            "gyroscope_master_bias_x",
            "gyroscope_master_bias_y",
            "gyroscope_master_bias_z",

            "gyroscope_slave_bias_x",
            "gyroscope_slave_bias_y",
            "gyroscope_slave_bias_z",

            "accelerometer_master_bias_x",
            "accelerometer_master_bias_y",
            "accelerometer_master_bias_z",

            "accelerometer_slave_bias_x",
            "accelerometer_slave_bias_y",
            "accelerometer_slave_bias_z",

            "magnetometer_factory_sensitivity_x",
            "magnetometer_factory_sensitivity_y",
            "magnetometer_factory_sensitivity_z",

            "magnetometer_soft_iron_distortion_x",
            "magnetometer_soft_iron_distortion_y",
            "magnetometer_soft_iron_distortion_z",

            "magnetometer_hard_iron_distortion_x",
            "magnetometer_hard_iron_distortion_y",
            "magnetometer_hard_iron_distortion_z"
        ]

    # Get label for gyroscope full scale value.
    #  @param [in] self - The object pointer.
    #  @retval label.
    def getGyroscoleFullScaleLabel(self):

        if self.gfs == GFS_250:
            return "GFS_250"
        elif self.gfs == GFS_500:
            return "GFS_500"
        elif self.gfs == GFS_1000:
            return "GFS_1000"
        elif self.gfs == GFS_2000:
            return "GFS_2000"
        else:
            return None

    # Get label for accelerometer full scale value.
    #  @param [in] self - The object pointer.
    #  @retval label.
    def getAccelerometerFullScaleLabel(self):

        if self.afs == AFS_2G:
            return "AFS_2G"
        elif self.afs == AFS_4G:
            return "AFS_4G"
        elif self.afs == AFS_8G:
            return "AFS_8G"
        elif self.afs == AFS_16G:
            return "AFS_16G"
        else:
            return None

    # Get label for magnetometer full scale value.
    #  @param [in] self - The object pointer.
    #  @retval label.
    def getMagnetometerFullScaleLabel(self):

        if self.mfs == AK8963_BIT_14:
            return "AK8963_BIT_14"
        elif self.mfs == AK8963_BIT_16:
            return "AK8963_BIT_16"
        else:
            return None

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
