# License : GPLv2.0
# copyright (c) 2023  Dave Bailey
# Author: Dave Bailey (dbisu, @daveisu)
# Pico and Pico W board support

import board
import digitalio
import storage

noStorageStatus = False
noStoragePin = digitalio.DigitalInOut(board.GP11)  # Btn_3
noStoragePin.direction = digitalio.Direction.INPUT
noStoragePin.pull = digitalio.Pull.UP
noStorageStatus = noStoragePin.value

# If GP15 is not connected, it will default to being pulled high (True)
# If GP is connected to GND, it will be low (False)

if (noStorageStatus == True):
    # don't show USB drive to host PC
    storage.disable_usb_drive()
    print("Disabling USB drive")
else:
    # normal boot
    print("USB drive enabled")
