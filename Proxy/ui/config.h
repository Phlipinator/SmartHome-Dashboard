#ifndef CONFIG_H
#define CONFIG_H

// CHANGE PROXY ID HERE
const int ID = 1;
const String pubTopic = "set_state_proxy_" + String(ID);
const String subTopic = "is_state_proxy_" + String(ID);

const char* ssid = "DashboardAP";
const char* password = "";

// MQTT broker credentials
const char* mqtt_server = "";
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