# MPU-9250 (MPU-6500 + AK8963) I2C Driver in Python

**MPU-9250** is a multi-chip module (MCM) consisting of two dies integrated into a single QFN package. One die the **MPU-6050** houses the 3-Axis gyroscope, the 3-Axis accelerometer and  temperature sensor. The other die houses the **AK8963** 3-Axis magnetometer. Hence, the MPU-9250 is a 9-axis MotionTracking device that combines a 3-axis gyroscope, 3-axis accelerometer, 3-axis magnetometer and a Digital Motion Processor™ (DMP).

<br />
<img 
src="https://gloimg.gbtcdn.com/soa/gb/2015/201509/goods_img_big-v1/1442961797146-P-3106869.jpg"
alt="MPU-9250"
height="150"
/>
<br />

## How To Use

With I2C bus, you can use the MPU-9250 in two ways: simple mode or master-slave mode.

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

mpu_0x68 = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    address_mpu_slave=None, 
    bus=1, 
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

mpu_0x68.configure()

mpu_0x69 = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_69, # In 0x69 Address
    address_mpu_slave=None, 
    bus=1, 
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

mpu_0x69.configure()

while True:
   
    print("MPU9250 in 0x68 address")
    print(mpu_0x68.readAccelerometerMaster())
    print(mpu_0x68.readGyroscopeMaster())
    print(mpu_0x68.readMagnetometerMaster())
    print(mpu_0x68.readTemperatureMaster())

    print("MPU9250 in 0x69 address")
    print(mpu_0x69.readAccelerometerMaster())
    print(mpu_0x69.readGyroscopeMaster())
    print(mpu_0x69.readMagnetometerMaster())
    print(mpu_0x69.readTemperatureMaster())

    time.sleep(1000)
```

### Master-Slave Mode

If you want to have more than two MPU-9250 on one I2C Bus, you must use Master-Slave mode. In this case, first configure the MPU-9250 according to the previous section, they will be used as Master. To configure the MPU-9250 slaves, connect as follows:

| MPU9250 Slave | MPU9250 Master | Raspberry  | Note |
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

mpu_0x68 = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68, # Master has 0x68 Address
    address_mpu_slave=MPU9050_ADDRESS_68, # Slave has 0x68 Address
    bus=1, 
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

mpu_0x68.configure()

mpu_0x69 = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_69, # Master has 0x69 Address
    address_mpu_slave=None, # This MPU-9250 don't have a slave
    bus=1, 
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

mpu_0x69.configure()

while True:
   
    print("MPU9250 in 0x68 I2C Bus - Master")
    print(mpu_0x68.readAccelerometerMaster())
    print(mpu_0x68.readGyroscopeMaster())
    print(mpu_0x68.readMagnetometerMaster())
    print(mpu_0x68.readTemperatureMaster())

    print("MPU9250 in 0x68 I2C Bus - Slave in 0x68 auxiliary sensor address")
    print(mpu_0x68.readAccelerometerSlave())
    print(mpu_0x68.readGyroscopeSlave())
    print(mpu_0x68.readTemperatureSlave())

    print("MPU9250 in 0x69 address - Only Master")
    print(mpu_0x69.readAccelerometerMaster())
    print(mpu_0x69.readGyroscopeMaster())
    print(mpu_0x69.readMagnetometerMaster())
    print(mpu_0x69.readTemperatureMaster())

    time.sleep(1000)
```

## Getting Data

All sensors and measurement units of the MPU-9250 are described below:

| Sensor  | Unit |
|---|---|
| Accelerometer | g (1g = 9.80665 m/s²) |
| Gyroscope | degrees per second (°/s) |
| Magnetometer | microtesla (μT) |
| Temperature | celsius degrees (°C) |


### Reading Accelerometer

TODO

### Reading Gyroscope

TODO

### Reading Magnetometer

TODO

### Reading Temperature

TODO

### Reading All Data

TODO

## Calibrating Sensors

TODO

### Accelerometer and Gyroscope

TODO

### Magnetometer

TODO

## Reset Registers

TODO

## Final Notes

The **mpu_9250.py** and **registers.py** files consist of the high level library. The **__init__.py**, **sampling.py** and **sensors.py** files contain execution examples.