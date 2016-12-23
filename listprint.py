from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

with open('assets/sentai.txt', 'r') as f:
    text = f.readlines()
f.closed

for line in text:
    printer.println(line)

printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults