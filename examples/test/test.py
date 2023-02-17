#####################################################################
# Author: Jeferson Menegazzo                                        #
# Year: 2020                                                        #
# License: CC BY-NC-ND 4.0                                          #
#####################################################################

import sys
sys.path.append("")

import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250


a = MPU9250("smbus_fake")
a.print()