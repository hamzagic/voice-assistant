import glob
import serial

ports = glob.glob('/dev/tty.*')
print(ports)