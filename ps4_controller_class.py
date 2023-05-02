import json
from pyPS4Controller.controller import Controller
import os
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

    def listen(self, timeout=30, on_connect=None, on_disconnect=None, on_sequence=None):
        """
        Copied as i needed to add the write_json_to_file function
        """
        def on_disconnect_callback():
            self.is_connected = False
            if on_disconnect is not None:
                on_disconnect()

        def on_connect_callback():
            self.is_connected = True
            if on_connect is not None:
                on_connect()

        def wait_for_interface():
            print("Waiting for interface: {} to become available . . .".format(self.interface))
            for i in range(timeout):
                if os.path.exists(self.interface):
                    print("Successfully bound to: {}.".format(self.interface))
                    on_connect_callback()
                    return
                time.sleep(1)
            print("Timeout({} sec). Interface not available.".format(timeout))
            exit(1)

        def read_events():
            try:
                return _file.read(self.event_size)
            except IOError:
                print("Interface lost. Device disconnected?")
                on_disconnect_callback()
                exit(1)

        def check_for(sub, full, start_index):
            return [start for start in range(start_index, len(full) - len(sub) + 1) if
                    sub == full[start:start + len(sub)]]

        def unpack():
            __event = struct.unpack(self.event_format, event)
            return (__event[3:], __event[2], __event[1], __event[0])

        def write_json_to_file(self):
            with open("json_states.json", 'w') as outfile:
                json.dump(self.button_states, outfile)

        wait_for_interface()
        try:
            _file = open(self.interface, "rb")
            event = read_events()
            if on_sequence is None:
                on_sequence = []
            special_inputs_indexes = [0] * len(on_sequence)
            while not self.stop and event:
                (overflow, value, button_type, button_id) = unpack()
                if button_id not in self.black_listed_buttons:
                    self.__handle_event(button_id=button_id, button_type=button_type, value=value, overflow=overflow,
                                        debug=self.debug)
                for i, special_input in enumerate(on_sequence):
                    check = check_for(special_input["inputs"], self.event_history, special_inputs_indexes[i])
                    if len(check) != 0:
                        special_inputs_indexes[i] = check[0] + 1
                        special_input["callback"]()
                event = read_events()
                write_json_to_file()
        except KeyboardInterrupt:
            print("\nExiting (Ctrl + C)")
            on_disconnect_callback()
            exit(1)


if __name__ == "__main__":
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen(timeout=60) # Set timeout to 1 second, allowing the loop in main() to execute

