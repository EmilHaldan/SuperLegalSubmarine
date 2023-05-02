import json
from pyPS4Controller.controller import Controller
import os
import time
import struct

class MySubmarineController(Controller):

    def __init__(self, body_voulme, syringe_capacity,
                dry_mass, water_density=1,**kwargs):
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
            "syringe_target" : 0,
            "forwards_throttle" : 0,
            "sideways_throttle" : 0
        }

        self.depth = 0
        self.body_density = 0
        self.SIZE = body_voulme
        self.water_density = water_density
         
        self.SYRINGE_CAPACITY = syringe_capacity
        self.syringe_volume = 0
        self.syringe_mass = 0

        self.dry_mass = dry_mass
        self.current_mass = dry_mass + self.syringe_mass

        self.vertical_speed = 0
        self.target_pressure = 0
    
    ##### CONTROLLER FUNCTIONS #####
    def write_json_to_file(self):
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


    ##### SUBMARINE FUNCTIONS #####
    def print_status(self):
        print("Current mass: ", self.current_mass)
        print("Current body_density: ", self.body_density)
        print("Current Syringe volume: ", self.syringe_volume)
        print("Current Syringe mass: ", self.syringe_mass)

    def update_syringe_mass(self):
        self.syringe_mass = self.syringe_volume * self.water_density

    def adjust_water(self, amount):
        if amount > 0:
            if amount > self.SYRINGE_CAPACITY - self.syringe_volume:
                self.syringe_volume = self.SYRINGE_CAPACITY
                print("!!! WARNING !!! SYRINGE STATUS: Syringe capacity is full.")
            else:
                self.syringe_volume += amount
        if amount < 0:
            if abs(amount) > self.syringe_volume:
                self.syringe_volume = 0
                print("!!! WARNING !!! SYRINGE STATUS: Syringe is empty.")
            else:
                self.syringe_volume += amount 
        else: 
            pass # no changes 

        self.adjust_body_density()
        self.estimate_vertical_speed()

    def adjust_body_density(self):
        self.adjust_mass()
        self.body_density = self.current_mass / self.SIZE

    def adjust_mass(self):
        self.update_syringe_mass()
        self.current_mass = self.dry_mass + (self.syringe_mass * self.water_density)

    def estimate_depth(current_pressure):
        # https://www.convertworld.com/en/pressure/metre-of-water.html
        pass

    def set_target_pressure(self, current_pressure):
        pass
        self.target_pressure = 0.1



if __name__ == "__main__":
    controller = MySubmarineController(interface="/dev/input/js0", 
                                        connecting_using_ds4drv=False,
                                        body_voulme = 2.7, 
                                        syringe_capacity = 0.06,
                                        dry_mass = 2.67)
    controller.listen(timeout=60) # Set timeout to 1 second, allowing the loop in main() to execute

