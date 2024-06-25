#include <FastLED.h>
#include <iostream>

// CONSTANTS
const int MATRIX_SIZE = 16;
const int SHORT_DELAY = 10;
const int LONG_DELAY = 100;
const int REPETITIONS = 6;
const bool DEBUG = false;

#define LED_PIN 5
#define NUM_LEDS 1151
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

const int relayPin = 13; // GPIO pin connected to the relay

// Unique Positions of the LEDs in the 16 x 16 matrix are stored here
int matrix[MATRIX_SIZE][MATRIX_SIZE][2] = {
    {{61, 62}, {58}, {55, 54}, {51}, {47}, {43, 44}, {40}, {36, 37}, {33}, {29}, {25, 26}, {22}, {18}, {15, 14}, {11}, {7, 8}},
    {{84}, {88}, {91, 92}, {95}, {98, 99}, {102}, {106}, {109, 110}, {113}, {116, 117}, {120}, {124}, {127, 128}, {131}, {134, 135}, {138}},
    {{206, 207}, {203}, {199}, {195, 196}, {192}, {188, 189}, {185}, {181}, {177, 178}, {174}, {170, 171}, {167}, {163}, {159, 160}, {156}, {152}},
    {{227, 228}, {231}, {235}, {238, 239}, {242}, {245, 246}, {249}, {253}, {256, 257}, {260}, {263, 264}, {267}, {271}, {274, 275}, {278}, {281, 282}},
    {{349, 350}, {346}, {342}, {338, 339}, {335}, {331, 332}, {328}, {324}, {320, 321}, {317}, {313, 314}, {310}, {306}, {302, 303}, {299}, {295, 296}},
    {{371}, {374, 375}, {378}, {381, 382}, {385}, {389}, {392, 393}, {396}, {399, 400}, {403}, {407}, {410, 411}, {414}, {417, 418}, {421}, {425}},
    {{494}, {490, 491}, {487}, {483}, {479, 480}, {476}, {472, 473}, {469}, {465}, {461, 462}, {458}, {454, 455}, {451}, {447}, {444}, {440}},
    {{514}, {517, 518}, {521}, {524, 525}, {528}, {532}, {535, 536}, {539}, {543}, {546}, {550}, {553, 554}, {557}, {561}, {564}, {568}},
    {{637}, {633}, {630}, {626}, {622, 623}, {619}, {615}, {612}, {608}, {604, 605}, {601}, {597}, {594}, {590}, {586, 587}, {583}},
    {{658, 659}, {662}, {666}, {669}, {673}, {676, 677}, {680}, {684}, {687}, {691}, {694, 695}, {698}, {702}, {705}, {709}, {712, 713}},
    {{780, 781}, {777}, {773}, {770}, {766}, {762, 763}, {759}, {755}, {752}, {748}, {744, 745}, {741}, {737}, {734}, {730}, {726, 727}},
    {{802}, {805}, {809}, {812, 813}, {816}, {820}, {823}, {827}, {830, 831}, {834}, {838}, {841}, {845}, {848, 849}, {852}, {856}},
    {{923}, {920}, {916}, {912, 913}, {909}, {905}, {902}, {898}, {894}, {891}, {887}, {883, 884}, {880}, {876}, {873}, {869}},
    {{949}, {952}, {956}, {959}, {963}, {967}, {970}, {974}, {977, 978}, {981}, {985}, {988}, {992}, {995, 996}, {999}, {1003}},
    {{1067}, {1064}, {1060}, {1056, 1057}, {1053}, {1049}, {1046}, {1042}, {1038}, {1035}, {1031}, {1027, 1028}, {1024}, {1020}, {1017}, {1013}},
    {{1090}, {1094}, {1097, 1098}, {1101}, {1105}, {1108}, {1112}, {1115, 1116}, {1119}, {1123}, {1126}, {1130}, {1134}, {1137}, {1141}, {1144, 1145}}};

void setup()
{
    Serial.begin(9600);
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
    FastLED.setBrightness(50);

    pinMode(relayPin, OUTPUT);   // Initialize the relay pin as an output
    digitalWrite(relayPin, LOW); // Start with the relay off
}

// Calculates a route between two sets of coordinates
void animateTrail(int r1, int c1, int r2, int c2)
{
    // Adjusting to zero-based indexing
    r1--;
    c1--;
    r2--;
    c2--;

    // Determine the direction of movement
    int horizontal = c1 - c2;
    int vertical = r1 - r2;

    // Check if coordinates are within bounds
    if (c1 >= 0 && c1 < MATRIX_SIZE && r1 >= 0 && r1 < MATRIX_SIZE && c2 >= 0 && c2 < MATRIX_SIZE && r2 >= 0 && r2 < MATRIX_SIZE)
    {
        // Iterating through horizontal direction
        if (horizontal < 0)
        {
            for (int c = c1; c <= c2; c++)
            {
                LEDProcessing(r1, c, true);
            }
            c1 = c2;
        }
        else
        {
            for (int c = c1; c >= c2; c--)
            {
                LEDProcessing(r1, c, true);
            }
            c1 = c2;
        }

        // Iterating through vertical direction
        if (vertical < 0)
        {
            for (int r = r1; r <= r2; r++)
            {
                LEDProcessing(r, c1, true);
            }
        }
        else
        {
            for (int r = r1; r >= r2; r--)
            {
                LEDProcessing(r, c1, true);
            }
        }
    }

    // Set all LEDs to black, because FastLED.clear() doesn't work here for some reason
    fill_solid(leds, NUM_LEDS, CRGB::Black);
    FastLED.show();
}

