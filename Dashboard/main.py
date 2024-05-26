import signal
import sys
import time

import serial
from config import Config
from lightController import LightController
from logger import Logger
from messageHandler import MessageHandler
from proxy import Proxy

logger = Logger("test.log")
config = Config()

# Initialize the LightController
lightController = LightController('/dev/ttyUSB0', 9600, logger)

# Proxy setup
Proxy0 = Proxy(0, config)
Proxy1 = Proxy(1, config)
Proxy2 = Proxy(2, config)
Proxy3 = Proxy(3, config)

proxy_list = [Proxy0, Proxy1, Proxy2, Proxy3]
# Initialize the MessageHandler
messageHandler = MessageHandler('test.mosquitto.org', proxy_list, lightController, "dashboardAnimations", logger, config)

# Start the MessageHandler
messageHandler.start()

# Keep the main thread running
try:
    while True:
        message = input()
        payload = message.split(",")
        if(len(payload) == 3):
            proxy = proxy_list[int(payload[0])]
            proxy_position = int(payload[1]), int(payload[2])
            messageHandler.handle_manual_override(proxy, proxy_position)
        elif(len(payload) == 1):
            proxy = proxy_list[int(payload[0])]
            print(f"Proxy {proxy.ID} is at position {proxy.position} with state {proxy.state}.")
        else:
            print("Invalid input, messages must be in format 'ID,x,y' to override the position or 'ID' to get the position.")
except KeyboardInterrupt:
    # Graceful shutdown on Ctrl+C
    messageHandler.stop()
