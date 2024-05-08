#ifndef CONFIG_H
#define CONFIG_H

// CHANGE PROXY ID HERE
const int ID = 1;
const String topic = "Proxy" + String(ID);

// WIFI Credentials
const char* ssid = "SSID";
const char* password = "PW";

// MQTT Broker settings
const char* mqtt_server = "BROKER";
const int mqtt_port = 1883;
const char* mqtt_user = "USER";
const char* mqtt_password = "PW";

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