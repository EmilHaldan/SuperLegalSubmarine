from pyPS4Controller.controller import Controller
import time

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

    def on_up_arrow_press(self):
        self.button_states["arrow_up"] = True

    def on_up_arrow_release(self):
        self.button_states["arrow_up"] = False

    def on_down_arrow_press(self):
        self.button_states["arrow_down"] = True

    def on_down_arrow_release(self):
        self.button_states["arrow_down"] = False

    def on_R3_up(self, value):
        self.button_states["R3_up"] = value

    def on_R3_down(self, value):
        self.button_states["R3_down"] = value

    def on_R3_left(self, value):
        self.button_states["R3_left"] = value

    def on_R3_right(self, value):
        self.button_states["R3_right"] = value

def main(controller):
    while True:
        # Your code that uses the controller button states
        if controller.button_states["arrow_up"]:
            print("Arrow up TRUE.")
        else: 
            print("Arrow up False.")
        if controller.button_states["arrow_down"]:
            print("Arrow DOWN TRUE.")
        else: 
            print("Arrow DOWN False.")
        print("R3 Up:", controller.button_states["R3_up"])
        print("R3 Down:", controller.button_states["R3_down"])
        print("R3 Left:", controller.button_states["R3_left"])
        print("R3 Right:", controller.button_states["R3_right"])
        time.sleep(0.2)

if __name__ == "__main__":
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.start()
    try:
        main(controller)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        controller.stop()
