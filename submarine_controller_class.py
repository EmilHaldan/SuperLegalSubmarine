import json
from pyPS4Controller.controller import Controller
import os
import time
import struct

class MySubmarineController(Controller):

    def __init__(self,**kwargs):
        Controller.__init__(self, **kwargs)

        self.button_states = {
            "arrow_up": False,
            "arrow_down": False,
            "R3_up": 0,
            "R3_down": 0,
            "R3_left": 0,
            "R3_right": 0
        }

        self.arduino_package = {
            "pressure_target" : 0,
            "forwards_throttle" : 0,
            "sideways_throttle" : 0
        }

    
    ##### CONTROLLER FUNCTIONS #####

    def write_button_states_to_json(self):
        with open("button_states.json", "w") as f:
            json.dump(self.button_states, f)
        print("")
        print("Button States: ")
        print("Arrow up: ", self.button_states["arrow_up"])
        print("Arrow down: ", self.button_states["arrow_down"])
        print("R3 up: ", self.button_states["R3_up"])
        print("R3 down: ", self.button_states["R3_down"])
        print("R3 left: ", self.button_states["R3_left"])
        print("R3 right: ", self.button_states["R3_right"])
        print("")

    def on_up_arrow_press(self):
        self.button_states["arrow_up"] = True
        self.adjust_pressure_target(amount = 0.1)
        self.write_button_states_to_json()
        self.write_package_to_arduino_json()

    def on_down_arrow_press(self):
        self.button_states["arrow_down"] = True
        self.adjust_pressure_target(amount = -0.1)
        self.write_button_states_to_json()
        self.write_package_to_arduino_json()

    def on_up_down_arrow_release(self):
        self.button_states["arrow_up"] = False
        self.button_states["arrow_down"] = False
        self.write_button_states_to_json()

    def on_R3_up(self, value):
        self.button_states["R3_up"] = value
        self.arduino_package["forwards_throttle"] = value # is always positive
        self.write_button_states_to_json()
        self.write_package_to_arduino_json()

    def on_R3_down(self, value):
        self.button_states["R3_down"] = value
        self.arduino_package["forwards_throttle"] = value # is always negative
        self.write_button_states_to_json()
        self.write_package_to_arduino_json()

    def on_R3_left(self, value):
        self.button_states["R3_left"] = value
        self.arduino_package["sideways_throttle"] = value # is always negative
        self.write_button_states_to_json()
        self.write_package_to_arduino_json()

    def on_R3_right(self, value):
        self.button_states["R3_right"] = value
        self.arduino_package["sideways_throttle"] = value # is always positive
        self.write_button_states_to_json()
        self.write_package_to_arduino_json()

    def on_R3_y_at_rest(self):
        self.button_states["R3_up"] = 0
        self.button_states["R3_down"] = 0
        self.button_states["R3_right"] = 0
        self.button_states["R3_left"] = 0
        self.arduino_package["forwards_throttle"] = 0
        self.arduino_package["sideways_throttle"] = 0
        self.write_button_states_to_json()
        self.write_package_to_arduino_json()


    ##### SUBMARINE FUNCTIONS #####
    def adjust_pressure_target(self, amount):
        self.arduino_package["pressure_target"] += amount
        if self.arduino_package["pressure_target"] < 0:
            self.arduino_package["pressure_target"] = 0

    def write_package_to_arduino_json(self):
        with open("arduino_package.json", "w") as f:
            json.dump(self.arduino_package, f)
        print("")
        print("Arduino Package: ")
        print("Pressure Target: ", self.arduino_package["pressure_target"])
        print("Forwards Throttle: ", self.arduino_package["forwards_throttle"])
        print("Sideways Throttle: ", self.arduino_package["sideways_throttle"])
        print("")


if __name__ == "__main__":
    controller = MySubmarineController(interface="/dev/input/js0", 
                                        connecting_using_ds4drv=False)
    controller.listen(timeout=60) # Set timeout to 1 second, allowing the loop in main() to execute

