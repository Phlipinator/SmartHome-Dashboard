#ifndef CONFIG_H
#define CONFIG_H

// CHANGE PROXY ID HERE
const int ID = 1;
const String topic = "Proxy" + String(ID);

// WIFI Credentials
const char* ssid = "Dashboard";
const char* password = "muchPrivate";

// MQTT Broker settings
const char* mqtt_server = "192.168.4.1";
const int mqtt_port = 1883;
const char* mqtt_user = "";
const char* mqtt_password = "";

// Initialize Position Pins
const byte TILE_PIN = 25;
const byte ROW_PIN = 32;
const byte COL_PIN = 33;

// Initialize Encoder Pins
const int encoderPinA = 27;
const int encoderPinB = 14;

// Screen resolution
static const uint16_t screenWidth = 240;
static const uint16_t screenHeight = 240;

#endif // CONFIG_H