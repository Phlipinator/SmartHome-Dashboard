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


def calculateVoltage(rawValue, type):
    adc = (rawValue / 4095.0) * 3.3
    if type == "tile":
        return adc * 1.68
    else:
        return adc * 1.51


tileList = [
    # Row 1
    (5.0, 1),
    (4.4, 2),
    (4.0, 3),
    (3.64, 4),
    # Row 2
    (3.3, 8),
    (3.0, 7),
    (2.68, 6),
    (2.36, 5),
    # Row 3
    (2.0, 9),
    (1.8, 10),
    (1.5, 11),
    (1.22, 12),
    # Row 4
    (0.94, 16),
    (0.66, 15),
    (0.38, 14),
    (0.1, 13),
]

rowList = [
    (4.9, 1),
    (3.0, 2),
    (1.75, 3),
    (0.4, 4),
]

colList = [
    (4.8, 1),
    (4.0, 2),
    (3.5, 3),
    (3.0, 4),
]


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
        print(
            "Tile: "
            + str(
                convertValue(
                    calculateVoltage(tileValue, "tile"), tileList, tileThreshold
                )
            )
        )
        print(
            "Row: "
            + str(
                convertValue(calculateVoltage(rowValue, "row"), rowList, rowThreshold)
            )
        )
        print(
            "Column: "
            + str(
                convertValue(calculateVoltage(colValue, "col"), colList, colThreshold)
            )
        )
        time.sleep(1)  # Delay for 1 second before reading again
    except Exception as e:
        print(f"Read Error: {e}")
        time.sleep(1)  # Delay for 1 second before reading again
