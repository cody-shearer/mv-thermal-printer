# This script accepts 1 argument, Converted Mana Cost(CMC)
# A local MariaDB instance is queried for a random card with the given CMC.
# An image is constructed from a template, the card art, and card info and then printed.

import mariadb
import os
import sys
import uuid
from PIL import Image, ImageFont, ImageDraw

fnt = ImageFont.truetype('VCR_OSD_MONO_1.001.ttf', 21)

def main(argv):
    name, mana_cost, art_file, card_type, rules, artist, power, toughness = get_card(int(argv))[0]

    im = Image.open('template.png')
    draw = ImageDraw.Draw(im)

    add_name(draw, name)
    add_mana_cost(draw, mana_cost)
    add_art(im, art_file)
    add_types(draw, card_type)
    add_rules(draw, rules)
    add_artist(draw, artist)
    add_power_toughness(draw, power, toughness)

    print_file = str(uuid.uuid1()) + '.png'

    # im.show()
    im.save(print_file, 'PNG')

    # lp is the CUPS print command
    os.system('lp ' + print_file)
    os.remove(print_file)


def add_name(draw: ImageDraw, text: str):
    draw.text((30, 28), text, font=fnt)


def add_mana_cost(draw: ImageDraw, text: str):
    draw.text((300, 28), text, font=fnt)

# expects images sized 304x245
def add_art(im_dest: Image, art: str):  
    with Image.open(art) as im:
        im_dest.paste(im, (40, 51))


def add_types(draw: ImageDraw, text: str):
    draw.text((35, 295), text, font=fnt)


def add_rules(draw: ImageDraw, text: str):
    draw.text((50, 320), text, font=fnt)


def add_artist(draw: ImageDraw, text: str):
    draw.text((35, 480), text, font=fnt)


def add_power_toughness(draw: ImageDraw, power: int, toughness: int):
    draw.text((310, 480), str(power) + '/' + str(toughness), font=fnt)


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
    main(sys.argv[0])
