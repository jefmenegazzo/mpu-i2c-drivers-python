# MPU-9250 (MPU-6500 + AK8963) I2C Driver in Python

**MPU-9250** is a multi-chip module (MCM) consisting of two dies integrated into a single QFN package. One die the **MPU-6050** houses the 3-Axis gyroscope, the 3-Axis accelerometer and  temperature sensor. The other die houses the **AK8963** 3-Axis magnetometer. Hence, the MPU-9250 is a 9-axis MotionTracking device that combines a 3-axis gyroscope, 3-axis accelerometer, 3-axis magnetometer and a Digital Motion Processor™ (DMP).

<br />
<img 
src="https://gloimg.gbtcdn.com/soa/gb/2015/201509/goods_img_big-v1/1442961797146-P-3106869.jpg"
alt="MPU-9250"
height="150"
align="center"
/>
<br />

## How To Use

With I2C Bus, you can use the MPU-9250 in two ways: simple mode or master-slave mode.

### Simple Mode (Master Only Mode)

In this mode, the MPU-9250 connects directly to Raspberry GPIOs. There are two physical addresses available for the MPU-9250, being 0x68 and 0x69. Therefore, on each I2C Bus you can have up to two MPU-9250 connected. The connection between GPIOs and MPU-9250 is as follows:

| MPU9250  | Raspberry  | Note |
|---|---|---|
| VDD  | 3.3V  | On some models of the MPU-9250 5V can be used.  |
| AD0  | 3.3V  | If used, the MPU-9250's address is changed to 0x69. Otherwise, the address is 0x68.  |
| GND  |  GND |   |
| SDA  |  SDA |   |
| SCL  |  SCL |   |

Below simple code to test the execution with never ending loop:

```python
import time
from registers import *
from mpu_9250 import MPU9250

mpu = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_69, # In 0x69 Address
    address_mpu_slave=None, 
    bus=1, 
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

mpu.configure() # Apply the settings to the registers.

while True:

    print("|.....MPU9250 in 0x69 Address.....|")
    print("Accelerometer", mpu.readAccelerometerMaster())
    print("Gyroscope", mpu.readGyroscopeMaster())
    print("Magnetometer", mpu.readMagnetometerMaster())
    print("Temperature", mpu.readTemperatureMaster())
    print("\n")

    time.sleep(1)
```

### Master-Slave Mode

If you want to have more than two MPU-9250 on one I2C Bus, you must use Master-Slave mode. In this case, first configure the MPU-9250 according to the previous section, they will be used as Master. To configure the MPU-9250 Slaves, connect as follows:

| MPU9250 Slave | MPU9250 Master | Raspberry PI | Note |
|---|---|---|---|
| VDD  | | 3.3V  | On some models of the MPU-9250 5V can be used.  |
| AD0  | | 3.3V  | If used, the MPU-9250's address is changed to 0x69. Otherwise, the address is 0x68.  |
| GND  | | GND |   |
| SDA  |  EDA |   |
| SCL  |  ECL |   |

This way you will have an MPU-9250 Master connecting SDA and SLC directly to the GPIO in Raspberry PI, and an MPU-9250 Slave connecting SDA and SLC to the EDA and ELC in MPU-9250 Master.

Below simple code to test the execution with never ending loop:

```python
import time
from registers import *
from mpu_9250 import MPU9250

mpu = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68, # Master has 0x68 Address
    address_mpu_slave=MPU9050_ADDRESS_68, # Slave has 0x68 Address
    bus=1, 
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

mpu.configure() # Apply the settings to the registers.

while True:
   
    print("|.....MPU9250 in 0x68 I2C Bus - Master.....|")
    print("Accelerometer", mpu.readAccelerometerMaster())
    print("Gyroscope", mpu.readGyroscopeMaster())
    print("Magnetometer", mpu.readMagnetometerMaster())
    print("Temperature", mpu.readTemperatureMaster())
    print("\n")

    print("|.....MPU9250 in 0x68 I2C Bus - Slave in 0x68 auxiliary sensor address.....|")
    print("Accelerometer", mpu.readAccelerometerSlave())
    print("Gyroscope", mpu.readGyroscopeSlave())
    print("Temperature", mpu.readTemperatureSlave())
    print("\n")

    time.sleep(1)
```

## Getting Data

All sensors and measurement units of the MPU-9250 are described below:

