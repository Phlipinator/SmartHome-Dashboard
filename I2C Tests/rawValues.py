import time

import smbus

# Create an instance of the smbus library
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

# The I2C address of the device
device_address = 0x36  # Change this to your device's address


def read_sensor_data():
    # Read 8 bytes of data from the device
    data = bus.read_i2c_block_data(
        device_address, 0x00, 8
    )  # Assuming 0x00 is the register address to start reading from

    # Combine the received bytes back into integers
    tileInt = (data[0] << 8) | data[1]
    rowInt = (data[2] << 8) | data[3]
    colInt = (data[4] << 8) | data[5]

    # Reserved bytes (data[6] and data[7]) are ignored for now but can be used in the future

    return tileInt, rowInt, colInt


while True:
    try:
        tile, row, col = read_sensor_data()
        print(f"Tile: {tile}, Row: {row}, Column: {col}")
        time.sleep(1)  # Delay for 1 second before reading again
    except:
        print("Read Error")
