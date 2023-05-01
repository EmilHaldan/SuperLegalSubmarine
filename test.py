import spidev
import time

def read_adc(adc, channel):
    if (channel > 7) or (channel < 0):
        return -1

    r = adc.xfer2([1, (8 + channel) << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

x_axis_channel = 0
y_axis_channel = 1

try:
    while True:
        x_axis_value = read_adc(spi, x_axis_channel)
        y_axis_value = read_adc(spi, y_axis_channel)
        print("X-axis: {}, Y-axis: {}".format(x_axis_value, y_axis_value))
        time.sleep(0.2)
except KeyboardInterrupt:
    spi.close()
