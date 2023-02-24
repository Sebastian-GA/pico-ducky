# License : GPLv2.0
# copyright (c) 2023  Dave Bailey
# Author: Dave Bailey (dbisu, @daveisu)
# Pico and Pico W board support


import supervisor


import time
import digitalio
from board import *
import board
from duckyinpython import *


# sleep at the start to allow the device to be recognized by the host computer
time.sleep(.5)

# turn off automatically reloading when files are written to the pico
#supervisor.disable_autoreload()
supervisor.runtime.autoreload = False

led = pwmio.PWMOut(board.LED, frequency=5000, duty_cycle=0)

led_state = False

async def main_loop():
    global led,button1

    button_task = asyncio.create_task(monitor_buttons(button1))
    pico_led_task = asyncio.create_task(blink_led(led))
    await asyncio.gather(pico_led_task, button_task)

asyncio.run(main_loop())
