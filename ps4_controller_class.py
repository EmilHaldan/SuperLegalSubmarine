import time
from pyPS4Controller.controller import Controller



class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_up_arrow_press(self):
        return "arrow up pressed"

    def on_down_arrow_press(self):
        return "arrow down pressed"

    def on_R3_left(self):
        return self.value

    def on_R3_right(self):
        return self.value


if __name__ == "__main__":

    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)#, event_definition=MyEventDefinition)
    controller.debug = True  # you will see raw data stream for any button press, even if that button is not mapped
    # you can start listening before controller is paired, as long as you pair it within the timeout window
    controller.listen(timeout=60)