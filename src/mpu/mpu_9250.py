"""
https://github.com/nickcoutsos/MPU-6050-Python/blob/master/MPU6050.py
https://github.com/Tijndagamer/mpu6050/blob/master/mpu6050/mpu6050.py
https://github.com/FaBoPlatform/FaBo9AXIS-MPU9250-Python/blob/master/FaBo9Axis_MPU9250/MPU9250.py
"""

import smbus, time
from registers import *

class MPU9250:

    # Settings
    address_ak = None
    address_mpu_master = None
    address_mpu_slave = None
    bus = None

    # Sensor Resolution
    gres = None # Gyroscope
    ares = None # Accelerometer
    mres = None # Magnetometer

    # Magnometer Sensitivity
    magXcoef = None
    magYcoef = None
    magZcoef = None

    # Constructor
    # @param [in] self - The object pointer.
    # @param [in] address_mpu_master - MPU-9250 I2C address.
    # @param [in] address_ak - AK8963 I2C slave address.
    # @param [in] address_mpu_slave - MPU-9250 I2C slave address.
    # @param [in] bus - I2C bus board (default:Board Revision 2[1]).
    def __init__(self, address_ak, address_mpu_master, address_mpu_slave, bus=1):
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
            self.configureMPU6500(gfs, afs)
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

        # Reset all registers to default
        # self.bus.write_byte_data(self.address_mpu_master, PWR_MGMT_1, 0x80)
        # time.sleep(0.1)

        # sleep off
        self.bus.write_byte_data(self.address_mpu_master, PWR_MGMT_1, 0x00)
        time.sleep(0.1)

        # auto select clock source
        self.bus.write_byte_data(self.address_mpu_master, PWR_MGMT_1, 0x01)
        time.sleep(0.1)

        # DLPF_CFG
        # self.bus.write_byte_data(self.address_mpu_master, CONFIG, 0x00)
        self.bus.write_byte_data(self.address_mpu_master, CONFIG, 0x03)

        # sample rate divider
        self.bus.write_byte_data(self.address_mpu_master, SMPLRT_DIV, 0x04)

        # gyro full scale select
        self.bus.write_byte_data(self.address_mpu_master, GYRO_CONFIG, gfs << 3)

        # accel full scale select
        self.bus.write_byte_data(self.address_mpu_master, ACCEL_CONFIG, afs << 3)

        # A_DLPFCFG
        # self.bus.write_byte_data(self.address_mpu_master, ACCEL_CONFIG_2, 0x00)
        self.bus.write_byte_data(self.address_mpu_master, ACCEL_CONFIG_2, 0x03)

        if self.address_mpu_slave is None:

            # BYPASS_EN enable
            self.bus.write_byte_data(self.address_mpu_master, INT_PIN_CFG, 0x02)
            time.sleep(0.1)   

            # Disable master
            self.bus.write_byte_data(self.address_mpu_master, USER_CTRL, 0x00)
            time.sleep(0.1) 
      
        else:

            # BYPASS_EN disabled
            self.bus.write_byte_data(self.address_mpu_master, INT_PIN_CFG, 0x00)
            time.sleep(0.1)           

            # Enable Master
            self.bus.write_byte_data(self.address_mpu_master, USER_CTRL, 0x20)
            time.sleep(0.1)  
            
            # Address to write MPU Slave
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_ADDR, self.address_mpu_slave)

            # # Reset all registers to default
            # self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, PWR_MGMT_1)
            # self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_DO, 0x80)
            # self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)
            # time.sleep(0.1)

            # sleep off
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, PWR_MGMT_1)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_DO, 0x00)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)
            time.sleep(0.1)

            # auto select clock source
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, PWR_MGMT_1)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_DO, 0x01)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)
            time.sleep(0.1)

            # DLPF_CFG
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, CONFIG)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_DO, 0x00)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)

            # DLPF_CFG
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, SMPLRT_DIV)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_DO, 0x04)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)

            # gyro full scale select
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, GYRO_CONFIG)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_DO, gfs << 3)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)

            # gyro full scale select
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, ACCEL_CONFIG)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_DO, afs << 3)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)

            # A_DLPFCFG
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, ACCEL_CONFIG_2)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_DO, 0x00)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)

            # BYPASS_EN enable
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, INT_PIN_CFG)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_DO, 0x02)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)
            time.sleep(0.1)

            # Disable master
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, USER_CTRL)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_DO, 0x00)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)
            time.sleep(0.1)
  
            # Address to read from MPU Slave
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV0_ADDR, self.address_mpu_slave | 0x80) # 0xE8
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV0_REG, ACCEL_OUT)  
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV0_CTRL, 0x8E) # read 14 bytes       
                       
    # Configure AK8963
    # @param [in] self - The object pointer.
    # @param [in] mfs - Magneto scale select.
    # @param [in] mode - Magnetometer mode select.
    def configureAK8963(self, mfs, mode):

        if mfs == AK8963_BIT_14:
            self.mres = MAGNOMETER_SCALE_MODIFIER_BIT_14
        elif mfs == AK8963_BIT_16:
            self.mres = MAGNOMETER_SCALE_MODIFIER_BIT_16
        else:
            raise Exception('Magnetometer scale modifier not found.')

        if self.address_mpu_slave is None:
            
            # set power down mode
            self.bus.write_byte_data(self.address_ak, AK8963_CNTL1, 0x00)
            time.sleep(0.1)

            # set read FuseROM mode
            self.bus.write_byte_data(self.address_ak, AK8963_CNTL1, 0x0F)
            time.sleep(0.1)

            # read coef data
            data = self.bus.read_i2c_block_data(self.address_ak, AK8963_ASAX, 3)

            self.magXcoef = (data[0] - 128) / 256.0 + 1.0
            self.magYcoef = (data[1] - 128) / 256.0 + 1.0
            self.magZcoef = (data[2] - 128) / 256.0 + 1.0

            # set power down mode
            self.bus.write_byte_data(self.address_ak, AK8963_CNTL1, 0x00)
            time.sleep(0.1)

            # set scale and continous mode
            self.bus.write_byte_data(self.address_ak, AK8963_CNTL1, (mfs << 4 | mode))
            time.sleep(0.1)
        
        else:

            # Address to write MPU Slave
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_ADDR, self.address_ak)  

            # set power down mode
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, AK8963_CNTL1)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_DO, 0x00)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)
            time.sleep(0.1)

            # set read FuseROM mode
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, AK8963_CNTL1)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_DO, 0x0F)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)
            time.sleep(0.1)

            # Address to read MPU Slave
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_ADDR, (self.address_ak | 0x80))

            data = []

            # Read sensitivity X
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, AK8963_ASAX)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)
            data.append(self.bus.read_byte_data(self.address_mpu_master, I2C_SLV4_DI))
        
            # Read sensitivity Y
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, AK8963_ASAY)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)
            data.append(self.bus.read_byte_data(self.address_mpu_master, I2C_SLV4_DI))

            # Read sensitivity Z
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, AK8963_ASAZ)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)
            data.append(self.bus.read_byte_data(self.address_mpu_master, I2C_SLV4_DI))

            self.magXcoef = (data[0] - 128) / 256.0 + 1.0
            self.magYcoef = (data[1] - 128) / 256.0 + 1.0
            self.magZcoef = (data[2] - 128) / 256.0 + 1.0

            # Address to write MPU Slave
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_ADDR, self.address_ak)

            # set power down mode
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, AK8963_CNTL1)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_DO, 0x00)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)
            time.sleep(0.1)

            # set scale and continous mode
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_REG, AK8963_CNTL1)
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_DO, (mfs << 4 | mode))
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV4_CTRL, 0x80)
            time.sleep(0.1)

            # Address to read from MPU Slave
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV1_ADDR, (self.address_ak | 0x80))
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV1_REG, AK8963_MAGNET_OUT)  
            self.bus.write_byte_data(self.address_mpu_master, I2C_SLV1_CTRL, 0x87)  # read 7 bytes
        
    # Read accelerometer
    #  @param [in] self - The object pointer.
    #  @retval x - x-axis data
    #  @retval y - y-axis data
    #  @retval z - z-axis data
    def readAccelerometerMaster(self):
        data = self.bus.read_i2c_block_data(self.address_mpu_master, ACCEL_OUT, 6)
        return self.convertAccelerometer(data)

    def readAccelerometerSlave(self):

        if self.address_mpu_slave is None:
            return self.getDataError()

        else:   
            data = self.bus.read_i2c_block_data(self.address_mpu_master, EXT_SENS_DATA_00, 6)
            return self.convertAccelerometer(data)
            
    def convertAccelerometer(self, data):
        
        x = self.dataConv(data[1], data[0]) * self.ares * GRAVITY
        y = self.dataConv(data[3], data[2]) * self.ares * GRAVITY
        z = self.dataConv(data[5], data[4]) * self.ares * GRAVITY

        return {"x": x, "y": y, "z": z}
        
    # Read gyroscope
    #  @param [in] self - The object pointer.
    #  @retval x - x-gyro data
    #  @retval y - y-gyro data
    #  @retval z - z-gyro data
    def readGyroscopeMaster(self):
        data = self.bus.read_i2c_block_data(self.address_mpu_master, GYRO_OUT, 6)
        return self.convertGyroscope(data)

    def readGyroscopeSlave(self):

        if self.address_mpu_slave is None:
            return self.getDataError()

        else:   
            data = self.bus.read_i2c_block_data(self.address_mpu_master, EXT_SENS_DATA_08, 6)
            return self.convertGyroscope(data)
                
    def convertGyroscope(self, data):
        
        x = self.dataConv(data[1], data[0]) * self.gres
        y = self.dataConv(data[3], data[2]) * self.gres
        z = self.dataConv(data[5], data[4]) * self.gres

        return {"x": x, "y": y, "z": z}

    # Read magnetometer
    #  @param [in] self - The object pointer.
    #  @retval x - X-magneto data
    #  @retval y - y-magneto data
    #  @retval z - Z-magneto data
    def readMagnetometerMaster(self):

        data = None

        if self.address_mpu_slave is None:
            data = self.bus.read_i2c_block_data(self.address_ak, AK8963_MAGNET_OUT, 7)

        else:   
            data = self.bus.read_i2c_block_data(self.address_mpu_master, EXT_SENS_DATA_14, 7)          

        return self.convertMagnetometer(data)

    def readMagnetometerSlave(self):
        return self.getDataError()
    
    def convertMagnetometer(self, data):

        x = 0
        y = 0
        z = 0

        # check overflow
        if (data[6] & 0x08) != 0x08:
            x = self.dataConv(data[0], data[1]) * self.mres * self.magXcoef
            y = self.dataConv(data[2], data[3]) * self.mres * self.magYcoef
            z = self.dataConv(data[4], data[5]) * self.mres * self.magZcoef

        return {"x": x, "y": y, "z": z}

    # Read temperature
    #  @param [in] self - The object pointer.
    #  @retval temperature - temperature(degrees C)
    def readTemperatureMaster(self):
        data = self.bus.read_i2c_block_data(self.address_mpu_master, TEMP_OUT, 2)
        return self.convertTemperature(data) 
        
    def readTemperatureSlave(self):
        data = self.bus.read_i2c_block_data(self.address_mpu_master, EXT_SENS_DATA_06, 2)
        return self.convertTemperature(data)

    def convertTemperature(self, data):
        temp = self.dataConv(data[1], data[0])
        temp = (temp / 333.87 + 21.0)
        return temp

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
        who_am_i = self.bus.read_byte_data(self.address_mpu_master, WHO_AM_I)
        return who_am_i == DEVICE_ID

    #  Check MPU data ready
    #  @param [in] self: The object pointer.
    #  @retval true: data is ready
    #  @retval false: data is not ready
    def checkMPUDataReady(self):
        drdy = self.bus.read_byte_data(self.address_mpu_master, INT_STATUS)
        return drdy & 0x01

    #  Check AK data ready
    #  @param [in] self: The object pointer.
    #  @retval true: data is ready
    #  @retval false: data is not ready
    def checkAKDataReady(self):
        drdy = self.bus.read_byte_data(self.address_ak, AK8963_ST1)
        return drdy & 0x01

    def getDataError(self):
        return {"x": 0, "y": 0, "z": 0}
