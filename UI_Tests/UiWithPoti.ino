#include <lvgl.h>
#include <TFT_eSPI.h>
#include <ui.h>

/*Don't forget to set Sketchbook location in File/Preferencesto the path of your UI project (the parent foder of this INO file)*/

// Initialize Text Object.
extern lv_obj_t * ui_Text;

/*Change to your screen resolution*/
static const uint16_t screenWidth  = 240;
static const uint16_t screenHeight = 240;

static lv_disp_draw_buf_t draw_buf;
static lv_color_t buf[ screenWidth * screenHeight / 10 ];

TFT_eSPI tft = TFT_eSPI(screenWidth, screenHeight); /* TFT instance */

#if LV_USE_LOG != 0
/* Serial debugging */
void my_print(const char * buf)
{
    Serial.printf(buf);
    Serial.flush();
}
#endif

/* Display flushing */
void my_disp_flush( lv_disp_drv_t *disp, const lv_area_t *area, lv_color_t *color_p )
{
    uint32_t w = ( area->x2 - area->x1 + 1 );
    uint32_t h = ( area->y2 - area->y1 + 1 );

    tft.startWrite();
    tft.setAddrWindow( area->x1, area->y1, w, h );
    tft.pushColors( ( uint16_t * )&color_p->full, w * h, true );
    tft.endWrite();

    lv_disp_flush_ready( disp );
}

void setup()
{
    Serial.begin( 9600 ); /* prepare for possible serial debug */

    String LVGL_Arduino = "Hello Arduino! ";
    LVGL_Arduino += String('V') + lv_version_major() + "." + lv_version_minor() + "." + lv_version_patch();

    Serial.println( LVGL_Arduino );
    Serial.println( "I am LVGL_Arduino" );

    lv_init();

#if LV_USE_LOG != 0
    lv_log_register_print_cb( my_print ); /* register print function for debugging */
#endif

    tft.begin();          /* TFT init */
    tft.setRotation( 3 ); /* Landscape orientation, flipped */

    lv_disp_draw_buf_init( &draw_buf, buf, NULL, screenWidth * screenHeight / 10 );

    /*Initialize the display*/
    static lv_disp_drv_t disp_drv;
    lv_disp_drv_init( &disp_drv );
    /*Change the following line to your display resolution*/
    disp_drv.hor_res = screenWidth;
    disp_drv.ver_res = screenHeight;
    disp_drv.flush_cb = my_disp_flush;
    disp_drv.draw_buf = &draw_buf;
    lv_disp_drv_register( &disp_drv );

    // Touch input driver initialization has been removed here

    ui_init();

    Serial.println( "Setup done" );
}


int lastPotValue = -1; // Holds the last potentiometer value; initialized to -1 so that any first reading is guaranteed to be different.

void loop()
{
    int threshold = 80; // The minimum change in potentiometer reading required to update the rotation.
    int potValue = analogRead(34); // Read the potentiometer value.
    // Serial.println(potValue);

    lv_timer_handler(); // let the GUI do its work

    // Calculate the absolute difference between the current and last potentiometer readings.
    int difference = abs(potValue - lastPotValue);

    // Update the rotation only if the difference exceeds the threshold.
    if(difference > threshold)
    {
        // Optional: Map the potValue to a specific rotation range if needed, e.g., 0 to 360 degrees.
        // int rotationAngle = map(potValue, 0, 4095, 0, 360);

        // For simplicity, assuming direct proportional control:
        int rotationAngle = potValue; // Adjust this calculation as needed for your application.

        lv_img_set_angle(ui_Text, rotationAngle);

        lastPotValue = potValue; // Update the lastPotValue with the current potValue.
    }

    delay(5); // Small delay to limit the update rate (adjust as necessary for your application).
}

