# This script accepts 1 argument, Converted Mana Cost(CMC)
# A local MariaDB instance is queried for a random card with the given CMC.
# An image is constructed from a template, the card art, and card info and then printed.

import mariadb
import os
import re
import sys
import uuid
from PIL import Image, ImageFont, ImageDraw

fnt = ImageFont.truetype('/home/pi/mv-thermal-printer/mplantin.ttf', 20)

def print_card(argv):
    name, mana_cost, art_file, card_type, rules, artist, power, toughness = get_card(int(argv))[0]

    im = Image.open('/home/pi/mv-thermal-printer/template.png')
    draw = ImageDraw.Draw(im)

    add_name(draw, name)
    add_mana_cost(draw, mana_cost)
    add_art(im, art_file)
    add_types(draw, card_type)
    add_rules(draw, rules)
    add_artist(draw, artist)
    add_power_toughness(draw, power, toughness)

    print_file = '/home/pi/mv-thermal-printer/' + str(uuid.uuid1()) + '.png'

    # im.show()
    im.save(print_file, 'PNG')

    # lp is the CUPS print command
    os.system('lp ' + print_file)
    os.remove(print_file)


def add_name(draw: ImageDraw, text: str):
    draw.text((30, 28), text, font=fnt)


def add_mana_cost(draw: ImageDraw, text: str):
    draw.text((355 - fnt.getsize(text)[0], 28), text, font=fnt)


def add_art(im_dest: Image, art: str): # expects images sized 304x245
    with Image.open(art) as im:
        im_dest.paste(im, (40, 51))


def add_types(draw: ImageDraw, text: str):
    draw.text((30, 299), text, font=fnt)


def add_rules(draw: ImageDraw, text: str): # max 286 width per line
    formatted_text = ''

    # removing reminder text to reduce rules text length
    text_no_reminder = re.sub(re.compile("[(].*?[)]"), '', text)

    # insert \n as needed to keep rules text within the box
    for line in text_no_reminder.split('\n'):
        new_line = ''
        ret_line = ''
        if fnt.getsize(line)[0] > 286:
            for word in line.split(' '):
                if fnt.getsize(new_line + word)[0] > 286 or fnt.getsize(word)[0] > 286:
                    if ret_line == '':
                        ret_line = new_line + '\n'
                    else:
                        ret_line = ret_line + new_line + '\n'
                    new_line = word + ' '
                else:
                    new_line = new_line + word + ' '
            ret_line = ret_line + new_line
        else:
            ret_line = line

        if formatted_text == '':
            formatted_text = ret_line + '\n'
        else:
            formatted_text = formatted_text + ret_line + '\n'

    formatted_text = formatted_text.strip()

    if len(formatted_text.split('\n')) > 7:
        formatted_text = 'Rules text too long.\n'

    draw.text((48, 322), formatted_text, font=fnt)


def add_artist(draw: ImageDraw, text: str):
    draw.text((30, 480), text, font=fnt)


def add_power_toughness(draw: ImageDraw, power: int, toughness: int):
    text = str(power) + '/' + str(toughness)
    draw.text((355 - fnt.getsize(text)[0], 480), text, font=fnt)


def get_card(cmc):
    conn = mariadb.connect(host='127.0.0.1', user='root',
                           password='pass', db='mtg')
    cursor = conn.cursor()
    sql = (
        'select \
            name, mana_cost, art_file, type, rules, artist, power, toughness \
        from \
            mtg.oracle_cards \
        where \
            cmc = %s \
            and not art_file is null \
        order by \
            rand() \
        limit 1')
    cursor.execute(sql, [cmc])
    return cursor.fetchall()


if __name__ == '__main__':
    print_card(sys.argv[1])
