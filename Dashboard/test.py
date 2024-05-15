import serial

from proxy import Proxy

# Serial connection setup
positionSerial = serial.Serial('/dev/ttyUSB1', 9600)

# Dictionary to keep track of Proxy instances
proxies = {}

try:
    while True:
        if positionSerial.in_waiting > 0:
            line = positionSerial.readline().decode('utf-8').strip()
            print(f"Received: {line}")
            parts = line.split(',')
            if len(parts) == 5:
                proxy_id_str, tile_str, row_str, col_str, state_str = parts
                # Convert numeric values from strings to integers
                tile = int(tile_str)
                row = int(row_str)
                col = int(col_str)
                state = int(state_str)
                
                # Check if it's formatted as "Proxy<ID>"
                if proxy_id_str.startswith("Proxy") and proxy_id_str[5:].isdigit():
                    proxy_id = proxy_id_str
                    if proxy_id not in proxies:
                        # Create new Proxy instance if it does not exist
                        proxies[proxy_id] = Proxy(tile, row, col, state, True)
                        print(f"Created new {proxy_id} with tile={tile}, row={row}, col={col}, state={state}")
                    else:
                        # Update existing Proxy instance
                        proxy = proxies[proxy_id]
                        proxy.update(tile, row, col, state, True)  # Assuming the Proxy class has an update method
                        print(f"Updated {proxy_id} with tile={tile}, row={row}, col={col}, state={state}")
except KeyboardInterrupt:
    print("Closing serial connection...")
    positionSerial.close()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    positionSerial.close()
