#include "config.h"

#include <WiFi.h>
#include <PubSubClient.h>

WiFiClient espClient;
PubSubClient client(espClient);

int tileVoltage = 0;
int rowVoltage = 0;
int colVoltage = 0;

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  // Set the Wi-Fi mode
  WiFi.mode(WIFI_STA);

  // Set the minimum security level
  WiFi.setMinSecurity(WIFI_AUTH_WPA_PSK);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a unique client ID
    String clientId = "Dashboard_Proxy_" + String(ID);
    // Attempt to connect
    if (client.connect(clientId.c_str(), mqtt_user, mqtt_password)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void initVoltagePins() {
  tileVoltage = analogRead(TILE_PIN);
  rowVoltage = analogRead(ROW_PIN);
  colVoltage = analogRead(COL_PIN);
}

void setup() {
  Serial.begin(9600);

  // The position information is read once in the beginning of the script, because the ADC pins cannot be used when WiFi is enabled
  delay(1000);
  initVoltagePins();
  delay(1000);

  setup_wifi();
  client.setServer(mqtt_server, 1883);

  // Publish the initial state once when powered on
  if (!client.connected()) {
    reconnect();
  }

  if (client.connected()) {
    String payload = String(tileVoltage) + "," + String(rowVoltage) + "," + String(colVoltage) + ",x";
    client.publish(pubTopic.c_str(), payload.c_str());
    Serial.println("Message published, going to deep sleep...");
    delay(1000); // Give some time for the message to be sent
    esp_deep_sleep_start(); // Enter deep sleep mode
  }
}

void loop() {
  // The loop function is not needed as we enter deep sleep in the setup function
}
