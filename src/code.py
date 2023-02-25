import os
import time

import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect

from oled_hat import HAT
import ducky
import menu


def get_payloads(function):
    # Returns a list of all avaiable payloads in /payloads folder
    # Every item in the list is a Menu instance where content is
    # the function argument

    os.chdir("/payloads/")
    files = os.listdir()
    my_payloads = []
    for file in files:
        if file[-3:] == ".dd" and file != "default.dd":
            my_payloads.append(menu.Menu(name=file[:-3],
                                         content=function,
                                         arg="/payloads/{}".format(file)))
    return my_payloads


def run_payload(file):
    splash = displayio.Group()
    my_hat.display.show(splash)
    splash.append(Rect(0, 0, 128, 64, fill=0x000000))
    splash.append(Rect(10, 5, 108, 54, fill=0xFFFFFF))
    splash.append(Rect(20, 10, 88, 44, fill=0x000000))
    splash.append(label.Label(terminalio.FONT,
                  text="Running", color=0xFFFFFF, x=40, y=25))

    ducky.runScript(file)


def set_default_payload(file):
    splash = displayio.Group()
    my_hat.display.show(splash)
    splash.append(Rect(0, 0, 128, 64, fill=0x000000))
    splash.append(Rect(10, 5, 108, 54, fill=0xFFFFFF))
    splash.append(Rect(20, 10, 88, 44, fill=0x000000))
    splash.append(label.Label(terminalio.FONT,
                  text="Setting", color=0xFFFFFF, x=40, y=25))

    # os.remove("/payloads/default.dd")
    # try:
    #     with open("/payloads/default.dd", "a") as file:
    #         file.write(file)
    #         file.flush()
    # except OSError as e:  # Typically when the filesystem isn't writeable...
    #     print(e)
    #     print("ptm this doesnt work")


main_menu = menu.Menu(name="main",
                      content=[menu.Menu("Run Payload", get_payloads(run_payload), None, "Cancel"),
                               menu.Menu("Set Default Payload", get_payloads(
                                   set_default_payload), None, "Cancel"),
                               # menu.Menu("Keyboard", "peeep", None, None),
                               # menu.Menu("Mouse", "peeep", None, None),
                               ],
                      arg=None
                      )

my_hat = HAT()
my_hat.update_bts()
my_hat.display.sleep()
time.sleep(1)


# --------------------- MAIN PROGRAM ---------------------
if not my_hat.bt_3.value:  # Run Payload
    ducky.runDefaultPayload()

my_hat.display.wake()


def display_menu(my_menu):
    my_menu.reset_scroll()

    while True:
        time.sleep(0.01)
        my_hat.display.show(my_menu.return_display())

        # Buttons
        my_hat.update_bts()
        if my_hat.bt_up.rose:  # Scroll up
            my_menu.scroll_up()
        if my_hat.bt_down.rose:  # Scroll down
            my_menu.scroll_down()
        if my_hat.bt_1.rose:  # Enter

            if callable(my_menu.content):
                my_menu.execute()
                return 0
            else:  # Menu
                answer = my_menu.select()
                if answer is -1:  # Back
                    return -1  # Exit from this menu and go back
                else:
                    # # Update menu content in case default changed
                    # if my_menu.name == "main" and answer.name == "Run Payload":
                    #     my_menu.content[0].set_content(
                    #         get_payloads(run_payload))
                    # if my_menu.name == "main" and answer.name == "Set Default Payload":
                    #     my_menu.content[0].set_content(
                    #         get_payloads(set_default_payload))
                    display_menu(answer)  # Run the new menu

    return 0


display_menu(main_menu)
