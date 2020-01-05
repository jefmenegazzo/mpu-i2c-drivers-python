##################################################################### 
# Author: Jeferson Menegazzo                                        # 
# Year: 2020                                                        # 
# License: MIT                                                      # 
##################################################################### 

# Class for code testing without I2C access. 
class FakeSmbus(object): 
    
    class SMBus(object): 
        
        def __init__(self, bus): 
            pass 
        
        def write_byte_data(self, a, b, c): 
            pass 
        
        def read_byte_data(self, a, b): 
            return 0 
            
        def read_i2c_block_data(self, a, b, c): 
            return [0] * c
            
        def close(self): 
            pass