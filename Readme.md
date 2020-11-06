# Protecta Smart Mailbox Protection

## Overview

Software code to run Protecta Mailbox.

## Pre-requisites

1. Make sure Pi is up to date

```
sudo apt-get update
sudo apt-get upgrade
```

1. Make sure Python 3 and the package manager Pip3 is installed and latest version
```
sudo apt-get install python3
```

1. Enable the SPI interface
see https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-spi

1. Install the Python Libraries
```
sudo pip3 install RPI.GPIO
sudo pip3 install adafruit-blinka
sudo pip3 install adafruit-circuitpython-charlcd
sudo pip3 install adafruit-circuitpython-matrixkeypad
sudo pip3 install spidev
sudo pip3 install mfrc522


```

## Wiring

### KeyPad

Membrane 3x4 matrix keypad - https://www.adafruit.com/product/419

Pin Config:

|Position (left to Right)| Wire Colour | GPIO Pin | Details |
| --- | --- | --- | --- | 
| 1 | RED | GPIO23 | Row 1 |
| 2 | ORANGE | GPIO24 | Row 2 |
| 3 | YELLOW | GPIO07 | Row 3 |
| 4 | GREEN | GPIO12 | Row 4 |
| 5 | BLUE | GPIO16 | Col 1 |
| 6 | PURPLE | GPIO20 | Col 2 |
| 7 | GREY | GPIO21 | Col 3 |

### RFID Reader

Duinotech XC4506 RFID RC522
https://www.jaycar.com.au/medias/sys_master/images/images/9403738816542/XC4506-dataSheetMain.pdf

Pin Config

|Position (left to Right)| Wire Colour | GPIO Pin | Details |
| --- | --- | --- | --- | 
| 1 | Brown | 3.3V | VCC |
| 2 | Yellow| GPIO25 | RST |
| 3 | Black | GND    | GND |
| 4 | Blue | SPIMSO | MOS |
| 5 | Purple | SPIMOSI | MOSI |
| 6 | Green | SPICLX | SCK |
| 7 | Orange | SPICEO | NCS |
| 8 | Null | Null | Null |IRQ |

### LCD Matrix

Adafruit Standard HD44780 LCD - https://www.adafruit.com/product/181

Pin Config:

|Position (left to Right)| Wire Colour | GPIO Pin | Details |
| --- | --- | --- | --- | 
| 1 | Black | GND | VSS |
| 2 | Red | 5V | VDD |
| 3 | Black | GND | V0 |
| 4 | Yellow  | LCD_RS = GPIO4 | RS | 
| 5 | Black  | GND | RW |
| 6 | Green  | LCD_E  = GPIO17 : Green | E |
| 7 |   | Null | D0 |
| 8 |   | Null | D1 |
| 9 |   | Null | D2 |
| 10|   | Null | D3 |
| 11| Orange | LCD_D4 = GPIO27 | D4 |
| 12| Blue   | LCD_D5 = GPIO22 | D5 |
| 13| Grey  | LCD_D6 = GPIO5 | D6 | 
| 14| White  | LCD_D7 = GPIO6 | D7 | 
| 15| Red   | 5V | A |
| 16| Black | GND | K |

## Components

- controller.py - Main file which reads keypad entry and checks the codes entered and controls response
- initate.py - Gets the electronic components ready
- actions.py - Performs actions according to code entered either accepting code (which unlocks door), denying code (sends message to display or raises alarm (send alarm message)
- lock.py - open and shuts lock when called code is accepted
- validations.py - compares PIN Code or RFID Tag id entered against the stored known codes
- message.py - trigers Push Safer event, which sends notification to phone app
- data.json (no in repo) - PIN codes for parcel delivery, RFID Id's and Push Safer Private Key

## References

1. https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/overview
1. LCD Controller - https://github.com/adafruit/Adafruit_CircuitPython_CharLCD
1. Matrix Keypad - https://github.com/adafruit/Adafruit_CircuitPython_MatrixKeypad
1. RFID - https://pimylifeup.com/raspberry-pi-rfid-rc522/
1. Notifcation service - www.pushsafer.com
