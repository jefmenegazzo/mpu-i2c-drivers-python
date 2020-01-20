#####################################################################
# Author: Jeferson Menegazzo                                        #
# Year: 2020                                                        #
# License: MIT                                                      #
#####################################################################

###########################################################
# Register Map for Gyroscope and Accelerometer - MPU 9250
###########################################################

# Gyroscope Self-Test Registers
SELF_TEST_X_GYRO = 0x00
SELF_TEST_Y_GYRO = 0x01
SELF_TEST_Z_GYRO = 0x02

# Accelerometer Self-Test Registers
SELF_TEST_X_ACCEL = 0x0D
SELF_TEST_Y_ACCEL = 0x0E
SELF_TEST_Z_ACCEL = 0x0F

# Gyro Offset Registers
XG_OFFSET_H = 0x13
XG_OFFSET_L = 0x14
YG_OFFSET_H = 0x15
YG_OFFSET_L = 0x16
ZG_OFFSET_H = 0x17
ZG_OFFSET_L = 0x18

# Accelerometer Offset Registers
XA_OFFSET_H = 0x77
XA_OFFSET_L = 0x78
YA_OFFSET_H = 0x7A
YA_OFFSET_L = 0x7B
ZA_OFFSET_H = 0x7D
ZA_OFFSET_L = 0x7E

# Sample Rate Divider
SMPLRT_DIV = 0x19

# Configuration
CONFIG = 0x1A

# Gyroscope Configuration
GYRO_CONFIG = 0x1B

# Accelerometer Configuration
ACCEL_CONFIG = 0x1C

# Accelerometer Configuration 2
ACCEL_CONFIG_2 = 0x1D

# Low Power Accelerometer ODR Control
LP_ACCEL_ODR = 0x1E

# Wake-on Motion Threshold
WOM_THR = 0x1F

# FIFO Enable
FIFO_EN = 0x23

# I2C Master Control
I2C_MST_CTRL = 0x24

# I2C Slave 0 Control
I2C_SLV0_ADDR = 0x25
I2C_SLV0_REG = 0x26
I2C_SLV0_DO = 0x63
I2C_SLV0_CTRL = 0x27

# I2C Slave 1 Control
I2C_SLV1_ADDR = 0x28
I2C_SLV1_REG = 0x29
I2C_SLV1_DO = 0x64
I2C_SLV1_CTRL = 0x2A

# I2C Slave 2 Control
I2C_SLV2_ADDR = 0x2B
I2C_SLV2_REG = 0x2C
I2C_SLV2_DO = 0x65
I2C_SLV2_CTRL = 0x2D

# I2C Slave 3 Control
I2C_SLV3_ADDR = 0x2E
I2C_SLV3_REG = 0x2F
I2C_SLV3_DO = 0x66
I2C_SLV3_CTRL = 0x30

# I2C Slave 4 Control
I2C_SLV4_ADDR = 0x31
I2C_SLV4_REG = 0x32
I2C_SLV4_DO = 0x33
I2C_SLV4_CTRL = 0x34
I2C_SLV4_DI = 0x35

# I2C Master Status
I2C_MST_STATUS = 0x36

# INT Pin / Bypass Enable Configuration
## BYPASS_EN[1]:
### When asserted, the i2c_master interface pins(ES_CL and ES_DA) will go into ‘bypass mode’ when the i2c master interface is disabled.
### The pins will float high due to the internal pull-up if not enabled and the i2c master interface is disabled.  
INT_PIN_CFG = 0x37

# Interrupt Enable
INT_ENABLE = 0x38

# Interrupt Status
INT_STATUS = 0x3A

# Accelerometer Measurements - High byte and low byte
ACCEL_XOUT_H = 0x3B
ACCEL_XOUT_L = 0x3C
ACCEL_YOUT_H = 0x3D
ACCEL_YOUT_L = 0x3E
ACCEL_ZOUT_H = 0x3F
ACCEL_ZOUT_L = 0x40

# Temperature Measurement
TEMP_OUT_H = 0x41
TEMP_OUT_L = 0x42

# Gyroscope Measurements - High byte and low byte
GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44
GYRO_YOUT_H = 0x45
GYRO_YOUT_L = 0x46
GYRO_ZOUT_H = 0x47
GYRO_ZOUT_L = 0x48

# External Sensor Data
EXT_SENS_DATA_00 = 0x49
EXT_SENS_DATA_01 = 0x4A
EXT_SENS_DATA_02 = 0x4B
EXT_SENS_DATA_03 = 0x4C
EXT_SENS_DATA_04 = 0x4D
EXT_SENS_DATA_05 = 0x4E
EXT_SENS_DATA_06 = 0x4F
EXT_SENS_DATA_07 = 0x50
EXT_SENS_DATA_08 = 0x51
EXT_SENS_DATA_09 = 0x52
EXT_SENS_DATA_10 = 0x53
EXT_SENS_DATA_11 = 0x54
EXT_SENS_DATA_12 = 0x55
EXT_SENS_DATA_13 = 0x56
EXT_SENS_DATA_14 = 0x57
EXT_SENS_DATA_15 = 0x58
EXT_SENS_DATA_16 = 0x59
EXT_SENS_DATA_17 = 0x5A
EXT_SENS_DATA_18 = 0x5B
EXT_SENS_DATA_19 = 0x5C
EXT_SENS_DATA_20 = 0x5D
EXT_SENS_DATA_21 = 0x5E
EXT_SENS_DATA_22 = 0x5F
EXT_SENS_DATA_23 = 0x60

