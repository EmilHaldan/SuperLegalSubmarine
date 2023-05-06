import time
from RF24 import RF24

# Configuration
RASPBERRY_PI_GPIO_CE = 22
RASPBERRY_PI_GPIO_CSN = 0
CHANNEL = 76

# Initialize the radio module
radio = RF24(RASPBERRY_PI_GPIO_CE, RASPBERRY_PI_GPIO_CSN)
radio.begin()
radio.setChannel(CHANNEL)
radio.setPALevel(3)
radio.setDataRate(RF24.RF24_1MBPS)
radio.setAutoAck(0, 1)
radio.openWritingPipe(0xF0F0F0F0E1)
radio.openReadingPipe(1, 0xF0F0F0F0D2)
radio.startListening()
radio.stopListening()
radio.printDetails()
radio.startListening()

print("Ready to receive data...")

while True:
    while not radio.available():
        time.sleep(0.01)
        
    received_data = []
    radio.read(received_data, 32)
    print("Received data: {}".format(received_data))
    
    # Send an acknowledgment message back
    radio.stopListening()
    radio.write(b"Data received.")
    radio.startListening()
