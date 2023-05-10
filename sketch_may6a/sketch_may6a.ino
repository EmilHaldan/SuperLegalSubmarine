#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

// Configure the Arduino Uno pins for the NRF24L01 module
const uint8_t CE_PIN = 9;
const uint8_t CSN_PIN = 10;

// Configure the NRF24L01 addresses and channel
const uint64_t ADDRESS = 0x7375626D6E; // "submne" in hexadecimal
const uint8_t CHANNEL = 76;

// Create an instance of the NRF24L01 module
RF24 radio(CE_PIN, CSN_PIN);

void setup() {
  Serial.begin(9600);
  
  // Initialize the NRF24L01 module
  radio.begin();
  radio.setChannel(CHANNEL);
  radio.setPALevel(RF24_PA_LOW);
  radio.setDataRate(RF24_1MBPS);
  radio.setCRCLength(RF24_CRC_8);
  radio.setAddressWidth(5);

  // Set the addresses for RX and TX pipes
  radio.openWritingPipe(ADDRESS);
  radio.openReadingPipe(1, ADDRESS);

  // Set the radio to listen
  radio.startListening();
}

void loop() {
  // Receive data from the Raspberry Pi
  if (radio.available()) {
    char received_data[32] = {0};
    radio.read(&received_data, sizeof(received_data));
    Serial.print("Data received: ");
    Serial.println(received_data);
  }

  // Send data to the Raspberry Pi
  radio.stopListening();
  const char* data_to_send = "Hello, Raspberry Pi!";
  bool success = radio.write(&data_to_send, sizeof(data_to_send));
  radio.startListening();

  if (success) {
    Serial.print("Data sent: ");
    Serial.println(data_to_send);
  }

  delay(1000);
}
