import time
import RPi.GPIO as GPIO

def rc_time(pin):
    count = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.05)

    GPIO.setup(pin, GPIO.IN)
    print("Reading pin {}".format(pin))
    print("GPIO.input(pin): ", GPIO.input(pin))
    if GPIO.input(pin) == GPIO.LOW:
        return 1
    elif GPIO.input(pin) == -GPIO.LOW:
        return -1
    else:
        return 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Assuming the X output of the joystick is connected to GPIO14 and the Y output is connected to GPIO15
x_axis_pin = 14
y_axis_pin = 15

try:
    while True:
        x_axis_value = rc_time(x_axis_pin)
        y_axis_value = rc_time(y_axis_pin)
        print("X-axis: {}, Y-axis: {}".format(x_axis_value, y_axis_value))
        time.sleep(0.2)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting")
