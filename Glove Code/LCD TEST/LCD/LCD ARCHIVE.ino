/*
  LiquidCrystal Library - Hello World

 Demonstrates the use a 16x2 LCD display.  The LiquidCrystal
 library works with all LCD displays that are compatible with the
 Hitachi HD44780 driver. There are many of them out there, and you
 can usually tell them by the 16-pin interface.

 This sketch prints "Hello World!" to the LCD
 and shows the time.

  The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)

*/

// include the library code:
#include <LiquidCrystal.h>

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 2, en = 3, d4 = 7, d5 = 6, d6 = 5, d7 = 4;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

byte Imposter[8] = {
  B01110,
  B11111,
  B11000,
  B11111,
  B11111,
  B11111,
  B10001,
  B00000
};
int R1;
int R2;

void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  //lcd.print("Suicide is");
  lcd.createChar(0, Imposter);
  
  
}

void loop() {
  // set the cursor to column 0, line 1
  lcd.setCursor(0, 0);
  lcd.print("Suicide is");
  lcd.setCursor(0, 1);
  // print the number of seconds since reset:
  lcd.print("Painless");
  R1=random(10,16);
  R2=random(0,2);
  
  lcd.setCursor(R1, R2);
  lcd.write(byte(0));
  delay(1000);
  lcd.setCursor(R1, R2);
  lcd.write(" ");
  delay(4000);
  //lcd.clear(); // Clears the display 
  //lcd.blink(); //Displays the blinking LCD cursor 
  
}
