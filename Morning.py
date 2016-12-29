from Adafruit_Thermal import *

from PIL import Image

printer = Adafruit_Thermal("/dev/ttyS0", 19200, timeout=5)

im = Image.open("assets/GOODMORNING.png")

width, height = im.size

new_width  = 384
new_height = new_width * height / width

im = im.resize((new_width,new_height))

printer.printImage(im,True)

printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults
