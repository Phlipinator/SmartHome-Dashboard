# !OLD SCRIPT! OUTDATED!

import time

import smbus

# Create an instance of the smbus library
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

# The I2C address of the device
deviceAddress = 0x36  # Change this to your device's address

tiles = [
    (1000, 1023, 1),
    (952, 999, 2),
    (890, 940, 3),
    (825, 875, 4),
    (556, 616, 5),
    (622, 682, 6),
    (686, 746, 7),
    (752, 812, 8),
    (490, 550, 9),
    (425, 485, 10),
    (356, 416, 11),
    (292, 352, 12),
    (32, 92, 13),
    (100, 160, 14),
    (162, 222, 15),
    (228, 288, 16),
]

columns = [(850, 1023, 1), (550, 849, 2), (250, 549, 3), (0, 249, 4)]

rows = [(1000, 1023, 1), (700, 999, 2), (400, 699, 3), (0, 399, 4)]


def readData():
    # Read 8 bytes of data from the device
    data = bus.read_i2c_block_data(
        deviceAddress, 0x00, 8
    )  # Assuming 0x00 is the register address to start reading from

    # Combine the received bytes back into integers
    tileInt = (data[0] << 8) | data[1]
    rowInt = (data[2] << 8) | data[3]
    colInt = (data[4] << 8) | data[5]

    return tileInt, rowInt, colInt


def convertValue(rawValue, data):
    for lower, upper, number in data:
        if lower <= rawValue <= upper:
            return number
    return 0  # If no range matches


while True:
    try:
        tile, row, col = readData()
        print(
            f"Tile: {convertValue(tile, tiles)}, Row: {convertValue(row, rows)}, Column: {convertValue(col, columns)}"
        )
        time.sleep(1)  # Delay for 1 second before reading again
    except Exception as e:
        print(f"Read Error: {e}")
        time.sleep(1)  # Delay for 1 second before reading again
