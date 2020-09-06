#!/usr/bin/env python3

import digitalio
import board
import busio
import adafruit_matrixkeypad
import adafruit_character_lcd.character_lcd as characterlcd
from gpiozero import LED,OutputDevice, Button

def devices():

    # Initate devices
    yellow_light = LED(2)
    blue_light = LED(19)
    red_light = LED (26)
    switch = Button(pin = 13)
    relay = OutputDevice(18)
    letter_switch = Button(3)


    # Initate Key Pad

    cols = [digitalio.DigitalInOut(x) for x in (board.D16, board.D20, board.D21)]
    rows = [digitalio.DigitalInOut(x) for x in (board.D23, board.D24, board.D7, board.D12)]
    keys = ((1, 2, 3), (4, 5, 6), (7, 8, 9), ("*", 0, "#"))
    keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

    # Initiate LCD Matrix
    lcd_columns = 16
    lcd_rows = 2
    lcd_rs = digitalio.DigitalInOut(board.D4)
    lcd_en = digitalio.DigitalInOut(board.D17)
    lcd_d7 = digitalio.DigitalInOut(board.D6)
    lcd_d6 = digitalio.DigitalInOut(board.D5)
    lcd_d5 = digitalio.DigitalInOut(board.D22)
    lcd_d4 = digitalio.DigitalInOut(board.D27)

    # Initialise the lcd class
    lcd = characterlcd.Character_LCD_Mono(
        lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
    )

    return keypad, switch, lcd, blue_light, red_light, yellow_light, relay, letter_switch