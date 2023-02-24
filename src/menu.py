import displayio
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect


def constrain(var, min, max):
    if min <= max:
        if min <= var <= max:
            return var
        elif var < min:
            return min
        else:
            return max
    else:  # This is an error
        return 0


class Menu():
    def __init__(self, name, content, arg, back):
        self.name = name
        # If content is callable, call as self.content(self.argument)
        self.argument = arg
        self._backeable = not back is None
        self.back = back
        self.set_content(content)

        self.curS = 0  # Position of cursor in screen
        self.curA = 0  # Index of first element in screen
        # Item Selected = cusA + curS

    def set_content(self, content):
        self.content = content
        if self._backeable:
            self.content.append(str(self.back))

    def scroll_up(self):
        num_options = constrain(len(self.content), 1, 4)
        if self.curS == 0:
            self.curA = constrain(
                self.curA - 1, 0, len(self.content) - num_options)
        self.curS = constrain(self.curS - 1, 0, num_options - 1)

    def scroll_down(self):
        num_options = constrain(len(self.content), 1, 4)
        if self.curS == 3:
            self.curA = constrain(
                self.curA + 1, 0, len(self.content) - num_options)
        self.curS = constrain(self.curS + 1, 0, num_options - 1)

    def reset_scroll(self):
        self.curS = 0
        self.curA = 0

    def execute(self):
        if callable(self.content):
            if not self.argument is None:
                return self.content(self.argument)
            return self.content()

    def select(self):
        if type(self.content) is list:
            if self._backeable and self.curA + self.curS == len(self.content) - 1:
                return -1
            return self.content[self.curA + self.curS]

    def return_display(self):
        # TODO add options to nums
        if type(self.content) is list:
            splash = displayio.Group()
            splash.append(Rect(0, 0, 128, 64, fill=0x000000))  # Clear

            # Amount of options to show in screen
            num_options = constrain(len(self.content), 1, 4)
            for i in range(num_options):
                option = self.content[i + self.curA]
                text = "fadfadfasdfadf"
                if (type(option) is str) or (type(option) is int) or (type(option) is float):
                    text = str(option)
                elif type(option) is Menu:
                    text = str(option.name)
                splash.append(label.Label(terminalio.FONT,
                              text=text, color=0xFFFFFF, x=10, y=5 + i*15))

                if self.curS == i:
                    splash.append(label.Label(terminalio.FONT,
                                  text=">", color=0xFFFFFF, x=0, y=5 + i*15))
            return splash
