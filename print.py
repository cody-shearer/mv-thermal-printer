#!/usr/bin/python
import sys, os, random, getopt, re
from Adafruit_Thermal import *
from PIL import Image

def main():
    printer = Adafruit_Thermal("/dev/ttyUSB0", 9600, timeout=5)

    img = Image.new('1', [384,5], 'black')
    printer.printImage(img,False)

    printer.feed(2)

    printer.sleep()      # Tell printer to sleep
    printer.wake()       # Call wake() before printing again, even if reset
    printer.setDefault() # Restore printer to defaults

if __name__ == '__main__':
  main()