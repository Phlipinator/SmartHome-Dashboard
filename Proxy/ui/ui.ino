#include "config.h"
#include <lvgl.h>
#include <TFT_eSPI.h>
#include <ui.h>
#include <WiFi.h>
#include <PubSubClient.h>

WiFiClient espClient;
PubSubClient client(espClient);

int tileVoltage = 0;
int rowVoltage = 0;
int colVoltage = 0;

// Initialize Text Object
extern lv_obj_t * ui_Text;

volatile int encoderPos = 0;
int lastEncoded = 0;

// Predefined angles that represent the different modes
const int32_t angles[] = { 0, 1190, -1280 };  
int modeIndex = 0;

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
  // Keep track of the last encoder position to detect changes
  static int lastEncoderPos = encoderPos;
  // Flag to decide whether to process this input or not
  static bool processInput = true;         

  int MSB = digitalRead(encoderPinA);      // Most significant bit
  int LSB = digitalRead(encoderPinB);      // Least significant bit
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
  // Convert the incoming message to a string
  String msg = "";
  for (unsigned int i = 0; i < length; i++) {
    msg += (char)message[i];
  }

  // Check if the message is a single digit number (0, 1, or 2)
  if (msg.length() == 1 && isDigit(msg.charAt(0))) {
    int value = msg.toInt();
    
    // Perform actions based on the value
    switch (value) {
      case 0:
        // Network
        lv_img_set_angle(ui_Text, angles[0]);
        break;
      case 1:
        // Third Party
        lv_img_set_angle(ui_Text, angles[1]);
        break;
      case 2:
        // Online
        lv_img_set_angle(ui_Text, angles[2]);
        break;
      default:
        Serial.print("Unsupported message");
        break;
    }
  }
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
      // String payload = String(ID);
      // client.publish(topic.c_str(), payload.c_str());
      // Subscribe to your topics here
      client.subscribe(subTopic.c_str());
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void initDisplay() {
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
}

void initEncoder() {
  // Encoder Init
  pinMode(encoderPinA, INPUT_PULLUP);
  pinMode(encoderPinB, INPUT_PULLUP);

  // Read the initial state
  lastEncoded = (digitalRead(encoderPinA) << 1) | digitalRead(encoderPinB);
}

void initVoltagePins() {
  tileVoltage = analogRead(TILE_PIN);
  rowVoltage = analogRead(ROW_PIN);
  colVoltage = analogRead(COL_PIN);
}

void setup() {
  Serial.begin(9600);

  initDisplay();
  initEncoder();

  // The position information is read once in the beginning of the script, because the ADC pins cannot be used when WiFi is enabled
  delay(1000);
  initVoltagePins();
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

  // Publish if there's a mode change
  if (currentModeIndex != lastModeIndex) {
    String payload = String(tileVoltage) + "," + String(rowVoltage) + "," + String(colVoltage) + "," + String(currentModeIndex);
    client.publish(pubTopic.c_str(), payload.c_str());

    lastModeIndex = currentModeIndex;
  }

  // Small delay to limit the update rate
  delay(5);
}