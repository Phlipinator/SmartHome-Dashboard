#include <Wire.h>

const byte TILE_PIN = 15;
const byte ROW_PIN = 16;
const byte COL_PIN = 17;

const byte DEVICE_ADDR = 0x03; // Number of the Sensor, has to be unique over all Sensors connected to the IoT-Dashboard.

void setup()
{
    Serial.begin(9600);

    Wire.begin(54); // Initialize the Arduino as an I2C slave with address 54
    Wire.setClock(800000);
    Wire.onRequest(readProxyData);
}

void loop()
{
    debug();

    delay(5000); // Wait for 5 seconds before next measurement
}

int getTileNumber()
{
    int rawValue = analogRead(TILE_PIN);
    // Define tiles based on measured analog values and assumed thresholds
    // Format: {lower_bound, upper_bound, tile_number}
    int tiles[16][3] = {
        {1000, 1023, 1}, {952, 999, 2}, {890, 940, 3}, {825, 875, 4}, {556, 616, 5}, {622, 682, 6}, {686, 746, 7}, {752, 812, 8}, {490, 550, 9}, {425, 485, 10}, {356, 416, 11}, {292, 352, 12}, {32, 92, 13}, {100, 160, 14}, {162, 222, 15}, {228, 288, 16}};

    for (int i = 0; i < 16; i++)
    {
        if (rawValue >= tiles[i][0] && rawValue <= tiles[i][1])
        {
            return tiles[i][2];
        }
    }

    return 0; // Return -1 if no tile matches
}

int getConsistentTile()
{
    int firstMeasurement = getTileNumber();
    delay(100); // Short delay between measurements
    int secondMeasurement = getTileNumber();
    delay(100);
    int thirdMeasurement = getTileNumber();

    if (firstMeasurement == secondMeasurement && secondMeasurement == thirdMeasurement)
    {
        return firstMeasurement; // All three measurements match
    }
    else
    {
        return 0; // Measurements do not match
    }
}

int getColumnNumber()
{
    int rawValue = analogRead(COL_PIN);
    // Format: {lower_bound, upper_bound, column_number}
    int columns[4][3] = {
        {850, 1023, 1}, // Average of highest readings for column 1
        {550, 849, 2},  // Average of middle-high readings for column 2
        {250, 549, 3},  // Average of middle-low readings for column 3
        {0, 249, 4}     // Lowest readings for column 4
    };

    for (int i = 0; i < 4; i++)
    {
        if (rawValue >= columns[i][0] && rawValue <= columns[i][1])
        {
            return columns[i][2];
        }
    }

    return 0; // Return -1 if no column matches
}

int getRowNumber()
{
    int rawValue = analogRead(ROW_PIN);
    // Format: {lower_bound, upper_bound, row_number}
    int rows[4][3] = {
        {1000, 1023, 1}, // First row
        {700, 999, 2},   // Second row
        {400, 699, 3},   // Third row
        {0, 399, 4}      // Fourth row
    };

    for (int i = 0; i < 4; i++)
    {
        if (rawValue >= rows[i][0] && rawValue <= rows[i][1])
        {
            return rows[i][2];
        }
    }

    return 0; // Return -1 if no row matches
}

void debug()
{
    Serial.print("Tile: ");
    Serial.println(getTileNumber());
    Serial.print("Row: ");
    Serial.println(getRowNumber());
    Serial.print("Column: ");
    Serial.println(getColumnNumber());
    Serial.println(" ");
}

void readProxyData()
{
    // Get sensor readings as integers.
    int tileInt = getTileNumber();  // Assuming it returns 1-16
    int rowInt = getRowNumber();    // Assuming it returns 1-4
    int colInt = getColumnNumber(); // Assuming it returns 1-4

    // Static values for testing
    // int tileInt = 1;
    // int rowInt = 1;
    // int colInt = 1;

    // Prepare the data array.
    const byte len = 4; // Adjusted for the new structure
    byte data[len];

    // Cast integer readings to byte, since we know they fit into a byte.
    data[0] = (byte)tileInt;
    data[1] = (byte)rowInt;
    data[2] = (byte)colInt;

    // Reserved byte for future use, initialized to 0.
    data[3] = 0; // Example: could be used for additional data in the future

    // Send the data over I2C.
    Wire.write(data, len);
}
