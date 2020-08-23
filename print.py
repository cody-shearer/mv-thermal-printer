#!/usr/bin/python
import sys, os, random, getopt, re
import uuid
from PIL import Image, ImageFont, ImageDraw

fnt = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf', 21)

def main():
    im = Image.open('template.png')
    draw = ImageDraw.Draw(im)
    
    add_name(draw, 'Serra Angel')
    add_mana_cost(draw, '3WW')
    add_art(im, 'lea-39-serra-angel.png')
    add_types(draw, 'Angel')
    add_rules(draw, 'Flying, Vigilance')
    add_artist(draw, 'Douglas Schuler')
    add_power_toughness(draw, 4, 4)

    print_file = str(uuid.uuid1()) + '.png'
    
    #im.show()
    im.save(print_file, 'PNG')

    #lp is the CUPS print command
    os.system('lp ' + print_file)
    os.remove(print_file)


def add_name(draw: ImageDraw, text: str):
  draw.text((30,28), text, font=fnt)

def add_mana_cost(draw: ImageDraw, text: str):
  draw.text((300,28), text, font=fnt)

def add_art(im_dest: Image, art: str): #expects images sized 304x245
  with Image.open(art) as im:
    im_dest.paste(im, (40, 51))


def add_types(draw: ImageDraw, text: str):
  draw.text((35,295), text, font=fnt)

def add_rules(draw: ImageDraw, text: str):
  draw.text((50,320), text, font=fnt)

def add_artist(draw: ImageDraw, text: str):
  draw.text((35,480), text, font=fnt)

def add_power_toughness(draw: ImageDraw, power: int, toughness: int):
  draw.text((310,480), str(power) + '/' + str(toughness), font=fnt)

if __name__ == '__main__':
  main()
