import time

import serial

# Setup the serial connection
ser = serial.Serial("/dev/ttyUSB1", 9600, timeout=1)


def send_led_position():
    while True:
        coordinates = input(
            "Enter the coordinates of the LED (in the format x,y), or 'exit' to quit: "
        )
        if coordinates.lower() == "exit":
            break
        x, y = coordinates.split(",")
        if x.isdigit() and y.isdigit():
            position = f"{x},{y}\n"
            ser.write(position.encode())
            time.sleep(0.1)  # Give some time for the ESP32 to process the command
        else:
            print("Please enter valid coordinates (in the format x,y) or 'exit'.")


send_led_position()

# Clean up
ser.close()
