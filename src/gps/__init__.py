# import time
# import serial
               
# ser = serial.Serial(            
#      port='/dev/serial0',
#      baudrate = 9600,
#      parity=serial.PARITY_NONE,
#      stopbits=serial.STOPBITS_ONE,
#      bytesize=serial.EIGHTBITS,
#      timeout=1
# )
         
# while 1:
#      ser.write('Hello\n')
#      time.sleep(1)

import serial

# serialport = serial.Serial("serial0", baudrate=9600, timeout=3.0)
serialport = serial.Serial("/dev/serial0", baudrate=9600, timeout=3.0)
# serialport = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)

print(serialport.isOpen())

def parseGPS(stri):
#     if stri.find('GGA') > 0:
        msg = pynmea2.parse(stri)
        print("AQUI")
        print(msg)
        print("Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s", msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units)

while True:
#     serialport.write("rnSay something:".encode())
#     rcv = serialport.read(10)
#     print(rcv)
#     serialport.write(("rnYou sent:" + repr(rcv)).encode())
     stri = serialport.readline()
     print(stri)
     parseGPS(stri)