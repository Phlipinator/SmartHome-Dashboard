import paho.mqtt.client as mqtt
from lightController import LightController

from proxy import Proxy


class MessageHandler:
    def __init__(self, broker_address, proxy_list, light_controller):
        self.broker_address = broker_address
        self.proxy_list = proxy_list
        self.light_controller = light_controller
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

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"Message received on topic {topic}: {payload}")
        self.handle_message(topic, payload)