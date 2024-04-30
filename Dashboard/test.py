import time

import smbus
from proxy import Proxy

# Create an instance of the smbus library
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

proxy = Proxy(0x36, bus)  # Device I2C address
position = proxy.get_position()
print(position)
