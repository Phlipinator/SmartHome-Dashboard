import time

from config import Config


class Proxy:
    def __init__(self, bus, address):
        """
        Initialize the Proxy object.

        Args:
            bus: The bus object used for I2C communication.
            address: The address of the proxy device.
        """
        self.bus = bus
        self.address = address
        self.is_plugged_in = False
        self.position = None
        self.state = None
        self.config = Config()

    def check_connection(self):
        """
        Check if the proxy is connected to the dashboard.
        """
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

    def read_proxy_data(self):
        """
        Read data from the proxy at the specified device address.

        Returns:
            The data read from the proxy as a triple of tile, row, and column values.
            Returns None if the proxy is not plugged in.
        """
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

    def calculate_voltage(self, raw_value, type):
        """
        Calculate the voltage based on the type of voltage divider.

        Args:
            raw_value: The raw value read from the ADC.
            type: The type of voltage divider ("tile", "row", or "col").

        Returns:
            The calculated voltage.
        """
        adc = (raw_value / 4095.0) * 3.3
        if type == "tile":
            return adc * 1.68
        elif type == "row":
            return adc * 1.51
        elif type == "col":
            return adc * 1.51
        return adc

    def convert_value(self, raw_value, type):
        """
        Match the correct position based on the voltage.

        Args:
            raw_value: The raw value read from the ADC.
            type: The type of voltage divider ("tile", "row", or "col").

        Returns:
            The matched position number.
            Returns 0 if no range matches.
        """
        voltage = self.calculate_voltage(raw_value, type)
        data_list = getattr(self.config, f"{type}List")
        threshold = self.config.thresholds[type]

        for voltage_level, number in data_list:
            if voltage_level - threshold <= voltage <= voltage_level + threshold:
                return number
        return 0

    def apply_adjustments(self, tile, row, col):
        """
        Apply adjustments to the row and column values based on the tile number.
        Converts the relative position on the board to the absolute position.

        Args:
            tile: The tile number.
            row: The original row value.
            col: The original column value.

        Returns:
            The adjusted row and column values as an absolute position of the dashboard
        """
        if tile > 0:
            row_adjustment, col_adjustment = self.config.adjustmentTable[tile - 1]
            adjusted_row = row + row_adjustment
            adjusted_col = col + col_adjustment
            return adjusted_row, adjusted_col
        return row, col

    def get_position(self):
        """
        Get the position of the proxy.

        Returns:
            The position of the proxy as a tuple of row and column values.
            Returns None if the proxy is not connected or if there are too many read failures.
        """
        self.check_connection()

        last_values = None
        consistent_count = 0
        failure_count = 0

        while consistent_count < 3:
            if failure_count >= 5:
                print("Exceeded maximum number of read failures.")
                return None

            data = self.read_proxy_data()
            if data is None:
                print("Failed to receive data, attempting again...")
                failure_count += 1
                time.sleep(1)
                continue

            tile_value, row_value, col_value = data
            tile = self.convert_value(tile_value, "tile")
            row = self.convert_value(row_value, "row")
            col = self.convert_value(col_value, "col")
            values = (tile, row, col)

            if last_values == values:
                consistent_count += 1
            else:
                last_values = values
                consistent_count = 1

            time.sleep(1)

        if tile > 0:
            return self.apply_adjustments(tile, row, col)

        return None
