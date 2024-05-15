import time

from config import Config


class Proxy:
    def __init__(self, tile, row, col, state, pluggedIn):
        """
        Initialize the Proxy object.

        Args:
            tile: The raw value read from the ADC for the tile.
            row: The raw value read from the ADC for the row.
            col: The raw value read from the ADC for the column.
            state: The state of the proxy
            pluggedIn: A boolean indicating if the proxy is plugged in or not.
        """
        self.position = None
        self.tileValue = tile
        self.rowValue = row
        self.colValue = col
        self.state = state
        self.is_plugged_in = pluggedIn
        self.config = Config()

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
        return None

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
        if self.is_plugged_in:
            tile = self.convert_value(self.tileValue, "tile")
            row = self.convert_value(self.rowValue, "row")
            col = self.convert_value(self.colValue, "col")

            if tile > 0:
                self.position = self.apply_adjustments(tile, row, col)
                return self.position

            self.position = row, col
            return self.position
        return None
