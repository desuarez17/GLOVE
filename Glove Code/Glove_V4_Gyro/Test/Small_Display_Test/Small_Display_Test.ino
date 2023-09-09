// Include Wire Library for I2C
#include <Wire.h>
 
// Include Adafruit Graphics & OLED libraries
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>

// Reset pin not used but needed for library
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

#define OLED_RESET -1
Adafruit_SH1106G display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(9600);
  // Start Wire library for I2C
  Wire.begin();
  
  // initialize OLED with I2C addr 0x3C
  delay(250); // wait for the OLED to power up
  display.begin(0x3C,true);

}

void loop() {
  display.clearDisplay();
  //
  // Clear the display
  //display.clearDisplay();
  //Set the color - always use white despite actual display color
  display.setTextColor(SH110X_WHITE);
  //Set the font size
  display.setTextSize(1);
  //Set the cursor coordinates
  display.setCursor(0,0);
  display.println("TEST");
  display.display();
  
}
