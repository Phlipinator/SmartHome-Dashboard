import paho.mqtt.client as mqtt


class MessageHandler:
    """
    A class that handles MQTT messages and performs actions based on the received messages.

    Args:
        broker_address (str): The address of the MQTT broker.
        proxy_list (list): The list of used proxy objects.
        light_controller (object): The objects that controls the light animations.
        animationTopic (str): The general topic for animation messages from the hub.
        logger (Logger): The logger object for logging messages.

    Attributes:
        broker_address (str): The address of the MQTT broker.
        proxy_list (list): A list of proxy objects.
        light_controller (object): The objects that controls the light animations.
        animationTopic (str): The general topic for animation messages from the hub.
        proxy_data (list): A list that stores the data for each proxy for comparison.
        client (mqtt.Client): The MQTT client.

    """

    def __init__(self, broker_address, proxy_list, light_controller, animationTopic, logger, config):
        self.broker_address = broker_address
        self.proxy_list = proxy_list
        self.light_controller = light_controller
        self.animationTopic = animationTopic
        self.logger = logger
        self.config = config

        # Initialize proxy_data with one (0, 0, 0) tuple for each element in proxy_list
        self.proxy_data = [(0, 0, 0) for _ in proxy_list]
        
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
        self.logger.info(f"(on_connect) Connected with result code {rc}")
        # Subscribe to set_state and is_state topics for each proxy
        for proxy in self.proxy_list:
            proxy_state_update_topic = f"proxy_state_update_proxy_{proxy.ID}"
            hub_state_update_topic = f"hub_state_update_proxy_{proxy.ID}"
            client.subscribe(proxy_state_update_topic)
            client.subscribe(hub_state_update_topic)
            self.logger.info(f"(on_connect) Subscribed to {proxy_state_update_topic} and {hub_state_update_topic}")

            # Subscribe to general animation topic for the hub
        client.subscribe(self.animationTopic)
        self.logger.info(f"(on_connect) Subscribed to {self.animationTopic}")

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
        self.logger.info(f"(on_message) Message received on topic {topic}: {payload}")

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
            self.logger.warning(f"(handle_message) Proxy with ID {proxy_ID} not found.")
            return
        
        # Process based on topic type
        if parts[0] == "proxy":
            data = payload.split(",")

            if len(data) != 4:
                self.logger.warning(f"(handle_message) Invalid payload '{payload}' format for 'set' message.")
                return
            
            if(data[3] == "x"):
                proxy.update(int(data[0]), int(data[1]), int(data[2]), True, False)
                # Set override back to False, as the state can only be 'x' if the Proxy get freshly plugged in
                proxy.override = False
            else:
                # If the override flag is set, do not update the position
                if(proxy.override):
                    proxy.state = int(data[3])
                    return
                
                proxy.update(int(data[0]), int(data[1]), int(data[2]), True, int(data[3]))
                
            self.compare_proxy_data(proxy, "proxy")

            self.logger.info(f"(handle_message) Updated Proxy {proxy_ID} with TileValue {data[0]}, rowValue {data[1]}, colValue {data[2]} and State {data[3]}.")
            
        elif parts[0] == "hub":
            try:
                proxy.state = int(payload)
            except ValueError:
                self.logger.warning(f"(handle_message) Invalid payload '{payload}' format for 'is' message.")
                return
            
            proxy.isConnected = True
            self.compare_proxy_data(proxy, "hub")
            self.logger.info(f"(handle_message) Updated Proxy {proxy_ID} with State {payload}.")
        else:
            self.logger.warning(f"(handle_message) Invalid topic '{topic}'.")

    def compare_proxy_data(self, proxy, change_type):
        """
        Compares the data of the proxy with the stored proxy data and performs actions based on the change type.

        Args:
            proxy (object): The proxy object.
            changeType (str): The type of change (either "proxy" or "hub").

        """
        if change_type == "proxy":
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
        elif change_type == "hub":
            if(proxy.state != self.proxy_data[proxy.ID][2]):
                self.handle_animation(f"0, {proxy.ID}", "path")
                self.update_proxy_data(proxy)
            else:
                return
        else:
            self.logger.warning(f"(compare_proxy_data) Invalid change type '{change_type}'.")

    def update_proxy_data(self, proxy):
        """
        Updates the stored proxy data with the data from the proxy object.

        Args:
            proxy (object): The proxy object.

        """
        if(proxy.position is None):
            self.proxy_data[proxy.ID] = (None, None, proxy.state)
            return

        proxy_row, proxy_col = proxy.position
        self.proxy_data[proxy.ID] = (proxy_row, proxy_col, proxy.state)

    def handle_animation(self, payload, animation_type):
        """
        Handles the animation based on the payload and animation type.

        Args:
            payload (str): The payload of the animation.
            animationType (str): The type of animation (either "path" or "coordinates").

        """
        if animation_type == "path":
            data = payload.split(",")
            if len(data) != 2:
                self.logger.warning(f"(handle_animation) Invalid payload '{payload}' format for path animation.")
                return

            start_proxy = next((p for p in self.proxy_list if p.ID == int(data[0])), None)
            end_proxy = next((p for p in self.proxy_list if p.ID == int(data[1])), None)

            if start_proxy is None or end_proxy is None:
                self.logger.warning(f"(handle_animation) Proxy IDs '{start_proxy.ID}' or '{end_proxy.ID}' not connected.")
                return
            
            if(start_proxy.position is None or end_proxy.position is None):
                self.logger.warning(f"(handle_animation) Proxy positions for Proxy IDs '{start_proxy.ID}' or '{end_proxy.ID}' not set.")
                return
            
            if(not start_proxy.is_plugged_in or not end_proxy.is_plugged_in):
                self.logger.warning(f"(handle_animation) Proxies '{start_proxy.ID}' or '{end_proxy.ID}' not connected.")
                return
            
            # Extracting x and y coordinates from the position tuple
            start_x, start_y = start_proxy.position
            end_x, end_y = end_proxy.position

            self.logger.info(f"(handle_animation) Sending path from Proxy {start_proxy.ID} to Proxy {end_proxy.ID}.")
            self.light_controller.send_path(start_x, start_y, end_x, end_y)

        elif animation_type == "coordinates":
            if len(str(payload)) != 1:
                self.logger.warning(f"(handle_animation) Invalid payload '{payload}' format for coordinates animation.")
                return
            
            proxy = next((p for p in self.proxy_list if p.ID == int(payload)), None)

            if proxy is None:
                self.logger.warning(f"(handle_animation) Proxy with ID {proxy.ID} not found.")
                return
            
            if (proxy.position is None):
                self.logger.warning(f"(handle_animation) Position for Proxy with ID {proxy.ID} not set.")
                return
            
            if(not proxy.is_plugged_in):
                self.logger.warning(f"(handle_animation) Proxy with ID {proxy.ID} not connected.")
                return
            
            self.logger.info(f"(handle_animation) Sending coordinates for Proxy {proxy.ID}.")
            self.light_controller.send_coordinates(proxy.position[0], proxy.position[1])

        else:
            self.logger.warning(f"(handle_animation) Invalid animation type '{animation_type}'.")

    def handle_manual_override(self, proxy, proxy_position):
        """
        Handles manual override of a proxy.

        Args:
            proxy (Proxy): The proxy object to override.
            proxy_position (str): The new position of the proxy.

        """
        proxy.override = True
        proxy.position = proxy_position
        self.handle_animation(proxy.ID, "coordinates")
        self.logger.info(f"(handle_manual_override) Manual override for Proxy {proxy.ID} with position {proxy_position}.")

    def get_proxy_number(self):
        """
        Returns the number of connected proxies.

        Returns:
            int: The number of proxies.

        """
        proxy_number = 0
        for proxy in self.proxy_list:
            if proxy.is_plugged_in:
                proxy_number += 1
        return proxy_number
    
    def adapt_voltages(self):
        threshold = 0.1 * self.get_proxy_number()
        for i in range(len(self.config.tileList)):
            value, index = self.config.tileList[i]
            self.config.tileList[i] = (value - threshold, index)

    def start(self):
        """
        Starts the message handler.

        """
        self.client.connect(self.broker_address)
        self.client.loop_start()
        self.logger.info("Message Handler started.")

    def stop(self):
        """
        Stops the message handler and disconnects from the MQTT broker.

        """
        self.client.loop_stop()
        self.client.disconnect()
        self.logger.info("Message Handler stopped.")
