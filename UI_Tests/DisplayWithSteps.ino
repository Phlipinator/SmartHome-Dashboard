#include <lvgl.h>
#include <TFT_eSPI.h>
#include <ui.h>

// Debugging
bool encoderDebug = false;
bool positionDebugging = false;

/*Don't forget to set Sketchbook location in File/Preferences to the path of your UI project (the parent folder of this INO file)*/

// Initialize Text Object
extern lv_obj_t *ui_Text;

// Initialize Encoder Pins
const int pinA = 15; // Encoder pin A
const int pinB = 2;  // Encoder pin B

volatile int encoderPos = 0;
int lastEncoded = 0;

int modeIndex = 0; // Index of the current mode

// Screen resolution
static const uint16_t screenWidth = 240;
static const uint16_t screenHeight = 240;

static lv_disp_draw_buf_t draw_buf;
static lv_color_t buf[screenWidth * screenHeight / 10];

TFT_eSPI tft = TFT_eSPI(screenWidth, screenHeight); /* TFT instance */

#if LV_USE_LOG != 0
/* Serial debugging */
void my_print(const char *buf)
{
    Serial.printf(buf);
    Serial.flush();
}
#endif

/* Display flushing */
void my_disp_flush(lv_disp_drv_t *disp, const lv_area_t *area, lv_color_t *color_p)
{
    uint32_t w = (area->x2 - area->x1 + 1);
    uint32_t h = (area->y2 - area->y1 + 1);

    tft.startWrite();
    tft.setAddrWindow(area->x1, area->y1, w, h);
    tft.pushColors((uint16_t *)&color_p->full, w * h, true);
    tft.endWrite();

    lv_disp_flush_ready(disp);
}

void incrementalEncoder()
{
    static int lastEncoderPos = encoderPos; // Keep track of the last encoder position to detect changes
    static bool processInput = true;        // Flag to decide whether to process this input or not

    int MSB = digitalRead(pinA);            // Most significant bit
    int LSB = digitalRead(pinB);            // Least significant bit
    int encoded = (MSB << 1) | LSB;         // Combining the two bits
    int sum = (lastEncoded << 2) | encoded; // Adding it to the previous encoded value

    if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011 || sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000)
    {
        if (processInput)
        {
            // Determine direction and increment or decrement encoderPos accordingly
            if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011)
                encoderPos++;
            else if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000)
                encoderPos--;

            // Only process this input, next one will be skipped
            processInput = false;
        }
        else
        {
            // Skip this input, next one will be processed
            processInput = true;
        }
    }

    lastEncoded = encoded; // Store this value for next time

    // If encoderPos has changed significantly (ignoring every second input), update UI
    if (!processInput && encoderPos != lastEncoderPos)
    {
        const int32_t angles[] = {0, 1190, -1280}; // Predefined angles
        const int numModes = sizeof(angles) / sizeof(angles[0]);

        // Adjust the mode index based on the encoder position
        modeIndex = encoderPos % numModes;
        if (modeIndex < 0)
            modeIndex += numModes; // Ensure modeIndex is positive

        // Snap rotation to the nearest predefined angle
        lv_img_set_angle(ui_Text, angles[modeIndex]);

        lastEncoderPos = encoderPos; // Update last position for next comparison

        if (encoderDebug)
        {
            Serial.print("Encoder Position: ");
            Serial.println(encoderPos);
            Serial.print("Mode Index: ");
            Serial.println(modeIndex);
        }
    }
}

void setup()
{
    Serial.begin(9600); /* prepare for possible serial debug */

    lv_init();

#if LV_USE_LOG != 0
    lv_log_register_print_cb(my_print); /* register print function for debugging */
#endif

    tft.begin();        /* TFT init */
    tft.setRotation(3); /* Landscape orientation, flipped */

    lv_disp_draw_buf_init(&draw_buf, buf, NULL, screenWidth * screenHeight / 10);

    /*Initialize the display*/
    static lv_disp_drv_t disp_drv;
    lv_disp_drv_init(&disp_drv);
    /*Change the following line to your display resolution*/
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
}

void loop()
{
    lv_timer_handler();   // let the LVGL do its work
    incrementalEncoder(); // Encoder Interpretation

    // Small delay to limit the update rate (adjust as necessary for your application).
    delay(5);
}