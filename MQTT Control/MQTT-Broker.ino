#include <Arduino.h>
#include <WiFi.h>
#include <PicoMQTT.h>

PicoMQTT::Server mqtt;  // Initialize MQTT server object

void setup() {
    // Initialize Serial for debugging
    Serial.begin(9600);
    
    // Set WiFi in AP mode
    WiFi.mode(WIFI_AP);
    WiFi.softAP("Dashboard", "muchPrivate");

    // Print the IP address of the ESP32
    // IPAddress IP = WiFi.softAPIP();
    // Serial.print("AP IP address: ");
    // Serial.println(IP);
    // IP: 192.168.4.1

    // Subscribe to a topic pattern and attach a callback
    mqtt.subscribe("#", [](const char* topic, const char* payload) {
        // Print received message to Serial
        Serial.printf("%s,%s\n", topic, payload);
    });

    // Start the MQTT broker
    mqtt.begin();
}

void loop() {
    // This handles client connections and messages
    mqtt.loop();
}
