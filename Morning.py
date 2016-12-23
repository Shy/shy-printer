from Adafruit_Thermal import *
import Image

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

im = Image.open("/img/GOODMORNING.png")
im.rotate(90)

printer.printImage(im,FALSE)