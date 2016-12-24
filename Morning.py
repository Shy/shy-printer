from Adafruit_Thermal import *

import Image

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

im = Image.open("assets/GOODMORNING.png")
im = im.rotate(90)

printer.printImage(im)

im.save('assets/GOODMORNING.bmp')

printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults
