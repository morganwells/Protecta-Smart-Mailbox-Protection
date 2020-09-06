# Validates PIN and RFID Tag ID against JSON file

def check_pin(pin_entered, data):
    pinstr = str(pin_entered[0]) + str(pin_entered[1]) + str(pin_entered[2]) + str(pin_entered[3])
    pinokflag = False
    parcels = data.get("parcels")
    for parcel in parcels:
        if parcel.get("pin") == pinstr:
            parcelname = parcel.get("item")
            pinokflag = True
    return pinokflag, parcelname

def check_tagid(tagid_entered, data):
    tagokflag = False
    users = data.get("users")
    for user in users:
        if user.get("tagid") == str(tagid_entered):
            tagokflag = True
    return tagokflag