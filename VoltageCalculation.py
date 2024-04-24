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


# Calculates the actual Voltage level from the raw value
def calculateVoltage(rawValue, type):
    adc = (rawValue / 4095.0) * 3.3
    if type == "tile":
        return adc * 1.68
    else:
        return adc * 1.51


# Stores adjustments for each tile in the format (row, column)
adjustmentTable = [
    # Row 1
    (0, 0),  # Tile 1
    (0, 4),  # Tile 2
    (0, 8),  # Tile 3
    (0, 12),  # Tile 4
    # Row 2
    (4, 0),  # Tile 5
    (4, 4),  # Tile 6
    (4, 8),  # Tile 7
    (4, 12),  # Tile 8
    # Row 3
    (8, 0),  # Tile 9
    (8, 4),  # Tile 10
    (8, 8),  # Tile 11
    (8, 12),  # Tile 12
    # Row 4
    (12, 0),  # Tile 13
    (12, 4),  # Tile 14
    (12, 8),  # Tile 15
    (12, 12),  # Tile 16
]


# Stores the voltage values for each tile
tileList = [
    # Row 1
    (5.0, 4),
    (4.4, 3),
    (4.0, 2),
    (3.64, 1),
    # Row 2
    (3.3, 5),
    (3.0, 6),
    (2.68, 7),
    (2.36, 8),
    # Row 3
    (2.0, 12),
    (1.8, 11),
    (1.5, 10),
    (1.22, 9),
    # Row 4
    (0.94, 13),
    (0.66, 14),
    (0.38, 15),
    (0.1, 16),
]

# Stores the voltage values for each row
rowList = [
    (4.9, 1),
    (3.0, 2),
    (1.75, 3),
    (0.4, 4),
]

# Stores the voltage values for each column
colList = [
    (4.8, 1),
    (4.3, 2),
    (3.7, 3),
    (3.2, 4),
]


# Converts the raw value to a number based on the voltage list
def convertValue(rawValue, dataList, threshold):
    for voltage, number in dataList:
        if voltage - threshold <= rawValue <= voltage + threshold:
            return number
    return 0  # If no range matches


tileThreshold = 0.15
rowThreshold = 0.5
colThreshold = 0.4

while True:
    try:
        tileValue, rowValue, colValue = read_sensor_data()

        tile = convertValue(
            calculateVoltage(tileValue, "tile"), tileList, tileThreshold
        )
        row = convertValue(calculateVoltage(rowValue, "row"), rowList, rowThreshold)
        col = convertValue(calculateVoltage(colValue, "col"), colList, colThreshold)

        # For Debugging
        # print(str(row) + "," + str(col) + "," + str(tile))

        # Retrieve row and col adjustments based on the tile number
        row_adjustment, col_adjustment = adjustmentTable[tile - 1]

        # Apply adjustments
        row += row_adjustment
        col += col_adjustment

        print("(" + str(row) + "," + str(col) + ")")

        time.sleep(1)  # Delay for 1 second before reading again
    except Exception as e:
        print(f"Read Error: {e}")
        time.sleep(1)  # Delay for 1 second before reading again