// Turn LED(s) for any given position on
void LEDProcessing(int row, int col, bool activate)
{
    // Ensure row and column are within valid range
    if (row >= 0 && row < MATRIX_SIZE && col >= 0 && col < MATRIX_SIZE)
    {
        // Check if there's a LED at the current position
        if (matrix[row][col][0] != 0)
        {
            leds[matrix[row][col][0]] = CRGB::Red;
        }
        // Check if there's a second LED at the current position
        if (matrix[row][col][1] != 0)
        {
            leds[matrix[row][col][1]] = CRGB::Red;
        }

        // Check if LEDs should be turned on immediately
        if (activate)
        {
            FastLED.show();
            delay(SHORT_DELAY);
            FastLED.clear();
        }
    }
}

// Calculate Coordinates surrounding any given position of the board
void animateStart(int row, int col)
{
    // Adjust to zero based indexing
    row--;
    col--;

    // Set LEDs at all four positions
    LEDProcessing(row - 1, col, false); // Up
    LEDProcessing(row + 1, col, false); // Down
    LEDProcessing(row, col - 1, false); // Left
    LEDProcessing(row, col + 1, false); // Right

    // Update all LEDs at once
    FastLED.show();
    delay(LONG_DELAY);

    // Clear all LEDs and update
    fill_solid(leds, NUM_LEDS, CRGB::Black);
    FastLED.show();
}

// Animate a wave-pattern from the center of the matrix
void animateBoot()
{
    // The center of the matrix for a 16x16 grid (2x2 center)
    int centerRow1 = MATRIX_SIZE / 2 - 1;
    int centerRow2 = MATRIX_SIZE / 2;
    int centerCol1 = MATRIX_SIZE / 2 - 1;
    int centerCol2 = MATRIX_SIZE / 2;

    // The maximum distance from the center to the edges
    int maxDistance = max(centerRow1, centerCol1);

    // Loop through each layer of the wave
    for (int distance = 0; distance <= maxDistance; distance++)
    {
        // Top and bottom rows of the current layer
        for (int col = centerCol1 - distance; col <= centerCol2 + distance; col++)
        {
            if (centerRow1 - distance >= 0 && col >= 0 && col < MATRIX_SIZE)
            {
                LEDProcessing(centerRow1 - distance, col, false); // Top row 1
                LEDProcessing(centerRow2 - distance, col, false); // Top row 2
            }
            if (centerRow1 + distance < MATRIX_SIZE && col >= 0 && col < MATRIX_SIZE)
            {
                LEDProcessing(centerRow1 + distance, col, false); // Bottom row 1
                LEDProcessing(centerRow2 + distance, col, false); // Bottom row 2
            }
        }

        // Left and right columns of the current layer
        for (int row = centerRow1 - distance + 1; row < centerRow2 + distance; row++)
        {
            if (row >= 0 && row < MATRIX_SIZE && centerCol1 - distance >= 0)
            {
                LEDProcessing(row, centerCol1 - distance, false); // Left column 1
                LEDProcessing(row, centerCol2 - distance, false); // Left column 2
            }
            if (row >= 0 && row < MATRIX_SIZE && centerCol1 + distance < MATRIX_SIZE)
            {
                LEDProcessing(row, centerCol1 + distance, false); // Right column 1
                LEDProcessing(row, centerCol2 + distance, false); // Right column 2
            }
        }

        // Show the current layer
        FastLED.show();
        delay(SHORT_DELAY); // Adjust delay as needed

        // Clear the current layer before moving to the next
        fill_solid(leds, NUM_LEDS, CRGB::Black);
    }

    // Ensure all LEDs are off at the end
    fill_solid(leds, NUM_LEDS, CRGB::Black);
    FastLED.show();
}

void loop()
{
    if (Serial.available())
    {
        String data = Serial.readStringUntil('\n');
        int r1, c1, r2, c2;

        // Try to parse two pairs of coordinates
        int coords = sscanf(data.c_str(), "%d,%d,%d,%d", &r1, &c1, &r2, &c2);

        // Check if the input contains two sets of coordinates
        if (coords == 4)
        {
            if (DEBUG)
            {
                std::cout << "First Coordinate: " << r1 << "," << c1 << std::endl;
                std::cout << "Second Coordinate: " << r2 << "," << c2 << std::endl;
            }
            for (int i = 0; i < REPETITIONS; i++)
            {
                digitalWrite(relayPin, HIGH);
                delay(10);
                animateTrail(r1, c1, r2, c2);
                delay(50);
                digitalWrite(relayPin, LOW);
            }
        }
        // Check if the input contains one set of coordinates
        else if (coords == 2)
        {
            if (DEBUG)
            {
                std::cout << "Single Coordinate: " << r1 << "," << c1 << std::endl;
            }
            for (int i = 0; i < REPETITIONS; i++)
            {
                digitalWrite(relayPin, HIGH);
                delay(10);
                animateStart(r1, c1);
                delay(50);
                digitalWrite(relayPin, LOW);
            }
        }
        else if (data == "boot")
        {
            if (DEBUG)
            {
                Serial.println("Performing boot animation.");
            }

            digitalWrite(relayPin, HIGH);
            delay(10);
            animateBoot();
            delay(5);
            animateBoot();
            delay(5);
            animateBoot();
            delay(50);
            digitalWrite(relayPin, LOW);
            
        }
        else
        {
            if (DEBUG)
            {
                Serial.println("Invalid input. Please provide both sets of coordinates.");
            }
        }
    }
}