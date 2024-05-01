import time

from config import Config


class Proxy:
    def __init__(self, bus, address):
        self.bus = bus
        self.address = address
        self.is_plugged_in = False
        self.position = None
        self.state = None
        self.config = Config()

    # Check if the proxy is connected to the dashboard
    def check_connection(self):
        attempts = 3
        for _ in range(attempts):
            try:
                self.bus.read_i2c_block_data(self.address, 0x00, 8)
                self.is_plugged_in = True
                print("Proxy is connected.")
                return  # Exit if successful
            except IOError:
                time.sleep(1)  # Wait a second and try again
        self.is_plugged_in = False  # Set to false if all attempts fail

    # Read data from the proxy at the specified device address
    def read_proxy_data(self):
        if not self.is_plugged_in:
            return None
        try:
            data = self.bus.read_i2c_block_data(self.address, 0x00, 8)
            tileInt = (data[0] << 8) | data[1]
            rowInt = (data[2] << 8) | data[3]
            colInt = (data[4] << 8) | data[5]

            return tileInt, rowInt, colInt
        except IOError as e:
            print(f"Read Error: {e}")
            return None

    # Calculate the voltage based the type of voltage divider
    def calculate_voltage(self, raw_value, type):
        adc = (raw_value / 4095.0) * 3.3
        if type == "tile":
            return adc * 1.68
        elif type == "row":
            return adc * 1.51
        elif type == "col":
            return adc * 1.51
        return adc

    # Match the correct position based on th voltage
    def convert_value(self, raw_value, type):

        voltage = self.calculate_voltage(raw_value, type)
        # Get the list of data based on the type
        data_list = getattr(self.config, f"{type}List")
        threshold = self.config.thresholds[type]

        for voltage_level, number in data_list:
            if voltage_level - threshold <= voltage <= voltage_level + threshold:
                return number
        return 0  # If no range matches

    # Function to get the position of the proxy
    def get_position(self):
        # First check connection to the device
        self.check_connection()
        data = self.read_proxy_data()

        if data is None:
            print("No data received from the device or device not connected.")
            return None  # Exit the function if no data is received

        tile_value, row_value, col_value = data  # Now it's safe to unpack

        tile = self.convert_value(tile_value, "tile")
        row = self.convert_value(row_value, "row")
        col = self.convert_value(col_value, "col")

        # Retrieve and apply row and column adjustments based on the tile number
        if tile > 0:  # Assuming tile numbering starts at 1
            row_adjustment, col_adjustment = self.config.adjustmentTable[tile - 1]
            adjusted_row = row + row_adjustment
            adjusted_col = col + col_adjustment
            return adjusted_row, adjusted_col
        return None
