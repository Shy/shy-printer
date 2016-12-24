from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

with open('assets/kamenrider.txt', 'r') as f:
    text = f.read()
f.closed

printer.inverseOn()
printer.println(text)
printer.inverseOff()

printer.upsideDownOn()
printer.println(text)
printer.upsideDownOff()

printer.sidewaysOn()
printer.println(text)
printer.sidewaysOff()

printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults