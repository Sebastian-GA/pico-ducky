import board
import digitalio
from adafruit_debouncer import Debouncer

import displayio
import busio
import adafruit_displayio_sh1106
from adafruit_display_shapes.rect import Rect

displayio.release_displays()

# ---------------------------------
# Buttons
PIN_BT_UP = board.GP7    # GPIO6
PIN_BT_DOWN = board.GP9  # GPIO19
PIN_BT_LEFT = board.GP6  # GPIO5
PIN_BT_RIGHT = board.GP10  # GPIO26
PIN_BT_CENTER = board.GP8  # GPIO13
PIN_BT_1 = board.GP13  # GPIO21
PIN_BT_2 = board.GP12  # GPIO20
PIN_BT_3 = board.GP11  # GPIO16
# Oled screen SPI
PIN_RS = board.GP16  # GPIO25
PIN_CS = board.GP17  # GPIO8
PIN_SCLK = board.GP18  # GPIO11
PIN_MOSI = board.GP19  # GPIO10
PIN_DC = board.GP20  # GPIO24

WIDTH = 128
HEIGHT = 64


def init_bt(pin):  # Init buttons
    # Reference: https://learn.adafruit.com/debouncer-library-python-circuitpython-buttons-sensors/advanced-debouncing
    bt = digitalio.DigitalInOut(pin)
    bt.direction = digitalio.Direction.INPUT
    bt.pull = digitalio.Pull.UP
    return lambda: not bt.value


class HAT():
    def __init__(self):
        # Setup Screen
        spi = busio.SPI(PIN_SCLK, PIN_MOSI)
        display_spi_bus = displayio.FourWire(spi,
                                             command=PIN_DC,
                                             chip_select=PIN_CS,
                                             reset=PIN_RS,
                                             baudrate=1000000,
                                             )

        self.display = adafruit_displayio_sh1106.SH1106(bus=display_spi_bus,
                                                        width=132,
                                                        height=64,
                                                        rotation=180)

        # Setup buttons
        self.bt_up = Debouncer(init_bt(PIN_BT_UP))
        self.bt_down = Debouncer(init_bt(PIN_BT_DOWN))
        self.bt_left = Debouncer(init_bt(PIN_BT_LEFT))
        self.bt_right = Debouncer(init_bt(PIN_BT_RIGHT))
        self.bt_center = Debouncer(init_bt(PIN_BT_CENTER))
        self.bt_1 = Debouncer(init_bt(PIN_BT_1))
        self.bt_2 = Debouncer(init_bt(PIN_BT_2))
        self.bt_3 = Debouncer(init_bt(PIN_BT_3))
        self.bts = [self.bt_up, self.bt_down, self.bt_left, self.bt_right,
                    self.bt_center, self.bt_1, self.bt_2, self.bt_3]

    # Update Buttons
    def update_bts(self):
        for bt in self.bts:
            bt.update()

    def clear(self):
        splash = displayio.Group()
        self.display.show(splash)
        splash.append(Rect(x=0, y=0, width=128, height=64, fill=0xFFFFFF))