# I2C Master Delay Control
I2C_MST_DELAY_CTRL = 0x67

# Signal Path Reset
SIGNAL_PATH_RESET = 0x68

# Accelerometer Interrupt Control
MOT_DETECT_CTRL = 0x69

# User Control
## I2C_MST_EN[5]: 
### 1 – Enable the I2C Master I/F module; pins ES_DA and ES_SCL are isolated from pins SDA/SDI and SCL/ SCLK.  
### 0 – Disable I2C Master I/F module; pins ES_DA and ES_SCL are logically driven by pins SDA/SDI and SCL/ SCLK.
USER_CTRL = 0x6A

# Power Management 1
PWR_MGMT_1 = 0x6B

# Power Management 2
PWR_MGMT_2 = 0x6C

# FIFO Count Registers
FIFO_COUNTH = 0x72
FIFO_COUNTL = 0x73

# FIFO Read Write
FIFO_R_W = 0x74

# Who Am I
WHO_AM_I = 0x75

# Gyro Full Scale Select
GFS_250 = 0x00  # 250dps
GFS_500 = 0x01  # 500dps
GFS_1000 = 0x02  # 1000dps
GFS_2000 = 0x03  # 2000dps

# Accel Full Scale Select
AFS_2G = 0x00  # 2G
AFS_4G = 0x01  # 4G
AFS_8G = 0x02  # 8G
AFS_16G = 0x03  # 16G

###########################################################
# Register Map for Magnetometer - AK8963
###########################################################

# Device ID
AK8963_WIA = 0x00

# Information
AK8963_INFO = 0x01

# Status 1
AK8963_ST1 = 0x02

# Measurement Data
AK8963_HXL = 0x03
AK8963_HXH = 0x04
AK8963_HYL = 0x05
AK8963_HYH = 0x06
AK8963_HZL = 0x07
AK8963_HZH = 0x08

# Status 2
AK8963_ST2 = 0x09

# Control 1
#AK8963_CNTL = 0x0A
AK8963_CNTL1 = 0x0A
# Control 2
# AK8963_RSV = 0x0B
AK8963_CNTL2 = 0x0B

# Self-Test Control
AK8963_ASTC = 0x0C

# Test 1, 2
AK8963_TS1 = 0x0D
AK8963_TS2 = 0x0E

# I2C Disable
AK8963_I2CDIS = 0x0F

# Sensitivity Adjustment values
AK8963_ASAX = 0x10
AK8963_ASAY = 0x11
AK8963_ASAZ = 0x12

# CNTL1 Mode select
# Power down mode
AK8963_MODE_DOWN = 0x00

# One shot data output
AK8963_MODE_ON = 0x01

# Magneto Scale Select
AK8963_BIT_14 = 0x00  # 14bit output
AK8963_BIT_16 = 0x01  # 16bit output

# Continous data output
AK8963_MODE_C8HZ = 0x02  # 8Hz
AK8963_MODE_C100HZ = 0x06  # 100Hz

###########################################################
# Others
###########################################################

FIRST_DATA_POSITION = ACCEL_XOUT_H
ACCEL_OUT = ACCEL_XOUT_H
GYRO_OUT = GYRO_XOUT_H
TEMP_OUT = TEMP_OUT_H
AK8963_MAGNET_OUT = AK8963_HXL

# Device ID
DEVICE_ID = 0x71

# Accelerometer Scale Modifiers
ACCEL_SCALE_MODIFIER_2G = 2.0/32768.0
ACCEL_SCALE_MODIFIER_4G = 4.0/32768.0
ACCEL_SCALE_MODIFIER_8G = 8.0/32768.0
ACCEL_SCALE_MODIFIER_16G = 16.0/32768.0

ACCEL_SCALE_MODIFIER_2G_DIV = 32768.0/2.0
ACCEL_SCALE_MODIFIER_4G_DIV = 32768.0/4.0
ACCEL_SCALE_MODIFIER_8G_DIV = 32768.0/8.0
ACCEL_SCALE_MODIFIER_16G_DIV = 32768.0/16.0

# Gyroscope Scale Modifiers
GYRO_SCALE_MODIFIER_250DEG = 250.0/32768.0
GYRO_SCALE_MODIFIER_500DEG = 500.0/32768.0
GYRO_SCALE_MODIFIER_1000DEG = 1000.0/32768.0
GYRO_SCALE_MODIFIER_2000DEG = 2000.0/32768.0

GYRO_SCALE_MODIFIER_250DEG_DIV = 32768.0/250.0
GYRO_SCALE_MODIFIER_500DEG_DIV = 32768.0/500.0
GYRO_SCALE_MODIFIER_1000DEG_DIV = 32768.0/1000.0
GYRO_SCALE_MODIFIER_2000DEG_DIV = 32768.0/2000.0

# Magnetometer Scale Modifiers
MAGNOMETER_SCALE_MODIFIER_BIT_14 = 4912.0/8190.0
MAGNOMETER_SCALE_MODIFIER_BIT_16 = 4912.0/32760.0

MAGNOMETER_SCALE_MODIFIER_BIT_14_DIV = 8190.0/4912.0
MAGNOMETER_SCALE_MODIFIER_BIT_16_DIV = 32760.0/4912.0

# Gravity
GRAVITY = 9.80665

# Default I2C Address
MPU9050_ADDRESS_68 = 0x68
MPU9050_ADDRESS_69 = 0x69
AK8963_ADDRESS = 0x0C