#include <Wire.h>

const byte TILE_PIN = 25;
const byte ROW_PIN = 32;
const byte COL_PIN = 33;

void setup()
{
    Serial.begin(9600);

    Wire.begin(54); // Initialize the Arduino as an I2C slave with address 54
    Wire.setClock(800000);
    Wire.onRequest(readProxyData);
}

void loop()
{
    // Uncomment for debugging purposes
    debug();

    delay(5000); // Wait for 5 seconds before next measurement
}

void debug()
{
    Serial.print("Tile Voltage: ");
    Serial.println((((analogRead(TILE_PIN) / 4095.0) * 3.3) * 1.68));
    Serial.print("Row Voltage: ");
    Serial.println((((analogRead(TILE_PIN) / 4095.0) * 3.3) * 1.51));
    Serial.print("Column Voltage: ");
    Serial.println((((analogRead(TILE_PIN) / 4095.0) * 3.3) * 1.51));
    Serial.println(" ");
}

void readProxyData()
{
    // Get sensor readings as integers.
    int tileInt = analogRead(TILE_PIN); // Now returns 0-1023
    int rowInt = analogRead(ROW_PIN);   // Now returns 0-1023
    int colInt = analogRead(COL_PIN);   // Now returns 0-1023

    // Prepare the data array. Now we need 2 bytes per value + 2 bytes for future expansion = 8 bytes
    const byte len = 6;
    byte data[len];

    // Split each integer into two bytes.
    data[0] = (byte)(tileInt >> 8);   // High byte of tileInt
    data[1] = (byte)(tileInt & 0xFF); // Low byte of tileInt
    data[2] = (byte)(rowInt >> 8);    // High byte of rowInt
    data[3] = (byte)(rowInt & 0xFF);  // Low byte of rowInt
    data[4] = (byte)(colInt >> 8);    // High byte of colInt
    data[5] = (byte)(colInt & 0xFF);  // Low byte of colInt

    Wire.write(data, len); // Send the data
}
