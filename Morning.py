from Adafruit_Thermal import *

from PIL import Image

printer = Adafruit_Thermal("/dev/ttyS0", 19200, timeout=5)

im = Image.open("assets/GOODMORNING.png")

new_width  = 384
new_height = new_width * im.height / im.width

im = im.resize((new_width,new_height))


im.save('assets/GOODMORNING.bmp')

printer.printImage(im,True)


printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults
