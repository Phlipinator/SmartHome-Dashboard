import serial
from lightController import LightController
from messageHandler import MessageHandler

from proxy import Proxy

lightController = LightController('/dev/ttyUSB0', 9600)


# Proxy setup
Proxy0 = Proxy(0, 0, 0, 0, False, 0)
Proxy1 = Proxy(0, 0, 0, 0, False, 1)
Proxy2 = Proxy(0, 0, 0, 0, False, 2)

messageHandler = MessageHandler('test.mosquitto.org', [Proxy0, Proxy1, Proxy2], lightController)