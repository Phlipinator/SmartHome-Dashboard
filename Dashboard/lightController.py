import threading
import time
from queue import Queue

import serial


class LightController:
    def __init__(self, port, baudrate):
        self.serial_port = serial.Serial(port, baudrate, timeout=1)
        self.message_queue = Queue()
        self.delay = 5  # Minimum delay of 5 seconds between messages
        self.worker_thread = threading.Thread(target=self._send_messages)
        self.worker_thread.daemon = True  # Daemonize the thread so it will automatically stop when the main program exits
        self.worker_thread.start()

    def _send_messages(self):
        while True:
            message = self.message_queue.get()
            self.serial_port.write(message.encode())
            print(f"Message sent: {message}")
            time.sleep(self.delay)

    def send_coordinates(self, x, y):
        message = f"{x},{y}\n"
        self.message_queue.put(message)
        print("Message added to queue.")

    def send_path(self, x1, y1, x2, y2):
        message = f"{x1},{y1},{x2},{y2}\n"
        self.message_queue.put(message)
        print("Message added to queue.")