| Sensor  | Unit |
|---|---|
| Accelerometer | g (1g = 9.80665 m/s²) |
| Gyroscope | degrees per second (°/s) |
| Magnetometer | microtesla (μT) |
| Temperature | celsius degrees (°C) |

Before read the sensor data, make sure that you have executed the command:

```python
    mpu.configure() # Apply the settings to the registers.
```

### Reading Accelerometer

The accelerometer measures acceleration in three axes (X, Y, Z). To read your data, use the commands:

```python
    masterData = mpu.readAccelerometerMaster()
    slaveData = mpu.readAccelerometerSlave() # If there is a slave
```

### Reading Gyroscope

The gyroscope measures rotation rate in three axes (X, Y, Z). To read your data, use the commands:

```python
    masterData = mpu.readGyroscopeMaster()
    slaveData = mpu.readGyroscopeSlave() # If there is a slave
```

### Reading Magnetometer

The magnetometer measures geomagnetic field in three axes (X, Y, Z). To read your data, use the command:

```python
    masterData = mpu.readMagnetometerMaster()
```

When used in Simple Mode (Master Only Mode), the magnetometer will be available on the I2C Bus with address 0x0C. When in Master-Slave Mode, the magnetometer will also behave as a slave, and address 0x0C will not appear on the I2C Bus, acting as an auxiliary sensor.

### Reading Temperature

The temperature sensor measures data in Celsius degrees. To read your data, use the command:

```python
    masterData = mpu.readTemperatureMaster()
    slaveData = mpu.readTemperatureSlave() # If there is a slave
```

### Reading All Data

If you want to read data from all sensors (master and slave) at the same time, use the commands below (useful for saving to csv):

```python
    labels = mpu.getAllDataLabels() # return labels with data description for each array position
    data = mpu.getAllData() # returns a array with data from all sensors
```

## Calibrating Sensors

This library has functions ready for calibration accelerometer, gyroscope and magnetometer sensors. To calibrate all sensors at once, use the command:

```python
    mpu.calibrate() # Calibrate sensors
    mpu.configure() # The calibration function resets the sensors, so you need to reconfigure them
```

### Accelerometer and Gyroscope

To calibrate the accelerometer and gyroscope sensors, make sure that the sensors remain fixed and stationary. Align the accelerometer's Z axis with gravity, i.e., gravity (1g) should only appear on the sensor's Z axis (place the sensor in a flat place). To perform calibration run the command:

```python
    mpu.calibrateMPU6050() # Calibrate sensors
    mpu.configure() # The calibration function resets the sensors, so you need to reconfigure them

    abias = mpu.abias # Get the master accelerometer biases
    abias_slave = mpu.abias_slave # Get the slave accelerometer biases
    gbias = mpu.gbias # Get the master gyroscope biases
    gbias_slave = mpu.gbias_slave # Get the slave gyroscope biases
```

The biases are programmatically applied to the sensor data. Therefore, when reading the sensor data, the biases will be applied internally, returning corrected data. If you have calculated the biases of these sensors once, and want the controller to use them, simply parameterize as follows:

```python
    mpu.abias = [0, 0, 0] # Set the master accelerometer biases
    mpu.abias_slave = [0, 0, 0] # Set the slave accelerometer biases
    mpu.gbias = [0, 0, 0] # Set the master gyroscope biases
    mpu.gbias_slave = [0, 0, 0] # Set the slave gyroscope biases
```

### Magnetometer

To perform calibration run the command:

```python
    mpu.configureAK8963() # Calibrate sensors
    mpu.configure() # The calibration function resets the sensors, so you need to reconfigure them

    magScale = mpu.magScale # Get magnetometer soft iron distortion
    mbias = mpu.mbias # Get magnetometer hard iron distortion
```

If you have calculated the biases of these sensor once, and want the controller to use them, simply parameterize as follows:

```python
    mpu.magScale = [0, 0, 0] # Set magnetometer soft iron distortion
    mpu.mbias = [0, 0, 0] # Set magnetometer hard iron distortion
```

## Reset Registers

If you want to reset the values in all registers of all sensors in all MPU-9250, execute the command below:

```python
    mpu.reset() # Reset sensors
    mpu.configure() # After resetting you need to reconfigure the sensors
```

## Final Notes

The **mpu_9250.py** and **registers.py** files consist of the high level library. The folder **example**, and **__init__.py**, **sampling.py** and **sensors.py** files contain execution examples.

## License

The MIT License (MIT). Please see [License File](LICENSE.txt) for more information.