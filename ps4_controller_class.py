import json
from pyPS4Controller.controller import Controller
import os
import time
import struct

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.button_states = {
            "arrow_up": False,
            "arrow_down": False,
            "R3_up": 0,
            "R3_down": 0,
            "R3_left": 0,
            "R3_right": 0,
        }
        
    def write_json_to_file(self):
        with open("button_states.json", "w") as f:
            json.dump(self.button_states, f)

    def on_up_arrow_press(self):
        self.button_states["arrow_up"] = True
        self.write_json_to_file()

    def on_up_arrow_release(self):
        self.button_states["arrow_up"] = False
        self.write_json_to_file()

    def on_down_arrow_press(self):
        self.button_states["arrow_down"] = True
        self.write_json_to_file()

    def on_down_arrow_release(self):
        self.button_states["arrow_down"] = False
        self.write_json_to_file()

    def on_R3_up(self, value):
        self.button_states["R3_up"] = value
        self.write_json_to_file()

    def on_R3_down(self, value):
        self.button_states["R3_down"] = value
        self.write_json_to_file()

    def on_R3_left(self, value):
        self.button_states["R3_left"] = value
        self.write_json_to_file()

    def on_R3_right(self, value):
        self.button_states["R3_right"] = value
        self.write_json_to_file()


if __name__ == "__main__":
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen(timeout=60) # Set timeout to 1 second, allowing the loop in main() to execute

