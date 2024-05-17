import time

import serial


class LightController:
    def __init__(self, port, baudrate):
        self.serial_port = serial.Serial(port, baudrate, timeout=1)
    
    def send_coordinates(self, x, y):
        message = f"{x},{y}\n"
        self.serial_port.write(message.encode())
    
    def send_rectangle(self, x1, y1, x2, y2):
        message = f"{x1},{y1},{x2},{y2}\n"
        self.serial_port.write(message.encode())
