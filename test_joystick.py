import time
from pyPS4Controller.controller import Controller



class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.target_pressure = 0
        self.target_pressure_delta = 0.01

    def on_up_arrow_press(self):
        self.target_pressure -= self.target_pressure_delta
        print(f"Target pressure level DECREASED by {self.target_pressure_delta} to: {self.target_pressure}")

    def on_down_arrow_press(self):
        self.target_pressure += self.target_pressure_delta
        print(f"Target pressure level INCREASE by {self.target_pressure_delta} to: {self.target_pressure}")

    def on_R3_left(self, value):
        print(f"Steering to the LEFT with {value} power")

    def on_R3_right(self, value):
        print(f"Steering to the RIGHT with {value} power")


if __name__ == "__main__":

    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False, event_definition=MyEventDefinition)
    controller.debug = True  # you will see raw data stream for any button press, even if that button is not mapped
    # you can start listening before controller is paired, as long as you pair it within the timeout window
    controller.listen(timeout=60)