import signal
import sys
import time

import serial
from lightController import LightController
from logger import Logger
from messageHandler import MessageHandler
from proxy import Proxy

logger = Logger()

# Initialize the LightController
lightController = LightController('/dev/ttyUSB0', 9600, logger)

# Proxy setup
Proxy0 = Proxy(0, logger)
Proxy1 = Proxy(1, logger)
Proxy2 = Proxy(2, logger)
Proxy3 = Proxy(3, logger)

proxy_list = [Proxy0, Proxy1, Proxy2, Proxy3]
# Initialize the MessageHandler
messageHandler = MessageHandler('test.mosquitto.org', proxy_list, lightController, "dashboardAnimations", "dashboardOverride", logger)

# Start the MessageHandler
messageHandler.start()

# Keep the main thread running
try:
    while True:
        message = input()
        payload = message.split(",")
        if(len(payload) == 3):
            messageHandler.handle_manual_override(message)
        elif(len(payload) == 1):
            try:
                proxy = proxy_list[int(payload[0])]
                print(f"Proxy {proxy.ID} is at position {proxy.position} with state {proxy.state}.")
    
            except (ValueError, TypeError) as e:
                logger.error(f"(safe_int_cast) Failed to cast '{payload}' to int: {e}")
        else:
            print("Invalid input, messages must be in format 'ID,x,y' to override the position or 'ID' to get the position.")
except KeyboardInterrupt:
    # Graceful shutdown on Ctrl+C
    messageHandler.stop()
