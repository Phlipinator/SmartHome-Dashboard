import serial

ser = serial.Serial('/dev/ttyUSB1', 9600)

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            print(line)
except KeyboardInterrupt:
    ser.close()
