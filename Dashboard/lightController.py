import threading
import time
from queue import Queue

import serial


class LightController:
    """
    A class that controls the communication with the light controller ESP32.

    Args:
        port (str): The serial port to connect to.
        baudrate (int): The baud rate for the serial communication (should be 9600).
        logger (Logger): The logger object for logging messages.

    Attributes:
        serial_port (serial.Serial): The serial port object for communication.
        message_queue (Queue): A queue to store the messages to be sent.
        logger (Logger): The logger object for logging messages.
        delay (int): The minimum delay (in seconds) between sending messages.
        worker_thread (threading.Thread): The thread for sending messages.

    """

    def __init__(self, port, baudrate, logger):
        self.serial_port = serial.Serial(port, baudrate, timeout=1)
        self.message_queue = Queue()
        self.logger = logger
        self.delay = 5  # Minimum delay of 5 seconds between messages
        self.worker_thread = threading.Thread(target=self._send_messages)
        self.worker_thread.daemon = True  # Daemonize the thread so it will automatically stop when the main program exits
        self.worker_thread.start()

    def _send_messages(self):
        """
        A private method that continuously sends messages from the message queue.

        """
        while True:
            message = self.message_queue.get()
            self.serial_port.write(message.encode())
            self.logger.info(f"(send_messages) Message sent: {message}")
            time.sleep(self.delay)

    def send_coordinates(self, x, y):
        """
        Adds a message with the given coordinates to the message queue.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.

        """
        message = f"{x},{y}\n"
        self.message_queue.put(message)
        self.logger.info("(send_coordinates) Coordinates Message added to queue.")

    def send_path(self, x1, y1, x2, y2):
        """
        Adds a message with the given path coordinates to the message queue.

        Args:
            x1 (int): The x-coordinate of the starting point.
            y1 (int): The y-coordinate of the starting point.
            x2 (int): The x-coordinate of the ending point.
            y2 (int): The y-coordinate of the ending point.

        """
        message = f"{x1},{y1},{x2},{y2}\n"
        self.message_queue.put(message)
        self.logger.info("(send_path) Path Message added to queue.")

    def send_boot(self):
        """
        Adds a message for the boot-animation to start
        
        """
        message = "boot"
        self.message_queue.put(message)
        self.logger.info("(send_path) Path Message added to queue.")
            