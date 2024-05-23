# Instructions
The *LED_Controller.ino* file can be uploaded to an ESP32 mircocontroller.
The LED-Strip is connected to *GPIO 5* and the Relay to *GPIO 13*
The *LED_Commander.py* file can be used for testing, to send coordinates manually via USB serial from a raspberry pi using python.
## Functionality
The code features a 2D array, that stores the unique positions of either 1 or 2 LEDs per field. Through serial it can take 2 types of arguments:
- A single coordinate to animate a plug-in animation in the format *x,y*
- Two sets of coordinates to animate a path from one position to the other in the format *x1,y1,x2,y2*