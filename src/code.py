import os
import board
import busio
import displayio
import time
import storage

from oled_hat import HAT
import ducky
import menu

from adafruit_display_text import label
import adafruit_imageload
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.triangle import Triangle


def get_payloads(function):
    os.chdir("/payloads/")
    files = os.listdir()
    my_payloads = []
    for file in files:
        if file[-3:] == ".dd" and file != "default.dd":
            my_payloads.append(menu.Menu(name=file[:-3],
                                         content=function,
                                         arg="/payloads/{}".format(file),
                                         back=None))
    return my_payloads


def run_payload(file):
    splash = displayio.Group()
    my_hat.display.show(splash)
    splash.append(Rect(0, 0, 128, 64, fill=0x000000))
    splash.append(Rect(10, 5, 108, 54, fill=0xFFFFFF))
    splash.append(Rect(20, 10, 88, 44, fill=0x000000))
    splash.append(Rect(30, 15, 68, 34, fill=0xFFFFFF))
    ducky.runScript(file)
    splash.append(Rect(0, 0, 128, 64, fill=0x000000))
    # TODO add wait message


def set_default_payload(file):
    splash = displayio.Group()
    my_hat.display.show(splash)
    splash.append(Rect(0, 0, 128, 64, fill=0x000000))
    splash.append(Rect(10, 5, 108, 54, fill=0xFFFFFF))
    # os.remove("/payloads/default.dd")
#     try:
#         with open("/payloads/default.dd", "a") as file:
#             file.write(file)
#             file.flush()
#     except OSError as e:  # Typically when the filesystem isn't writeable...
#         print(e)
#         print("ptm this doesnt work")
    # TODO add wait message


def return_itself(a):
    return a


main_menu = menu.Menu(name="main",
                      content=[menu.Menu("Run Payload", get_payloads(run_payload), None, "Cancel"),
                               menu.Menu("Set Default Payload", get_payloads(
                                   set_default_payload), None, "Cancel"),  # Add "remove default" option
                               menu.Menu("Keyboard", "peeep", None, None),
                               menu.Menu("Mouse", "peeep", None, None),
                               ],
                      arg=None,
                      back=None
                      )

my_hat = HAT()
my_hat.update_bts()
my_hat.display.sleep()

if not my_hat.bt_3.value:  # Run Payload
    ducky.runDefaultScript()

my_hat.display.wake()


def display_menu(my_menu):
    able_buttons = False  # Prevent miss click
    my_menu.reset_scroll()
    while True:
        time.sleep(0.01)
        my_hat.update_bts()

        if not able_buttons:
            able_buttons = True
            for bt in my_hat.buttons:
                if bt.value:
                    able_buttons = False
                    break

        my_hat.display.show(my_menu.return_display())

        # Buttons
        if able_buttons:
            my_hat.update_bts()
            if my_hat.bt_up.value:  # Scroll up
                my_menu.scroll_up()
            if my_hat.bt_down.value:  # Scroll down
                my_menu.scroll_down()
            if my_hat.bt_1.value:  # Enter
                answer = my_menu.select()
                if answer is -1:  # Back
                    break
                if callable(answer.content):  # Function
                    answer2 = answer.execute()
                else:  # Menu
                    # Update menu content
                    if my_menu.name == "main" and answer.name == "Run Payload":
                        my_menu.content[0].set_content(
                            get_payloads(run_payload))
                    if my_menu.name == "main" and answer.name == "Set Default Payload":
                        my_menu.content[0].set_content(
                            get_payloads(set_default_payload))

                    answer2 = display_menu(answer)  # Run the new menu
                able_buttons = False

    return answer


display_menu(main_menu)
