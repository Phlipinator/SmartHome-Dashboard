# This script is just an example serial communication script that sends messages to the ESP32 from the Raspberry Pi

import time

import serial

# Setup the serial connection
ser = serial.Serial("/dev/ttyUSB1", 9600, timeout=1)


def send_message():
    print("Enter your message. Press 'enter' to send.")
    print("Enter 'exit' to quit.")

    while True:
        message = input("Message: ")

        if message.lower() == "exit":
            break

        # Send message
        ser.write(f"{message}\n".encode())
        time.sleep(0.1)


send_message()

# Clean up
ser.close()
