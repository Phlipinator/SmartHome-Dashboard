#include <FastLED.h>

// Define LED matrix dimensions
const int MATRIX_SIZE = 16;

#define LED_PIN 5
#define NUM_LEDS 1151
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

// Create a 16x16 LED matrix
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
  FastLED.setBrightness(20);
}

void processLEDCommand(const String &command)
{
  int x, y;
  sscanf(command.c_str(), "%d,%d", &x, &y);
  Serial.print("Received X: ");
  Serial.print(x);
  Serial.print(", Y: ");
  Serial.println(y);
  if (x >= 1 && x <= MATRIX_SIZE && y >= 1 && y <= MATRIX_SIZE)
  {
    Serial.print("LEDs at position ");
    Serial.print(x);
    Serial.print(",");
    Serial.print(y);
    Serial.print(": ");
    x--; // Adjusting to zero-based indexing
    y--; // Adjusting to zero-based indexing
    if (matrix[x][y][0] != 0)
    {
      Serial.print(matrix[x][y][0]);
      FastLED.clear();                   // Clear previous data
      leds[matrix[x][y][0]] = CRGB::Red; // Set the specified LED to red
      FastLED.show();                    // Update the LEDs
      if (matrix[x][y][1] != 0)
      {
        Serial.print(",");
        Serial.print(matrix[x][y][1]);
        leds[matrix[x][y][1]] = CRGB::Red; // Set the specified LED to red
        FastLED.show();                    // Update the LEDs
      }
    }
    else
    {
      Serial.print("None");
    }
    Serial.println();
  }
  else
  {
    Serial.println("Invalid position");
  }
}

void loop()
{
  if (Serial.available())
  {
    String data = Serial.readStringUntil('\n');
    processLEDCommand(data);
  }
}
