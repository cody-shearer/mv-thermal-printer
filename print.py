#!/usr/bin/python
import sys, os, random, getopt, re
from Adafruit_Thermal import *
from PIL import Image

def main():
    printer = Adafruit_Thermal("/dev/ttyUSB0", 9600, timeout=5)


    printer.printImage('template.png',False)

    printer.feed(2)

    printer.sleep()      # Tell printer to sleep
    printer.wake()       # Call wake() before printing again, even if reset
    printer.setDefault() # Restore printer to defaults

if __name__ == '__main__':
  main()