import signal
import sys
import time

import serial
from lightController import LightController
from messageHandler import MessageHandler

from proxy import Proxy

# Initialize the LightController
lightController = LightController('/dev/ttyUSB0', 9600)

# Proxy setup
Proxy0 = Proxy(0, 0, 0, 0, False, 0)
Proxy1 = Proxy(0, 0, 0, 0, False, 1)
Proxy2 = Proxy(0, 0, 0, 0, False, 2)

# Initialize the MessageHandler
messageHandler = MessageHandler('test.mosquitto.org', [Proxy0, Proxy1, Proxy2], lightController, "dashboardAnimations")

# Start the MessageHandler
messageHandler.start()

# Keep the main thread running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Graceful shutdown on Ctrl+C
    messageHandler.stop()