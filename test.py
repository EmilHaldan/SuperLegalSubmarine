import time
import RPi.GPIO as GPIO

def rc_time(pin):
    count = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(pin, GPIO.IN)
    while GPIO.input(pin) == GPIO.LOW:
        count += 1

    return count

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
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting")
