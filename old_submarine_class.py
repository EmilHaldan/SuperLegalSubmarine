import pandas as pd
import numpy as np 
import math
import os 


class Submarine:
    def __init__(self, body_voulme, syringe_capacity, water_density=1,
                dry_mass = None, syringe_volume = None):
        self.altitude = 0
        self.body_density = 0
        self.SIZE = body_voulme
        self.SYRINGE_CAPACITY = syringe_capacity
        self.water_density = water_density
        
        if syringe_volume is None:
            self.syringe_mass = self.SYRINGE_CAPACITY/2 * water_density
            self.syringe_volume = self.SYRINGE_CAPACITY/2
        else: 
            self.syringe_volume = syringe_volume
            self.syringe_mass = syringe_volume * water_density

        if dry_mass is None:
            self.current_mass = self.SIZE * self.water_density
            self.dry_mass = self.current_mass - self.syringe_mass
        else: 
            self.dry_mass = self.current_mass - self.syringe_mass
            self.current_mass = dry_mass + self.syringe_mass

        self.vertical_speed = 0
        self.target_pressure = 0
        print("Expected dry mass: ", self.dry_mass)
        print("Mass for stable body_density: ", self.current_mass)
        
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

    def estimate_vertical_speed(self):
        """
        Calculates the estimated velocity of a body with changing body_density in water.
        
        Parameters:
            depth (float): The depth of the body in the water in meters.
            density_water (float): The density of the water in kg/m^3.
            density_body (float): The density of the body in kg/m^3.
            mass (float): The mass of the body in kg.
            volume (float): The volume of the body in m^3.
        
        Returns:
            The estimated velocity of the body in m/s.
        """
        
        # Calculate the gravitational force acting on the body.
        gravitational_force = self.current_mass * 9.81
        
        # Calculate the volume of water displaced by the body.
        volume_displaced = self.SIZE
        
        # Calculate the buoyant force acting on the body.
        buoyant_force = volume_displaced * self.water_density * 9.81
        
        # Calculate the net force acting on the body.
        net_force = buoyant_force - gravitational_force
        
        # Calculate the acceleration of the body.
        acceleration = net_force / self.current_mass
        
        # Calculate the estimated velocity of the body.
        if acceleration > 0:
            direction = 1
        else: 
            direction = -1

        velocity = math.sqrt(2 * abs(acceleration))
        
        self.vertical_speed = velocity * direction

    def estimate_depth(current_pressure):
        # https://www.convertworld.com/en/pressure/metre-of-water.html
        pass

    def set_target_pressure(self, current_pressure):
        pass
        self.target_pressure = 0.1





if __name__ == "__main__":
    submarine_volume = 3.6 #6.500 # in Liters (L/1000 = cc)
    syringe_capacity = 0.06 #0.100 # in Liters (L/1000 = cc)

    submarine = Submarine(body_voulme=submarine_volume, syringe_capacity=syringe_capacity)
