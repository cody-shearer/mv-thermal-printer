#!/usr/bin/python
import sys, os, random, getopt, re
from Adafruit_Thermal import *
from PIL import Image, ImageFont, ImageDraw

fnt = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf', 21)

def main():
    printer = Adafruit_Thermal("/dev/ttyUSB0", 9600, timeout=5)

    im = Image.open('template.png')
    add_name(im, 'Serra Angel')
    add_rules(im, 'Flying, Vigilance')
    add_artist(im, 'Douglas Schuler')
    add_types(im, 'Angel')
    add_power_toughness(im, '4/4')
    add_art(im, 'lea-39-serra-angel.png')
    printer.printImage(im, True)

    printer.feed(2)

    printer.sleep()      # Tell printer to sleep
    printer.wake()       # Call wake() before printing again, even if reset
    printer.setDefault() # Restore printer to defaults

def add_name(image, text):
  draw = ImageDraw.Draw(image)
  draw.text((30,28), text, font=fnt)

def add_rules(image, text):
  draw = ImageDraw.Draw(image)
  draw.text((50,320), text, font=fnt)

def add_artist(image, text):
  draw = ImageDraw.Draw(image)
  draw.text((35,480), text, font=fnt)

def add_power_toughness(image, text):
  draw = ImageDraw.Draw(image)
  draw.text((300,480), text, font=fnt)

def add_art(image, art):
  im = Image.open(art)
  image.paste(im, (40, 51))

def add_types(image, text):
  draw = ImageDraw.Draw(image)
  draw.text((35,295), text, font=fnt)

def add_mana_cost(image, text):
  draw = ImageDraw.Draw(image)
  draw.text((30,28), text, font=fnt)

if __name__ == '__main__':
  main()