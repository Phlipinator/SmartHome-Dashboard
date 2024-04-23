# !OLD SCRIPT! OUTDATED!

import time

import smbus

# Create an instance of the smbus library
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

# The I2C address of the device
deviceAddress = 0x36  # Change this to your device's address

tiles = [
    # Row 1
    (4095, 3500, 1),  # For 4095
    (3549, 3000, 2),  # For 3202
    (2999, 2800, 3),  # For 2915
    (2799, 2550, 4),  # For 2685
    # Row 2
    (2549, 2350, 8),  # For 2433
    (2349, 2100, 7),  # For 2230
    (2099, 1850, 6),  # For 1990
    (1849, 1650, 5),  # For 1770
    # Row 3
    (1649, 1450, 9),  # For 1550
    (1449, 1280, 10),  # For 1344
    (1279, 1050, 11),  # For 1177
    (1049, 770, 12),  # For 917
    # Row 4
    (769, 600, 16),  # For 700
    (599, 350, 15),  # For 499
    (349, 150, 14),  # For 290
    (149, 0, 13),  # For 66
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
    for upper, lower, number in data:
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
