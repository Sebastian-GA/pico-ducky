# pico-ducky

## Install

Install and have your USB Rubber Ducky working in less than 5 minutes.

1. Clone the repo to get a local copy of the files.

2. Download [CircuitPython for the Raspberry Pi Pico](https://circuitpython.org/board/raspberry_pi_pico/). \*Updated to 8.0.0

3. Plug the device into a USB port while holding the boot button. It will show up as a removable media device named `RPI-RP2`.

4. Copy the downloaded `.uf2` file to the root of the Pico (`RPI-RP2`). The device will reboot and after a second or so, it will reconnect as `CIRCUITPY`.

5. Download `adafruit-circuitpython-bundle-8.x-mpy-YYYYMMDD.zip` [here](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/latest) and extract it outside the device.

6. Navigate to `lib` in the recently extracted folder and copy `adafruit_hid` to the `lib` folder on your Raspberry Pi Pico.

7. Copy `adafruit_debouncer.mpy` and `adafruit_ticks.mpy` to the `lib` folder on your Raspberry Pi Pico.

8. Copy `asyncio` to the `lib` folder on your Pico.

9. Copy `boot.py` from your clone to the root of your Pico.

10. Copy `duckyinpython.py`, `code.py` to the root folder of the Pico.

11. Find a script [here](https://github.com/hak5/usbrubberducky-payloads) or [create your own one using Ducky Script](https://docs.hak5.org/hak5-usb-rubber-ducky/ducky-script-basics/hello-world) and save it as `payload.dd` in the payloads folder. Currently, pico-ducky only supports DuckScript 1.0, not 3.0.

### Setup mode

To edit the payload, enter setup mode by connecting the pin 1 (`GP0`) to pin 3 (`GND`), this will stop the pico-ducky from injecting the payload in your own machine.

### USB enable/disable mode

If you need the pico-ducky to not show up as a USB mass storage device for stealth, follow these instructions.

-   Enter setup mode.
-   Copy your payload script to the pico-ducky.
-   Disconnect the pico from your host PC.
-   Connect a jumper wire between pin 18 (`GND`) and pin 20 (`GPIO15`).  
    This will prevent the pico-ducky from showing up as a USB drive when plugged into the target computer.
-   Remove the jumper and reconnect to your PC to reprogram.

### Changing Keyboard Layouts

Copied from [Neradoc/Circuitpython_Keyboard_Layouts](https://github.com/Neradoc/Circuitpython_Keyboard_Layouts/blob/main/PICODUCKY.md)

#### How to use one of these layouts with the pico-ducky repository.

**Go to the [latest release page](https://github.com/Neradoc/Circuitpython_Keyboard_Layouts/releases/latest), look if your language is in the list.**

#### If your language/layout is in the bundle

Download the `py` zip, named `circuitpython-keyboard-layouts-py-XXXXXXXX.zip`

**NOTE: You can use the mpy version targetting the version of Circuitpython that is on the device, but on Raspberry Pi Pico you don't need it - they only reduce file size and memory use on load, which the pico has plenty of.**

#### If your language/layout is not in the bundle

Try the online generator, it should get you a zip file with the bundles for yout language

https://www.neradoc.me/layouts/

#### Now you have a zip file

#### Find your language/layout in the lib directory

For a language `LANG`, copy the following files from the zip's `lib` folder to the `lib` directory of the board.  
**DO NOT** modify the adafruit_hid directory. Your files go directly in `lib`.  
**DO NOT** change the names or extensions of the files. Just pick the right ones.  
Replace `LANG` with the letters for your language of choice.

-   `keyboard_layout_win_LANG.py`
-   `keycode_win_LANG.py`

Don't forget to get [the adafruit_hid library](https://github.com/adafruit/Adafruit_CircuitPython_HID/releases/latest).

#### Modify the pico-ducky code to use your language file:

At the start of the file comment out these lines:

```py
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as KeyboardLayout
from adafruit_hid.keycode import Keycode
```

Uncomment these lines:  
_Replace `LANG` with the letters for your language of choice. The name must match the file (without the py or mpy extension)._

```py
from keyboard_layout_win_LANG import KeyboardLayout
from keycode_win_LANG import Keycode
```

##### Example: Set to German Keyboard (WIN_DE)

```py
from keyboard_layout_win_de import KeyboardLayout
from keycode_win_de import Keycode
```

Copy the files keyboard_layout_win_de.mpy and keycode_win_de.mpy to the /lib folder on the Pico board

```
adafruit_hid/
keyboard_layout_win_de.mpy
keycode_win_de.mpy
```

## Useful links and resources

### How to recover your Pico if it becomes corrupted or doesn't boot.

Follow these instructions if your Pico ends up in an odd state

1. Download the reset firmware from [flash_nuke.uf2](https://datasheets.raspberrypi.com/soft/flash_nuke.uf2)
2. While holding the BOOTSEL button on the Pico, plug in the USB cable to your computer.
3. When the RPI-RP2 drive shows up on your computer, copy the flash_nuke.uf2 file to the Pico
4. After the device reboots, follow the Install instructions.

### Docs

[CircuitPython](https://circuitpython.readthedocs.io/en/6.3.x/README.html)

[CircuitPython HID](https://learn.adafruit.com/circuitpython-essentials/circuitpython-hid-keyboard-and-mouse)

[Ducky Script](https://github.com/hak5darren/USB-Rubber-Ducky/wiki/Duckyscript)
