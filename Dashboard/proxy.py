import time

from config import Config


class Proxy:
    """
    A class that stores the relevant data for a Proxy device.

    Args:
        ID (int): The unique identifier for the proxy.

    Attributes:
        position (tuple): The position of the proxy (initially None).
        tile_value (int): The tile value associated with the proxy (initially None).
        row_value (int): The row value associated with the proxy (initially None).
        col_value (int): The column value associated with the proxy (initially None).
        state (int): The state of the proxy (initially None).
        is_plugged_in (bool): Indicates whether the proxy is plugged in (initially None).
        config (Config): The configuration object for the proxy.
        override (bool): Indicates if the proxy is in override mode (initially False).
        ID (int): The unique identifier for the proxy.
        logger (Logger): The logger object for the proxy.
    """
    def __init__(self, ID, logger):
        self.position = None
        self.tile_value = None
        self.row_value = None
        self.col_value = None
        self.state = None
        self.is_plugged_in = None
        self.config = Config()
        self.override = False
        self.ID = ID
        self.logger = logger
        

    def update(self, tile, row, col, plugged_in, state = False):
        """
        Update the values of the proxy.

        Args:
            tile: The raw value read from the ADC for the tile.
            row: The raw value read from the ADC for the row.
            col: The raw value read from the ADC for the column.
            state: The state of the proxy
            pluggedIn: A boolean indicating if the proxy is plugged in or not.
        """
        self.tile_value = tile
        self.row_value = row
        self.col_value = col
        self.is_plugged_in = plugged_in

        if state is not False:
            self.state = state

        self.set_position()

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

        # Find the closest voltage match
        closest_match = min(data_list, key=lambda x: abs(x[0] - voltage))

        if type == "tile":
            for voltage_level, number in data_list:
                if voltage_level - 0.25 <= voltage <= voltage_level + 0.05:
                    return number

            self.logger.warning("(convert_value) Returning fallback value for tile")
            return closest_match[1]
        
        else:
            for voltage_level, number in data_list:
                if voltage_level - 1 <= voltage <= voltage_level + 0.05:
                    return number

            self.logger.warning(f"(convert_value) Returning fallback value for {type}")
            return closest_match[1]


    def apply_adjustments(self, tile, row, col):
        """
        Apply adjustments to the row and column numbers based on the tile number.
        Converts the relative position on the board to the absolute position.

        Args:
            tile: The (absolute) tile number.
            row: The relative row number.
            col: The relative column number.

        Returns:
            The adjusted row and column values as an absolute position of the dashboard
        """
        if tile > 0:
            row_adjustment, col_adjustment = self.config.adjustmentTable[tile - 1]
            adjusted_row = row + row_adjustment
            adjusted_col = col + col_adjustment
            return adjusted_row, adjusted_col
        return row, col

    def set_position(self):
        """
        Get the position of the proxy.

        Returns:
            The position of the proxy as a tuple of row and column values.
            Returns None if the proxy is not connected or if there are too many read failures.
        """
        if self.is_plugged_in:
            tile = self.convert_value(self.tile_value, "tile")
            row = self.convert_value(self.row_value, "row")
            col = self.convert_value(self.col_value, "col")

            if tile > 0:
                self.position = self.apply_adjustments(tile, row, col)
                return

            self.position = row, col
            return
