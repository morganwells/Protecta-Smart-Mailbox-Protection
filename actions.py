# Function to display message when PIN Code entered is correct which then opens the lock
 
import lock
import time    
import message

def code_accepted(lcd, red_light, blue_light, switch, relay):
    print("Code Accepted")
    print("Switch Value", switch.value)
    lcd.clear()
    lcd.home()
    lock.open_lock(blue_light, relay)
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
    lock.close_lock(blue_light, relay)
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

def code_denied(lcd, red_light):
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

    # Function if door is opened without PIN or RFID to alert breakin

def run_alarm(lcd, red_light, api_key):
    print("Alarm Triggered")
    # Clear Display
    lcd.clear()
    lcd.home()
    lcd.cursor = False
    # Flash denied message and red light
    red_light.blink()
    message.send_message("mailbox_alarm","Alarm One","Alarm Two","Alarm Three",api_key)
    for i in range(4):
        lcd.home()
        lcd.message = "Alarm! Alarm!\nPolice Called"
        time.sleep(0.5)
        lcd.clear()
        time.sleep(0.5)