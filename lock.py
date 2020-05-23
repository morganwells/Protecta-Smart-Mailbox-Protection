# Function to open lock


def open_lock(blue_light, relay):
    print("Opening Lock")
    blue_light.on()
    relay.on()
   
# function to close lock
def close_lock(blue_light, relay):
    print("Closing Lock")
    blue_light.off()
    relay.off()