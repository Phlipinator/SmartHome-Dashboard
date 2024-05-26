#ifndef CONFIG_H
#define CONFIG_H

// CHANGE PROXY ID HERE
const int ID = 0;
const String pubTopic = "proxy_state_update_proxy_" + String(ID);

const char* ssid = "DashboardAP";
const char* password = "muchPrivate";

// MQTT broker credentials
const char* mqtt_server = "test.mosquitto.org";
const char* mqtt_user = "";
const char* mqtt_password = "";

// Initialize Position Pins
const byte TILE_PIN = 25;
const byte ROW_PIN = 32;
const byte COL_PIN = 33;

#endif // CONFIG_H