# This script runs on raspberry pi startup
# Handles key presses, display, and sends cmc to printer script

import adafruit_matrixkeypad
import board
import digitalio
import printer
import time
from adafruit_ht16k33.segments import Seg14x4

# initialize keypad
cols = [digitalio.DigitalInOut(x) for x in (board.D13, board.D5, board.D26)]
rows = [digitalio.DigitalInOut(x) for x in (board.D6, board.D21, board.D20, board.D19)]

keys = ((1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        ('*', 0, '#'))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

# initialize display
i2c = board.I2C()
display = Seg14x4(i2c)
disp = '00'
display.print(disp)

# used to prevent repeated input while holding the key down
wait = False

while True:
    keys = keypad.pressed_keys
    if not keys:
        wait = False
    if len(keys) <= 3:
        if keys and not wait:
            wait = True

            if str(keys)[1] == '\'':
                key = str(keys)[2]
            else:
                key = str(keys)[1]

            if key == '*':
                disp = '00'
                display.print(disp)
            elif key == '#':
                disp = '00'
                display.print(disp)
                printer.print_card(int(disp))
            else:
                disp = disp[1] + str(key)
                display.print(disp)
    time.sleep(0.1)
