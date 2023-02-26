<div align="center">

<a href="https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect">
<img 
src="https://gloimg.gbtcdn.com/soa/gb/2015/201509/goods_img_big-v1/1442961797146-P-3106869.jpg"
alt="MPU-9250"
height="150"
align="center"
/>
</a>

<br />

🙌 Use [donations](#Sponsors-and-Donations) to help support your projects! 🙌

</div>

<br />

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://img.shields.io/badge/Project_Status-Active-green?style=flat-square&color=success)](https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=flat-square&color=success)](https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg?style=flat-square&color=success)](LICENSE.txt)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=QYV4NEUSVWZCY&source=url)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect?style=flat-square) 
![pypi](https://img.shields.io/pypi/v/pybadges.svg?style=flat-square)
![versions](https://img.shields.io/pypi/pyversions/pybadges.svg?style=flat-square)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.3960441-blue?style=flat-square)](https://doi.org/10.5281/zenodo.3960441)
[![GitHub issues](https://img.shields.io/github/issues/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect?style=flat-square)](https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect/issues)
[![GitHub forks](https://img.shields.io/github/forks/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect?style=flat-square)](https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect/network/members)
[![GitHub stars](https://img.shields.io/github/stars/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect?style=flat-square)](https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect/stargazers)
[![GitHub watchers](https://img.shields.io/github/watchers/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect?style=flat-square)](https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect/watchers)
[![GitHub contributors](https://img.shields.io/github/contributors/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect?style=flat-square&color=success)](https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect/graphs/contributors/)
[![HitCount](http://hits.dwyl.io/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect/badges.svg)](https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/mpu9250_jmdev?style=flat-square&color=success)](https://pypi.org/project/mpu9250_jmdev)

# MPU-9250 (MPU-6500 + AK8963) I2C Driver in Python

**MPU-9250** is a multi-chip module (MCM) consisting of two dies integrated into a single QFN package. One die the **MPU-6500** houses the 3-Axis gyroscope, the 3-Axis accelerometer and  temperature sensor. The other die houses the **AK8963** 3-Axis magnetometer. Hence, the MPU-9250 is a 9-axis MotionTracking device that combines a 3-axis gyroscope, 3-axis accelerometer, 3-axis magnetometer and a Digital Motion Processor™ (DMP). The hardware documentation for MPU-9250 can be found at [Product Specification](https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect/blob/master/doc/MPU-9250%20Product%20Specification%20Revision%201.1.pdf) and [Register Map and Descriptions](https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect/blob/master/doc/MPU-9250%20Register%20Map%20and%20Descriptions%20Revision%201.6.pdf).

## Table of Contents
- [Instalation](#Instalation)
- [How To Use](#How-To-Use)
- [Getting Data](#Getting-Data)
- [Calibrating Sensors](#Calibrating-Sensors)
- [Reset Registers](#Reset-Registers)
- [Final Notes](#Final-Notes)
- [Sponsors and Donations](#Sponsors-and-Donations)
- [What We're Working on Now](#What-We're-Working-on-Now)
- [How To Cite](#How-To-Cite)
- [License](#License)

## Instalation

To install via pip use:

```bash
pip install mpu9250-jmdev
```

To use the package for development purposes use:

```bash
git clone https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect.git MPU9250
cd MPU9250
pip install -e .
pip install -r requirements.txt
```

### Known Issues

> :information_source: Notice that this package requires Python 3.6 or higher.

> :warning: If you have both Python 2 and 3 installed on your machine, use ```pip3``` to install and ```python3``` to run instead. 

> :warning: If you run your python source-code with ```sudo```, remember to use ```sudo``` with ```pip install``` commands as well.

> :warning: If you get zero values and the message **Using Fake SMBus**, the **smbus2** requirement has not been installed correctly. Try installing manually with the command ```pip install -r requirements.txt``` or ```python -mpip install smbus2```.

> :exclamation: Any other problem or questions, **open an issue in this repository [clicking here](https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect/issues), do not send me an e-mail!**

## How To Use

With I2C Bus, you can use the MPU-9250 in two ways: simple mode or advanced mode. The example source-codes are in **examples** folder.

### Simple Mode - Master Only

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
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

mpu = MPU9250(
    address_ak=AK8963_ADDRESS, 
    address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
    address_mpu_slave=None, 
    bus=1,
    gfs=GFS_1000, 
    afs=AFS_8G, 
    mfs=AK8963_BIT_16, 
    mode=AK8963_MODE_C100HZ)

mpu.configure() # Apply the settings to the registers.

while True:

    print("|.....MPU9250 in 0x68 Address.....|")
    print("Accelerometer", mpu.readAccelerometerMaster())
    print("Gyroscope", mpu.readGyroscopeMaster())
    print("Magnetometer", mpu.readMagnetometerMaster())
    print("Temperature", mpu.readTemperatureMaster())
    print("\n")

    time.sleep(1)
```

### Advanced Mode - Master-Slave

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
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

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

When used in Simple Mode (Master Only), the magnetometer will be available on the I2C Bus with address 0x0C. When in Advanced Mode (Master-Slave), the magnetometer will also behave as a slave, and address 0x0C will not appear on the I2C Bus, acting as an auxiliary sensor.

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

### Reading All Settings

If you want to read settings (biases, resolutions, scale factors) from all sensors (master and slave) at the same time, use the commands below (useful for saving to csv):

```python
    labels = mpu.getAllSettingsLabels() # return labels with settings description for each array position
    data = mpu.getAllSettings() # returns a array with settings from all sensors
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
    mpu.calibrateMPU6500() # Calibrate sensors
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
    mpu.calibrateAK8963() # Calibrate sensors
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

The folder **mpu9250** consist of the high level library. The folder **examples** contains files with basic execution and threaded examples.

## Sponsors and Donations

This project does not have any funding. To help maintain the project, consider making a donation 🙌.

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=QYV4NEUSVWZCY&source=url)

## What We're Working on Now 

New features are currently under development:
- V2: new major version will be released soon, much more robust than the current one. It will supports several MPU models, such as 9250, 9150, 6050, 6500.
- Complete support documentation for configuring RPi, I2C, VNC, SSH, etc.

## How To Cite

To cite this repository, use the reference below:

```bibtex
@software{menegazzo3960441,
    author = {Jeferson Menegazzo and Aldo von Wangenheim},
    title = {{MPU-9250 Sensors Data Collect}},
    month = jul,
    year = 2020,
    publisher = {Zenodo},
    version = {1.0.12},
    doi = {10.5281/zenodo.3960441},
    url = {https://github.com/Intelligent-Vehicle-Perception/MPU-9250-Sensors-Data-Collect/}
}
```

## License

This project is under Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND 4.0). Please see [License File](LICENSE.txt) for more information.
