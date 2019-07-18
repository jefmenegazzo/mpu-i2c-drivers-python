# # Function which accumulates gyro and accelerometer data after device initialization. 
    # # It calculates the average of the at-rest readings and then loads the resulting offsets into accelerometer and gyro bias registers.
    # def calibrateAccGyro(self):

    #     # Reset all registers to default
    #     self.bus.write_byte_data(self.address_mpu_master, PWR_MGMT_1, 0x80)
    #     time.sleep(0.1)

    #     # get stable time source. Auto select clock source to be PLL gyroscope reference if ready
    #     # else use the internal oscillator, bits 2:0 = 001
    #     self.bus.write_byte_data(self.address_mpu_master, PWR_MGMT_1, 0x01)
    #     self.bus.write_byte_data(self.address_mpu_master, PWR_MGMT_2, 0x00)
    #     time.sleep(0.2)

    #     # Configure device for bias calculation
    #     self.bus.write_byte_data(self.address_mpu_master, INT_ENABLE, 0x00) # Disable all interrupts
    #     self.bus.write_byte_data(self.address_mpu_master, FIFO_EN, 0x00) # Disable FIFO
    #     self.bus.write_byte_data(self.address_mpu_master, PWR_MGMT_1, 0x00) # Turn on internal clock source
    #     self.bus.write_byte_data(self.address_mpu_master, I2C_MST_CTRL, 0x00) # Disable I2C master
    #     self.bus.write_byte_data(self.address_mpu_master, USER_CTRL, 0x00) # Disable FIFO and I2C master modes
    #     self.bus.write_byte_data(self.address_mpu_master, USER_CTRL, 0x0C) # Reset FIFO and DMP
    #     time.sleep(0.015)

    #     # Configure MPU6050 gyro and accelerometer for bias calculation
    #     self.bus.write_byte_data(self.address_mpu_master, CONFIG, 0x01) # Set low-pass filter to 188 Hz
    #     self.bus.write_byte_data(self.address_mpu_master, SMPLRT_DIV, 0x00) # Set sample rate to 1 kHz
    #     self.bus.write_byte_data(self.address_mpu_master, GYRO_CONFIG, 0x00) # Set gyro full-scale to 250 degrees per second, maximum sensitivity
    #     self.bus.write_byte_data(self.address_mpu_master, ACCEL_CONFIG, 0x00) # Set accelerometer full-scale to 2 g, maximum sensitivity

    #     gyrosensitivity = 131    # = 131 LSB/degrees/sec
    #     accelsensitivity = 16384 # = 16384 LSB/g

    #     # Configure FIFO to capture accelerometer and gyro data for bias calculation
    #     self.bus.write_byte_data(self.address_mpu_master, USER_CTRL, 0x40) # Enable FIFO
    #     self.bus.write_byte_data(self.address_mpu_master, FIFO_EN, 0x78) # Enable gyro and accelerometer sensors for FIFO  (max size 512 bytes in MPU-9150). Accumulate 40 samples in 40 milliseconds = 480 bytes
    #     time.sleep(0.04)

    #     # At end of sample accumulation, turn off FIFO sensor read
    #     self.bus.write_byte_data(self.address_mpu_master, FIFO_EN, 0x00) # Disable gyro and accelerometer sensors for FIFO
    #     data = self.bus.read_i2c_block_data(self.address_mpu_master, FIFO_COUNTH, 2) # read FIFO sample count
        
    #     fifo_count = self.combineBytes(data[0], data[1])
    #     packet_count = fifo_count / 12 # How many sets of full gyro and accelerometer data for averaging

    #     gyro_bias = [0, 0, 0]
    #     accel_bias = [0, 0, 0]

    #     for i in range(packet_count):
            
    #         data = self.bus.read_i2c_block_data(self.address_mpu_master, FIFO_R_W, 12) # read data for averaging
    
    #         accel_temp = [0, 0, 0]
    #         gyro_temp = [0, 0, 0]

    #         # Form signed 16-bit integer for each sample in FIFO
    #         accel_temp[0] = self.combineBytes(data[0], data[1])
    #         accel_temp[1] = self.combineBytes(data[2], data[3])
    #         accel_temp[2] = self.combineBytes(data[4], data[5])
    #         gyro_temp[0] = self.combineBytes(data[6], data[7])
    #         gyro_temp[1] = self.combineBytes(data[8], data[9])
    #         gyro_temp[2] = self.combineBytes(data[10], data[11])

    #         accel_bias[0] += accel_temp[0] # Sum individual signed 16-bit biases to get accumulated signed 32-bit biases
    #         accel_bias[1] += accel_temp[1]
    #         accel_bias[2] += accel_temp[2]
    #         gyro_bias[0] += gyro_temp[0]
    #         gyro_bias[1] += gyro_temp[1]
    #         gyro_bias[2] += gyro_temp[2]
    
    #     accel_bias[0] /= packet_count # Normalize sums to get average count biases
    #     accel_bias[1] /= packet_count
    #     accel_bias[2] /= packet_count
    #     gyro_bias[0] /= packet_count
    #     gyro_bias[1] /= packet_count
    #     gyro_bias[2] /= packet_count

    #     if accel_bias[2] > 0:
    #         accel_bias[2] -= accelsensitivity
    #         # Remove gravity from the z-axis accelerometer bias calculation
    #     else:
    #         accel_bias[2] += accelsensitivity
    
    #     # Construct the gyro biases for push to the hardware gyro bias registers, which are reset to zero upon device startup
    #     data = [0,0,0,0,0]
    #     data[0] = (-gyro_bias[0] / 4 >> 8) & 0xFF # Divide by 4 to get 32.9 LSB per deg/s to conform to expected bias input format
    #     data[1] = (-gyro_bias[0] / 4) & 0xFF     # Biases are additive, so change sign on calculated average gyro biases
    #     data[2] = (-gyro_bias[1] / 4 >> 8) & 0xFF
    #     data[3] = (-gyro_bias[1] / 4) & 0xFF
    #     data[4] = (-gyro_bias[2] / 4 >> 8) & 0xFF
    #     data[5] = (-gyro_bias[2] / 4) & 0xFF

    #     # Push gyro biases to hardware registers
    #     # self.bus.write_byte_data(self.address_mpu_master, XG_OFFSET_H, data[0])
    #     # self.bus.write_byte_data(self.address_mpu_master, XG_OFFSET_L, data[1])
    #     # self.bus.write_byte_data(self.address_mpu_master, YG_OFFSET_H, data[2])
    #     # self.bus.write_byte_data(self.address_mpu_master, YG_OFFSET_L, data[3])
    #     # self.bus.write_byte_data(self.address_mpu_master, ZG_OFFSET_H, data[4])
    #     # self.bus.write_byte_data(self.address_mpu_master, ZG_OFFSET_L, data[5])

    #     # Output scaled gyro biases for display in the main program
    #     gyroBias = [0,0,0]
    #     gyroBias[0] = gyro_bias[0] / gyrosensitivity
    #     gyroBias[1] = gyro_bias[1] / gyrosensitivity
    #     gyroBias[2] = gyro_bias[2] / gyrosensitivity

    #     print("GYRO BIAS")
    #     print(gyroBias)

    #     #  Construct the accelerometer biases for push to the hardware accelerometer bias registers. These registers contain
    #     #  factory trim values which must be added to the calculated accelerometer biases; on boot up these registers will hold
    #     #  non-zero values. In addition, bit 0 of the lower byte must be preserved since it is used for temperature
    #     #  compensation calculations. Accelerometer bias registers expect bias input as 2048 LSB per g, so that
    #     #  the accelerometer biases calculated above must be divided by 8.

    #     accel_bias_reg = [0, 0, 0]                # A place to hold the factory accelerometer trim biases
    #     data = self.bus.read_i2c_block_data(self.address_mpu_master, XA_OFFSET_H, 2) # Read factory accelerometer trim values
    #     accel_bias_reg[0] = self.combineBytes(data[0], data[1])
    #     data = self.bus.read_i2c_block_data(self.address_mpu_master, YA_OFFSET_H, 2) 
    #     accel_bias_reg[1] = self.combineBytes(data[0], data[1])
    #     data = self.bus.read_i2c_block_data(self.address_mpu_master, ZA_OFFSET_H, 2) 
    #     accel_bias_reg[2] = self.combineBytes(data[0], data[1])
        
    #     mask = 1             # Define mask for temperature compensation bit 0 of lower byte of accelerometer bias registers
    #     mask_bit = [0, 0, 0]  # Define array to hold mask bit for each accelerometer bias axis
       
    #     for i in range(3):

    #        if ((accel_bias_reg[ii] & mask)):
    #             mask_bit[ii] = 0x01 # If temperature compensation bit is set, record that fact in mask_bit
        
    #     # Construct total accelerometer bias, including calculated average accelerometer bias from above
    #     accel_bias_reg[0] -= (accel_bias[0] / 8) # Subtract calculated averaged accelerometer bias scaled to 2048 LSB/g (16 g full scale)
    #     accel_bias_reg[1] -= (accel_bias[1] / 8)
    #     accel_bias_reg[2] -= (accel_bias[2] / 8)

    #     data[0] = (accel_bias_reg[0] >> 8) & 0xFF
    #     data[1] = (accel_bias_reg[0]) & 0xFF
    #     data[1] = data[1] | mask_bit[0] # preserve temperature compensation bit when writing back to accelerometer bias registers
    #     data[2] = (accel_bias_reg[1] >> 8) & 0xFF
    #     data[3] = (accel_bias_reg[1]) & 0xFF
    #     data[3] = data[3] | mask_bit[1] # preserve temperature compensation bit when writing back to accelerometer bias registers
    #     data[4] = (accel_bias_reg[2] >> 8) & 0xFF
    #     data[5] = (accel_bias_reg[2]) & 0xFF
    #     data[5] = data[5] | mask_bit[2] # preserve temperature compensation bit when writing back to accelerometer bias registers

    #     # Apparently this is not working for the acceleration biases in the MPU-9250
    #     # Are we handling the temperature correction bit properly?
    #     # Push accelerometer biases to hardware registers
    #     # self.bus.write_byte_data(self.address_mpu_master, XA_OFFSET_H, data[0])
    #     # self.bus.write_byte_data(self.address_mpu_master, XA_OFFSET_L, data[1])
    #     # self.bus.write_byte_data(self.address_mpu_master, YA_OFFSET_H, data[2])
    #     # self.bus.write_byte_data(self.address_mpu_master, YA_OFFSET_L, data[3])
    #     # self.bus.write_byte_data(self.address_mpu_master, ZA_OFFSET_H, data[4])
    #     # self.bus.write_byte_data(self.address_mpu_master, ZA_OFFSET_L, data[5])

    #     # Output scaled accelerometer biases for display in the main program
    #     accelBias = [0,0,0]
    #     accelBias[0] = accel_bias[0] / accelsensitivity
    #     accelBias[1] = accel_bias[1] / accelsensitivity
    #     accelBias[2] = accel_bias[2] / accelsensitivity

    #     print("ACCEL BIAS")
    #     print(accelBias)

   

    # def combineBytes(self, data1, data2):
    #     return ((data1 << 8) | data2)