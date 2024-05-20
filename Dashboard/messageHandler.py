import paho.mqtt.client as mqtt


class MessageHandler:
    """
    A class that handles MQTT messages and performs actions based on the received messages.

    Args:
        broker_address (str): The address of the MQTT broker.
        proxy_list (list): The list of used proxy objects.
        light_controller (object): The objects that controls the light animations.
        animationTopic (str): The general topic for animation messages from the hub.

    Attributes:
        broker_address (str): The address of the MQTT broker.
        proxy_list (list): A list of proxy objects.
        light_controller (object): The objects that controls the light animations.
        animationTopic (str): The general topic for animation messages from the hub.
        proxy_data (list): A list that stores the data for each proxy for comparison.
        client (mqtt.Client): The MQTT client.

    """

    def __init__(self, broker_address, proxy_list, light_controller, animationTopic):
        self.broker_address = broker_address
        self.proxy_list = proxy_list
        self.light_controller = light_controller
        self.animationTopic = animationTopic

        self.proxy_data = [
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
        ]

        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
    
    def on_connect(self, client, userdata, flags, rc):
        """
        Callback function that is called when the MQTT client is connected to the broker.

        Args:
            client (mqtt.Client): The MQTT client.
            userdata: User-defined data.
            flags: Response flags from the broker.
            rc (int): The connection result code.

        """
        print("Connected with result code " + str(rc))
        # Subscribe to set_state and is_state topics for each proxy
        for proxy in self.proxy_list:
            set_state_topic = f"set_state_proxy_{proxy.ID}"
            is_state_topic = f"is_state_proxy_{proxy.ID}"
            client.subscribe(set_state_topic)
            client.subscribe(is_state_topic)
            print(f"Subscribed to {set_state_topic} and {is_state_topic}")
            # Subscribe to general animation topic for the hub
        client.subscribe(self.animationTopic)
        print(f"Subscribed to {self.animationTopic}")

    def on_message(self, client, userdata, msg):
        """
        Callback function that is called when a message is received.

        Args:
            client (mqtt.Client): The MQTT client.
            userdata: User-defined data.
            msg (mqtt.MQTTMessage): The received message.

        """
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"Message received on topic {topic}: {payload}")
        if(topic == self.animationTopic):
           self.handle_animation(payload, "path")
        else:
            self.handle_message(topic, payload)

    def handle_message(self, topic, payload):
        """
        Handles the received message based on the topic and payload.

        Args:
            topic (str): The topic of the received message.
            payload (str): The payload of the received message.

        """
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
            self.compare_proxy_data(proxy, "set")

            print(f"Updated Proxy {proxy_ID} with TileValue {data[0]}, rowValue {data[1]}, colValue {data[2]} and State {data[3]}.")
            
        elif parts[0] == "is":
            try:
                proxy.state = int(payload)
            except ValueError:
                print("Invalid payload format for 'is' message.")
                return
            self.compare_proxy_data(proxy, "set")
            print(f"Updated Proxy {proxy_ID} State {payload}.")
        else:
            print("Invalid topic.")

    def compare_proxy_data(self, proxy, changeType):
        """
        Compares the data of the proxy with the stored proxy data and performs actions based on the change type.

        Args:
            proxy (object): The proxy object.
            changeType (str): The type of change (either "set" or "is").

        """
        if changeType == "set":
            # Extracting x and y coordinates from the position tuple
            proxy_row, proxy_col = proxy.position

            if(proxy_row != self.proxy_data[proxy.ID][0] or proxy_col != self.proxy_data[proxy.ID][1]):
                self.handle_animation(proxy.ID, "coordinates")
                self.update_proxy_data(proxy)

            elif(proxy.state != self.proxy_data[proxy.ID][2]):
                self.handle_animation(f"{proxy.ID}, 0", "path")
                self.update_proxy_data(proxy)
            else:
                return
        elif changeType == "is":
            if(proxy.state != self.proxy_data[proxy.ID][2]):
                self.handle_animation(f"0, {proxy.ID}", "path")
                self.update_proxy_data(proxy)
            else:
                return
        else:
            print("Invalid change type.")

    def update_proxy_data(self, proxy):
        """
        Updates the stored proxy data with the data from the proxy object.

        Args:
            proxy (object): The proxy object.

        """
        proxy_row, proxy_col = proxy.position
        self.proxy_data[proxy.ID] = (proxy_row, proxy_col, proxy.state)

    def handle_animation(self, payload, animationType):
        """
        Handles the animation based on the payload and animation type.

        Args:
            payload (str): The payload of the animation.
            animationType (str): The type of animation (either "path" or "coordinates").

        """
        if animationType == "path":
            data = payload.split(",")
            if len(data) != 2:
                print("Invalid payload format for path animation.")
                return

            start_proxy = next((p for p in self.proxy_list if p.ID == int(data[0])), None)
            end_proxy = next((p for p in self.proxy_list if p.ID == int(data[1])), None)

            if start_proxy is None or end_proxy is None:
                print("Proxy IDs not connected")
                return
            
            if(start_proxy.position == None or end_proxy.position == None):
                print("Proxy positions not set")
                return
            
            # Extracting x and y coordinates from the position tuple
            start_x, start_y = start_proxy.position
            end_x, end_y = end_proxy.position

            print(f"Sending path from Proxy {start_proxy.ID} to Proxy {end_proxy.ID}")
            self.light_controller.send_path(start_x, start_y, end_x, end_y)

        elif animationType == "coordinates":
            if len(str(payload)) != 1:
                print("Invalid payload format for coordinates animation.")
                return
            
            proxy = next((p for p in self.proxy_list if p.ID == int(payload)), None)

            if proxy is None:
                print("Proxy ID not found.")
                return
            
            if (proxy.position == None):
                print("Proxy position not set.")
                return
            
            print("Sending coordinates for Proxy {proxy.ID}.")
            self.light_controller.send_coordinates(proxy.position[0], proxy.position[1])

        else:
            print("Invalid animation type.")

    def start(self):
        """
        Starts the message handler.

        """
        self.client.connect(self.broker_address)
        self.client.loop_start()

    def stop(self):
        """
        Stops the message handler and disconnects from the MQTT broker.

        """
        self.client.loop_stop()
        self.client.disconnect()