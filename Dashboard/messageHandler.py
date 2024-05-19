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
        
        # Process based on topic type
        if parts[0] == "set":
            data = payload.split(",")

            if len(data) != 4:
                print("Invalid payload format for 'set' message.")
                return
            
            proxy.update(int(data[0]), int(data[1]), int(data[2]), int(data[3]), True)
            print(f"Updated Proxy {proxy_ID} with TileValue {data[0]}, rowValue {data[1]}, colValue {data[2]} and State {data[3]}.")
            
        elif parts[0] == "is":
            try:
                proxy.state = int(payload)
            except ValueError:
                print("Invalid payload format for 'is' message.")
                return
            print(f"Updated Proxy {proxy_ID} State {payload}.")
        else:
            print("Invalid topic.")

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

        # Debug output
        print("Start Proxy Position:", start_proxy.position)
        print("End Proxy Position:", end_proxy.position)

        # Extracting x and y coordinates from the position attribute
        start_x, start_y = map(int, start_proxy.position.split(','))
        end_x, end_y = map(int, end_proxy.position.split(','))

        # Debug output
        print("Start Position (x, y):", start_x, start_y)
        print("End Position (x, y):", end_x, end_y)

        self.light_controller.send_path(start_x, start_y, end_x, end_y)


    def start(self):
        self.client.connect(self.broker_address)
        self.client.loop_start()