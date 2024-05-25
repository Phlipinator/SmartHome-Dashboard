import signal
import sys
import time

import serial
from lightController import LightController
from logger import Logger
from messageHandler import MessageHandler
from proxy import Proxy

logger = Logger("test.log")

# Initialize the LightController
lightController = LightController('/dev/ttyUSB0', 9600, logger)

# Proxy setup
Proxy0 = Proxy(0)
Proxy1 = Proxy(1)
Proxy2 = Proxy(2)
Proxy3 = Proxy(3)

# Initialize the MessageHandler
messageHandler = MessageHandler('test.mosquitto.org', [Proxy0, Proxy1, Proxy2, Proxy3], lightController, "dashboardAnimations", logger)

# Start the MessageHandler
messageHandler.start()

# Keep the main thread running
try:
    while True:
        message = input("Input manual position override in format 'ID,row,col' ")
        payload = message.split(",")
        print(payload)
except KeyboardInterrupt:
    # Graceful shutdown on Ctrl+C
    messageHandler.stop()
