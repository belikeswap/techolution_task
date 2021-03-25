import minimalmodbus

device = minimalmodbus.Instrument('COM1', 9)
device.serial.baudrate = 9600

try:
    print(device.read_register(8000, 2))
except IOError:
    print("Error reading from device!")
