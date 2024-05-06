#include <lvgl.h>
#include <TFT_eSPI.h>
#include <ui.h>
#include <WiFi.h>
#include <PubSubClient.h>

// WIFI Credentials
const char* ssid = "SSID";
const char* password = "PW";

// MQTT Broker settings
const char* mqtt_server = "BROKER";
const int mqtt_port = 1883;
const char* mqtt_user = "USER";
const char* mqtt_password = "PW";

WiFiClient espClient;
PubSubClient client(espClient);

const int ID = 1;
const String topic = "Proxy" + String(ID);

// Initialize Position Pins
const byte TILE_PIN = 25;
const byte ROW_PIN = 32;
const byte COL_PIN = 33;

int tileVoltage = 0;
int rowVoltage = 0;
int colVoltage = 0;

// Initialize Text Object
extern lv_obj_t * ui_Text;

// Initialize Encoder Pins
const int pinA = 27;  // Encoder pin A
const int pinB = 14;  // Encoder pin B

volatile int encoderPos = 0;
int lastEncoded = 0;

// Predefined angles that represent the different modes
const int32_t angles[] = { 0, 1190, -1280 };  
int modeIndex = 0;

// Screen resolution
static const uint16_t screenWidth = 240;
static const uint16_t screenHeight = 240;

static lv_disp_draw_buf_t draw_buf;
static lv_color_t buf[screenWidth * screenHeight / 10];

TFT_eSPI tft = TFT_eSPI(screenWidth, screenHeight);  // TFT instance

/* Display flushing */
void my_disp_flush(lv_disp_drv_t* disp, const lv_area_t* area, lv_color_t* color_p) {
  uint32_t w = (area->x2 - area->x1 + 1);
  uint32_t h = (area->y2 - area->y1 + 1);

  tft.startWrite();
  tft.setAddrWindow(area->x1, area->y1, w, h);
  tft.pushColors((uint16_t*)&color_p->full, w * h, true);
  tft.endWrite();

  lv_disp_flush_ready(disp);
}

void incrementalEncoder() {
  static int lastEncoderPos = encoderPos;  // Keep track of the last encoder position to detect changes
  static bool processInput = true;         // Flag to decide whether to process this input or not

  int MSB = digitalRead(pinA);             // Most significant bit
  int LSB = digitalRead(pinB);             // Least significant bit
  int encoded = (MSB << 1) | LSB;          // Combining the two bits
  int sum = (lastEncoded << 2) | encoded;  // Adding it to the previous encoded value

  if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011 || sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) {
    if (processInput) {
      // Determine direction and increment or decrement encoderPos accordingly
      if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011)
        encoderPos--;
      else if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000)
        encoderPos++;

      // Only process this input, next one will be skipped
      processInput = false;
    } else {
      // Skip this input, next one will be processed
      processInput = true;
    }
  }

  lastEncoded = encoded;  // Store this value for next time

  // If encoderPos has changed significantly (ignoring every second input), update UI
  if (!processInput && encoderPos != lastEncoderPos) {
    const int numModes = sizeof(angles) / sizeof(angles[0]);

    // Adjust the mode index based on the encoder position
    modeIndex = encoderPos % numModes;
    if (modeIndex < 0)
      modeIndex += numModes;  // Ensure modeIndex is positive

    // Snap rotation to the nearest predefined angle
    lv_img_set_angle(ui_Text, angles[modeIndex]);

    lastEncoderPos = encoderPos;  // Update last position for next comparison
  }
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

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

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  for (unsigned int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
  }
  Serial.println();
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a unique client ID
    String clientId = "ESP32Client-" + String((uint32_t)ESP.getEfuseMac(), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str(), mqtt_user, mqtt_password)) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      String payload = String(ID);
      client.publish(topic.c_str(), payload.c_str());
      // Subscribe to your topics here
      // client.subscribe("yourSubscriptionTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying, non-blocking wait could be implemented here
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(9600);

  lv_init();

  tft.begin();         // TFT init
  tft.setRotation(2);  // Set right Orientation

  lv_disp_draw_buf_init(&draw_buf, buf, NULL, screenWidth * screenHeight / 10);

  // Initialize the display
  static lv_disp_drv_t disp_drv;
  lv_disp_drv_init(&disp_drv);
  disp_drv.hor_res = screenWidth;
  disp_drv.ver_res = screenHeight;
  disp_drv.flush_cb = my_disp_flush;
  disp_drv.draw_buf = &draw_buf;
  lv_disp_drv_register(&disp_drv);

  // Touch input driver initialization has been removed here

  ui_init();

  // Encoder Init
  pinMode(pinA, INPUT_PULLUP);
  pinMode(pinB, INPUT_PULLUP);

  // Read the initial state
  lastEncoded = (digitalRead(pinA) << 1) | digitalRead(pinB);

  // The position information is read once in the beginning of the script, because the ADC pins cannot be used when WiFi is enabled
  delay(1000);
  tileVoltage = analogRead(TILE_PIN);
  rowVoltage = analogRead(ROW_PIN);
  colVoltage = analogRead(COL_PIN);
  delay(1000);

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  lv_timer_handler();  // Let LVGL do its work

  incrementalEncoder();  // Encoder Interpretation

  // Attempt to reconnect if the client is not connected
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Initialize to -1 to ensure it triggers the first time
  static int lastModeIndex = -1;  

  int currentModeIndex = modeIndex;

  // Publish if there's a significant change
  if (currentModeIndex != lastModeIndex) {
    String payload = String(tileVoltage) + "," + String(rowVoltage) + "," + String(colVoltage) + "," + String(currentModeIndex);
    client.publish(topic.c_str(), payload.c_str());

    lastModeIndex = currentModeIndex;
  }

  // Small delay to limit the update rate
  delay(5);
}