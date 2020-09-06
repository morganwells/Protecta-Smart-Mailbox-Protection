# Function to display message when PIN Code entered is correct which then opens the lock
 
import lock
import time    
import message

def code_accepted(lcd, red_light, blue_light, yellow_light, switch, relay, api_key, parcelname):
    print("Code Accepted")
    parcel_notify(parcelname, api_key)
    
    print("Switch Value", switch.value)
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
    yellow_light.on()
    print("Door Open")
    lcd.message = "Door Open"
    # Now they have opened door, wait for them to close it, then lock it
    while (switch.value == 0):
        time.sleep(0.2)
    lock.close_lock(blue_light, relay)
    yellow_light.off()
    red_light.on()
    print("Door Closed")
    lcd.message = "Door Closed"
    time.sleep(2)
    # Reset disply to start position
    print("Reset LCD after close")
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
    print("Reset LCD after deny")
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
    message.send_message(api_key,"Your mailbox alarm was triggered","Protecta Alarm")
    for i in range(4):
        lcd.home()
        lcd.message = "Alarm! Alarm!\nPolice Called"
        time.sleep(0.5)
        lcd.clear()
        time.sleep(0.5)
        
def parcel_notify(item, api_key):
    print("Sending Parcel Notification")
    mes_text = "You just recieved a parcel from " + item
    message.send_message(api_key,mes_text,"Protecta Recieved Parcel")
    
def letter_notify(api_key):
    print("Sending Letter Notificaiton")
    message.send_message(api_key,"You just recieved a letter","Protecta Recieved Letter")