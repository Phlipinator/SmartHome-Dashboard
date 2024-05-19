import paho.mqtt.client as mqtt
from lightController import LightController

from proxy import Proxy


class MessageHandler:
    def __init__(self, broker_address, proxy_list, light_controller, animationTopic):
        self.broker_address = broker_address
        self.proxy_list = proxy_list
        self.light_controller = light_controller
        self.animationTopic = animationTopic
        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
    
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # Subscribe to set_state and is_state topics for each proxy
        for proxy in self.proxy_list:
            set_state_topic = f"set_state_proxy_{proxy.ID}"
            is_state_topic = f"is_state_proxy_{proxy.ID}"
            client.subscribe(set_state_topic)
            client.subscribe(is_state_topic)
            print(f"Subscribed to {set_state_topic} and {is_state_topic}")
        client.subscribe(self.animationTopic)
        print(f"Subscribed to {self.animationTopic}")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"Message received on topic {topic}: {payload}")
        if(topic == self.animationTopic):
           self.handle_animation(payload)
        else:
            self.handle_message(topic, payload)

    def handle_message(self, topic, payload):
        # Extract the proxy ID from the topic
        parts = topic.split("_")
        proxy_ID = int(parts[-1])
        
        # Find the proxy
        proxy = next((p for p in self.proxy_list if p.ID == proxy_ID), None)
        
        if proxy is None:
            print(f"Proxy with ID {proxy_ID} not found.")
            return
        
        # Store the old position and state
        old_position = proxy.position
        old_state = proxy.state
        
        # Process based on topic type
        if parts[0] == "set":
            data = payload.split(",")

            if len(data) != 4:
                print("Invalid payload format for 'set' message.")
                return
            
            tile_value = int(data[0])
            row_value = int(data[1])
            col_value = int(data[2])
            state = int(data[3])
            
            # Update the proxy with the new position and state
            proxy.update(tile_value, row_value, col_value, state, True)
            print(f"Updated Proxy {proxy_ID} with TileValue {tile_value}, rowValue {row_value}, colValue {col_value}, and State {state}.")
            
            # Compare the new position and state with the old values
            if (tile_value, row_value, col_value) != old_position or state != old_state:
                # Call a function to handle the change
                self.handle_proxy_change(proxy)
                
        elif parts[0] == "is":
            try:
                state = int(payload)
            except ValueError:
                print("Invalid payload format for 'is' message.")
                return
            
            # Update the proxy state
            proxy.state = state
            print(f"Updated Proxy {proxy_ID} State {state}.")
            
            # Compare the new state with the old value
            if state != old_state:
                # Call a function to handle the change
                self.handle_proxy_change(proxy)
        else:
            print("Invalid topic.")

    def handle_proxy_change(self, proxy):
        # Function to handle the change in position or state of the proxy
        print(f"Proxy {proxy.ID} position or state has changed. Handling the change...")
        # Add your logic to handle the change here

    def handle_animation(self, payload):
        data = payload.split(",")
        if len(data) != 2:
            print("Invalid payload format for animation message.")
            return

        start_proxy = next((p for p in self.proxy_list if p.ID == int(data[0])), None)
        end_proxy = next((p for p in self.proxy_list if p.ID == int(data[1])), None)

        if start_proxy is None or end_proxy is None:
            print("Proxy IDs not connected")
            return

        # Extracting x and y coordinates from the position tuple
        start_x, start_y = start_proxy.position
        end_x, end_y = end_proxy.position

        print("Sending path from Proxy {start_proxy.ID} to Proxy {end_proxy.ID}")
        self.light_controller.send_path(start_x, start_y, end_x, end_y)

    def start(self):
        self.client.connect(self.broker_address)
        self.client.loop_start()