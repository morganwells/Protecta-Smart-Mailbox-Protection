#!/usr/bin/env python3
#
#
#
#
#   References: 
#     1) LCD Controller - https://github.com/adafruit/Adafruit_CircuitPython_CharLCD
#     2) Matrix Keypad - https://github.com/adafruit/Adafruit_CircuitPython_MatrixKeypad
#     3) RFID - https://github.com/adafruit/Adafruit_CircuitPython_PN532
#
#
#

# Import modules

import time
from signal import pause
import json

import initiate
import validations
import actions
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

import os
os.chdir("/home/morgan/Documents/pi-letterbox")

# Intiate Devices

keypad, switch, lcd, blue_light, red_light, yellow_light, relay, letter_switch = initiate.devices()

# Reset Devices
relay.off()
blue_light.off()
red_light.on()
lcd.clear()
lcd.home()

# Initiate Variables
seq=[]
tries = 0
with open('data.json') as json_file:
    data = json.load(json_file)
    api_key = data.get("api_key")
    print(api_key)

# Function to Check PIN
def check_code(key):
    global seq
    # To open lock with RFID press * button and then use RFID tag
    if (key =="*"):
        lcd.clear()
        lcd.home()
        lcd.message = "Swipe RFID Tag"
        reader = SimpleMFRC522()
        print(reader)
        # Wait for RFID Input
        id, text = reader.read()
        print(id)
        print(text)
        
        # If RFID Tag is authenticated
        if validations.check_tagid(id, data):
            actions.code_accepted(lcd, red_light, blue_light, yellow_light, switch, relay, api_key, "Morgan RFID Entry")
        # wrong RFID tag quit
        else:
            actions.code_denied(lcd, red_light)
            
        # Reset PIN ready for next try
        seq = []
        
    # To open lock with PIN enter four numbers and press # button

    # Check if # pressed or if 4 numbers already entered
    elif (key=="#" or len(seq)>3):
        # Check if PIN entered matched code
        pinreturn = validations.check_pin(seq, data)
        print (pinreturn)
        if pinreturn[0]:
            actions.code_accepted(lcd, red_light, blue_light, yellow_light, switch, relay, api_key, pinreturn[1])
        # Wrong Code entered    
        else:
            actions.code_denied(lcd, red_light)    
        # Reset PIN ready for next try
        seq = []

    # If less than 4 numbers add latest number to PIN sequence
    else:
        # Print result
        seq.append(key)
        lcd.cursor_position(len(seq),2)
        lcd.message = str(key)
        print(key,seq)

try:
    # Start Message LCD
    print("Writing Sart message")
    lcd.message = "Enter PIN:"
    lcd.cursor = True
    lcd.cursor_position(0,2)
    
    # Start monitoring Letter Slot switch
    def send_letter():
        actions.letter_notify(api_key)
    letter_switch.when_released =  send_letter

    # Wait for Key Press, when pressed run printKey funtion

    while True:
     
        keys = keypad.pressed_keys
        # wait for key press
        if keys:
            print("Pressed: ", keys[0])
            check_code(keys[0])
        time.sleep(0.2)
        # check to see if mailbox door is opened without code 
        if (switch.value == 0):
                    actions.run_alarm(lcd, red_light, api_key)

finally:
    red_light.off()
    lcd.clear()
    lcd.home()
    lcd.message = "Goodbye"
    time.sleep(2.0)
    GPIO.cleanup()
    