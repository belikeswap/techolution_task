"""
What is Modbus?
Modbus is a royalty-free communication protocol often used in industrial communications, 
especially with PLC (Programmable Logic Controllers) and SCADA Systems.

"""

import minimalmodbus

device = minimalmodbus.Instrument('COM1', 9)
device.serial.baudrate = 9600

try:
    print(device.read_register(8000, 2))
except IOError:
    print("Error reading from device!")
