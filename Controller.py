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


# Intiate Devices

keypad, switch, lcd, blue_light, red_light, relay, reader = initiate.devices()

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
    
# Function to Check PIN
def printKey(key):
    global seq
    # To open lock with RFID press * button and then use RFID tag
    if (key =="*"):
        
        # Wait for RFID Input
        id, text = reader.read()
        print(id)
        print(text)
        
        # If RFID Tag is authenticated
        if validations.check_tagid(id, data):
            actions.code_accepted(lcd, red_light, blue_light, switch, relay)
        # wrong RFID tag quit
        else:
            actions.code_denied(lcd, red_light)
            
        # Reset PIN ready for next try
        seq = []
        
    # To open lock with PIN enter four numbers and press # button
    
    # Check if # pressed or if 4 numbers already entered
    elif (key=="#" or len(seq)>3):
        # Check if PIN entered matched code
        if validations.check_pin(seq, data):
            actions.code_accepted(lcd, red_light, blue_light, switch, relay)
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

# Start Message LCD

lcd.message = "Enter PIN:"
lcd.cursor = True
lcd.cursor_position(0,2)

# Wait for Key Press, when pressed run printKey funtion

while True:
     
    keys = keypad.pressed_keys
    if (switch.value == 0):
        actions.run_alarm(lcd, red_light, api_key)
    if keys:
        print("Pressed: ", keys[0])
        printKey(keys[0])
    time.sleep(0.2)
