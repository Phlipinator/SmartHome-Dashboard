# Instructions
## Code
To start the program, just execute the *main.py* file.
By default there are 4 Proxies, including the hub, to change that you need to create a new Proxy object, with unique ID and pass it on to the message handler.

The rest of the code is documented well and should be self-explanatory.
## LED Controller
For the LED-control to work properly, you need to modify some settings in the configurations, so the ESP gets always registered on the same serial.
Instructions on how to do that can be found [here](https://medium.com/@fredbonjour/connect-multiple-micro-controllers-to-one-raspberry-pi-over-usb-with-a-reliable-identification-21e41db514a7).

## Log
During execution the program automatically adds every event into a log-file. Make sure to change the output location in the *main.py* file.
The Line should look like this:

**logger = Logger("test.log")**