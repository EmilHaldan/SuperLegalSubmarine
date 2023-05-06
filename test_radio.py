import time
from RF24 import RF24, RF24_PA_LOW

# Configure the Raspberry Pi pins for the NRF24L01 module
RPI_CE_PIN = 25
RPI_CSN_PIN = 0

# Configure the NRF24L01 addresses and channel
ADDRESS = b"submne"
CHANNEL = 76

# Create an instance of the NRF24L01 module
radio = RF24(RPI_CE_PIN, RPI_CSN_PIN)

# Initialize the NRF24L01 module
radio.begin()
radio.set_channel(CHANNEL)
radio.set_pa_level(RF24_PA_LOW)
radio.set_data_rate(1)
radio.set_crc_length(2)
radio.set_address_width(5)

# Set the addresses for RX and TX pipes
radio.open_writing_pipe(ADDRESS)
radio.open_reading_pipe(1, ADDRESS)

# Set the radio to listen
radio.start_listening()

def send_data(data):
    radio.stop_listening()
    success = radio.write(data)
    radio.start_listening()
    return success

def receive_data():
    if radio.available():
        received_data = []
        radio.read(received_data, radio.get_dynamic_payload_size())
        return received_data
    else:
        return None

def main():
    while True:
        # Send data to the Arduino Uno
        data_to_send = b"Hello, Submarine!"
        if send_data(data_to_send):
            print("Data sent: ", data_to_send)

        # Receive data from the Arduino Uno
        received_data = receive_data()
        if received_data is not None:
            print("Data received: ", received_data)

        time.sleep(1)

if __name__ == '__main__':
    main()
