bool potLCKD = true;

//LCD stuff
#include <LiquidCrystal.h>
const int rs = 8, en = 7,v0 =9, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

void setup() {
  Serial.begin(9600); 
  lcd.begin(16, 2);
  lcd.clear();
  lcd.print("Hemoglbn Ct14ppm");
  pinMode(v0,OUTPUT);//set pin 6 to output for lcd brightness
  //pinMode(9,OUTPUT);//for LED
}

void loop() {
  //poll data
  int butVAL = analogRead(A0);
  int potVAL = analogRead(A1);
  
  //Serial.println(potVAL);
  Serial.println(butVAL);
  
  int potPRCNT = map(potVAL,0,1023,0,100);
  //lock the pot to brightness
  int lcdPWM = map(potPRCNT,0,100,0,255);
  
  analogWrite(v0,lcdPWM);//push the brighntess setting
  analogWrite(12,lcdPWM);
  analogWrite(11,lcdPWM);
  analogWrite(10,lcdPWM);
  //analogWrite(9,lcdPWM);
  //LCD
  //lcd.setCursor(0, 0);
  //lcd.print("Test TEXT");
  //lcd.setCursor(0, 1);
  //lcd.print("Painless");

}
