import smbus
import time

# Create an SMBus instance
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1

# Arduino I2C address (54 in decimal is 0x36 in hexadecimal)
arduino_address = 0x36

def read_from_arduino():
    # Read 8 bytes of data from the address of the Arduino
    data = bus.read_i2c_block_data(arduino_address, 0, 8)
    
    # Extract tile, row, column, and sensor reading from the data
    tile = data[0]
    row = data[1]
    column = data[2]
    sensor_reading = (data[3] << 8) + data[4]  # Combine high and low bytes
    
    # You can process the reserved bytes similarly if needed
    
    return tile, row, column, sensor_reading

while True:
	try:
		tile, row, column, sensor_reading = read_from_arduino()
		print(f"Tile: {tile}, Row: {row}, Column: {column}, Sensor Reading: {sensor_reading}")
	except:
		print("Read error")
	
	time.sleep(2)
