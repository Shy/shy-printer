from Adafruit_Thermal import *
import sys

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

with open(sys.argv[1], 'r') as f:
    text = f.read()
f.closed

printer.println(text)

printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults