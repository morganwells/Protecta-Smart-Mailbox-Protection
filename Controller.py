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
import digitalio
import board
import busio
import adafruit_matrixkeypad
import adafruit_character_lcd.character_lcd as characterlcd
from mfrc522 import SimpleMFRC522
from gpiozero import LED,OutputDevice, Button
from signal import pause
import requests
import json

# Initate devices
blue_light = LED(26)
red_light = LED (19)
switch = Button(pin = 13)
reader = SimpleMFRC522()
relay = OutputDevice(18)


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

# Send Message to Line via IFTTT

def check_pin(pin_entered):
    pinstr = str(pin_entered[0]) + str(pin_entered[1]) + str(pin_entered[2]) + str(pin_entered[3])
    pinokflag = False
    parcels = data.get("parcels")
    for parcel in parcels:
        if parcel.get("pin") == pinstr:
            pinokflag = True
    return pinokflag

def check_tagid(tagid_entered):
    tagokflag = False
    users = data.get("users")
    for user in users:
        if user.get("tagid") == str(tagid_entered):
            tagokflag = True
    return tagokflag

def send_message(event, val1, val2, val3):
    url = "https://maker.ifttt.com/trigger/" + event +"/with/key/" + api_key
    x = requests.post(url, data = {"value1": val1, "value2":val2, "value3":val3})
    print(x.text)

# Function if door is opened without PIN or RFID to alert breakin

def run_alarm():
    print("Alarm Triggered")
    # Clear Display
    lcd.clear()
    lcd.home()
    lcd.cursor = False
    # Flash denied message and red light
    red_light.blink()
    send_message()
    for i in range(4):
        lcd.home()
        lcd.message = "Alarm! Alarm!\nPolice Called"
        time.sleep(0.5)
        lcd.clear()
        time.sleep(0.5)


# Function to open lock
def open_lock():
    print("Opening Lock")
    blue_light.on()
    relay.on()
   
# function to close lock
def close_lock():
    print("Closing Lock")
    blue_light.off()
    relay.off()
    
# Function to display message when PIN Code entered is correct which then opens the lock    

def code_accepted():
    print("Code Accepted")
    print("Switch Value", switch.value)
    lcd.clear()
    lcd.home()
    open_lock()
    red_light.off()
    blue_light.on()
    for i in range(4):
        lcd.message = "Code Accepted!"
        time.sleep(0.5)
        lcd.clear()
        time.sleep(0.5)
    # wait for the person to open door after unlocking it    
    switch.wait_for_release()
    print("Door Open")
    lcd.message = "Door Open"
    # Now they have opened door, wait for them to close it, then lock it
    while (switch.value == 0):
        time.sleep(0.2)
    close_lock()
    red_light.on()
    print("Door Closed")
    lcd.message = "Door Closed"
    time.sleep(1)
    # Reset disply to start position
    lcd.clear()
    lcd.message = "Enter PIN:"
    lcd.cursor = True
    lcd.cursor_position(0,2)

    
# Function to display message when PIN Code entered is incorrect

def code_denied():
    print("Code Denied")
    # Clear Display
    lcd.clear()
    lcd.home()
    lcd.cursor = False
    # Flash denied message and red light
    for i in range(4):
        lcd.message = "Code Denied!"
        red_light.on()
        time.sleep(0.5)
        lcd.clear()
        red_light.off()
        time.sleep(0.5)
    # Reset disply to start position
    lcd.message = "Enter PIN:"
    lcd.cursor = True
    lcd.cursor_position(0,2)
    red_light.on()

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
        if check_tagid(id):
            code_accepted()
        # wrong RFID tag quit
        else:
            code_denied()
            
        # Reset PIN ready for next try
        seq = []
        
    # To open lock with PIN enter four numbers and press # button
    
    # Check if # pressed or if 4 numbers already entered
    elif (key=="#" or len(seq)>3):
        # Check if PIN entered matched code
        if check_pin(seq):
            code_accepted()
        # Wrong Code entered    
        else:
            code_denied()    
        # Reset PIN ready for next try
        seq = []

    # If less than 4 numbers add latest number to PIN sequence
    else:
        # Print result
        seq.append(key)
        lcd.cursor_position(len(seq),2)
        lcd.message = str(key)
        print(key,seq)



# Start Main

# Start Message LCD


lcd.message = "Enter PIN:"
lcd.cursor = True
lcd.cursor_position(0,2)

# Wait for Key Press, when pressed run printKey funtion

while True:
    
    
    keys = keypad.pressed_keys
    if (switch.value == 0):
        run_alarm()
    if keys:
        print("Pressed: ", keys[0])
        printKey(keys[0])
    time.sleep(0.2)





