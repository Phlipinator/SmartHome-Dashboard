# Tangible SmartHome Dashboard
This repository contains the code as well as all resources for my masters-thesis regarding a tangible SmartHome Dashboard.
This file will explain the general file-structure, but the user-guides for each part of the project will be included in separate README files in each of the sub-folders.
## Dashboard
Contains the code than runs on the Raspberry Pi 4B.
## LED Control
Contains the LED-Control Code for the ESp32 that is connected to a relay and the Neopixel LED-Strips, as well as a simple testing script for sending messages via serial from the Pi.
## Proxy
Contains the code with all libraries for all 4 Proxies.
- 0: Contains a broken down version of the Proxy Code that just publishes the position once and then goes into deep-sleep to conserve energy.
- 1: Lamp Icon
- 2: Plug Icon
- 3: Sensor Icon
## CAD
Contains STL files for all relevant parts of the prototype as well as a Fusion360 file.