import time
from gpiozero import MCP3008

adc = MCP3008(channel=0, device=0)  # Configure the MCP3008 ADC

# Assuming GPIO14 is connected to CH2 and GPIO15 is connected to CH3 on the MCP3008
gpio14_channel = 8
gpio15_channel = 10

try:
    while True:
        gpio14_voltage = adc(channel = gpio14_channel).value * 3.3  # Convert the ADC reading to voltage (0-3.3V)
        gpio15_voltage = adc(channel = gpio15_channel).value * 3.3  # Convert the ADC reading to voltage (0-3.3V)
        
        print("GPIO14 Voltage: {:.2f}V, GPIO15 Voltage: {:.2f}V".format(gpio14_voltage, gpio15_voltage))
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Exiting")



# import spidev
# import time

# def read_adc(adc, channel):
#     if (channel > 7) or (channel < 0):
#         return -1

#     r = adc.xfer2([1, (8 + channel) << 4, 0])
#     data = ((r[1] & 3) << 8) + r[2]
#     return data

# spi = spidev.SpiDev()
# spi.open(0, 0)
# spi.max_speed_hz = 1000000

# x_axis_channel = 0
# y_axis_channel = 1

# try:
#     while True:
#         x_axis_value = read_adc(spi, x_axis_channel)
#         y_axis_value = read_adc(spi, y_axis_channel)
#         print("X-axis: {}, Y-axis: {}".format(x_axis_value, y_axis_value))
#         time.sleep(0.2)
# except KeyboardInterrupt:
#     spi.close()

