#!/usr/bin/python
import sys, os, random, getopt, re
from Adafruit_Thermal import *
from PIL import Image, ImageFont

fnt = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf', 21)

def main():
    printer = Adafruit_Thermal("/dev/ttyUSB0", 9600, timeout=5)

    img = Image.open('template.png')
    add_name(img, 'text')
    printer.printImage(img, True)

    printer.feed(2)

    printer.sleep()      # Tell printer to sleep
    printer.wake()       # Call wake() before printing again, even if reset
    printer.setDefault() # Restore printer to defaults

def add_name(image, text):
  draw = ImageDraw.Draw(image)
  draw.text((30,28), 'Serra Angel', font=fnt)

if __name__ == '__main__':
  main()