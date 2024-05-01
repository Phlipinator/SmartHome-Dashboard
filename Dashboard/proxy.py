import time

import smbus
from config import Config


class Proxy:
    def __init__(self, bus, address):
        self.bus = bus
        self.address = address
        self.is_plugged_in = False
        self.position = None
        self.state = None
        self.config = Config()

    def read_proxy_data(self):
        # if not self.is_plugged_in:
        #     return None
        try:
            # Read data from the proxy at the specified device address
            data = self.bus.read_i2c_block_data(self.address, 0x00, 8)
            tileInt = (data[0] << 8) | data[1]
            rowInt = (data[2] << 8) | data[3]
            colInt = (data[4] << 8) | data[5]

            return tileInt, rowInt, colInt
        except IOError as e:
            print(f"Read Error: {e}")
            return None
