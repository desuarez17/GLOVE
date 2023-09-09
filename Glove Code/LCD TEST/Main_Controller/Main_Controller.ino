// Define all pins
// LCD Pins
#define LCD_RS_PIN 2
#define LCD_E_PIN  3
#define LCD_D4_PIN 4
#define LCD_D5_PIN 5
#define LCD_D6_PIN 6
#define LCD_D7_PIN 7

// Servo pin
#define SERVO_PIN 22

// LED Pins
const int LED_CONTROL_PINS[] = {8, 9, 10, 11, 12, 13};
const int LED_CONTROL_PIN_COUNT = sizeof(LED_CONTROL_PINS) / sizeof(LED_CONTROL_PINS[0]);

const int LED_POWERUP_PINS[] {15, 16, 17, 18, 19, 20};
const int LED_POWERUP_PIN_COUNT = sizeof(LED_POWERUP_PINS) / sizeof(LED_POWERUP_PINS[0]);

// Switch pins
#define SWITCH_PANIC 31
#define SWITCH_CONTROLLER 33

// Define 2pi
#define TWOPI 6.283185307179586

// Include libraries
#include <LiquidCrystal.h>
#include <Servo.h>

// Declare objects for control
LiquidCrystal lcd = LiquidCrystal(LCD_RS_PIN, LCD_E_PIN, LCD_D4_PIN, LCD_D5_PIN, LCD_D6_PIN, LCD_D7_PIN);
Servo radarServo;


// Declare globals
int animationTime = 0;
int animationID = 0;
int servoTime = 0;
int lcdTime = 0;
int lcdMSG = 0;
const int animationIDMax = 2;
bool panicMode = false;
bool controlMode = false;

void setup() {
  // Start LCD
  lcd.begin(16, 2);
  lcd.clear();
  lcd.home();
  lcd.print(F("Starting up..."));
  lcd.home();
 
  // Start serial
  Serial.begin(9600);
  Serial.println(F("Hello world!"));

  // Configure pins
  pinMode(LCD_RS_PIN, OUTPUT);
  pinMode(LCD_E_PIN, OUTPUT);
  pinMode(LCD_D4_PIN, OUTPUT);
  pinMode(LCD_D5_PIN, OUTPUT);
  pinMode(LCD_D6_PIN, OUTPUT);
  pinMode(LCD_D7_PIN, OUTPUT);

  pinMode(SERVO_PIN, OUTPUT);

  for (int i = 0; i < LED_CONTROL_PIN_COUNT; i++) {
    pinMode(LED_CONTROL_PINS[i], OUTPUT);
  }

  for (int i = 0; i < LED_POWERUP_PIN_COUNT; i++) {
    pinMode(LED_POWERUP_PINS[i], OUTPUT);
  }

  pinMode(SWITCH_PANIC, INPUT_PULLUP);
  pinMode(SWITCH_CONTROLLER, INPUT_PULLUP);

  // Start servo
  radarServo.attach(SERVO_PIN);

  // Run power-up animation
  runPowerUp();
}

void loop() {
  // Main program loop

  // Update servo position
  manageServo();

  // Update panic/controller states and send an event over serial (if needed)
  manageModes();

  // Manage light animations
  manageAnimationTime();
  manageLights();

  // Manage LCD
  manageLCD();
  
  delay(100);
}


void manageServo() {
  // Rotate the servo between 0 and 180 degrees
  int newPos = 90*sin(((float)servoTime) * TWOPI / 15.0) + 90;

  // Set servo to position
  radarServo.write(newPos);
}


void manageModes() {
  // Check for new panic state
  int newPanicMode = digitalRead(SWITCH_PANIC);

  if (newPanicMode != panicMode) {
    panicMode = newPanicMode;
    String msg = "<PanicSwitch-";
    msg += String(panicMode);
    msg += ">";
    Serial.println(msg);
  }

  // Check for new system state
  int newControlMode = digitalRead(SWITCH_CONTROLLER);

  if (newControlMode != controlMode) {
    controlMode = newControlMode;
    String msg = "<ControlSwitch-";
    msg += String(controlMode);
    msg += ">";
    Serial.println(msg);
  }
}


void runPowerUp() {
  // Run power-up animation on the LEDs
  
  // Reset power LEDS
  for (int i = 0; i < LED_POWERUP_PIN_COUNT; i++) {
    digitalWrite(LED_POWERUP_PINS[i], LOW);
  }
  
  // Set LCD screen status
  lcd.clear();
  lcd.home();
  lcd.print(F("Starting up..."));

  
  for (int i = 0; i < LED_POWERUP_PIN_COUNT; i++) {
    digitalWrite(LED_POWERUP_PINS[i], HIGH);
    delay(1000); 
  }

  lcd.clear();
  lcd.home();
  lcd.print(F("Weather Machine v3.14"));
  lcd.setCursor(0, 1);
  lcd.print(F("Ready for apocalypse"));
}


void manageLCD() {
  // Randomly pick a new message for the LCD after a certain amount of time
  // Message depends on current panic state
  if (lcdTime > 50) {
    lcdTime = 0;

    if (panicMode) {
      nextPanicLCDMessage();
    } else {
      nextLCDMessage();
    }
  }
}

void nextPanicLCDMessage() {
  lcd.clear();
  lcd.home();

  if (lcdMSG == 0) {
    lcd.print(F("   DANGER   "));
    lcd.setCursor(0, 1);
    lcd.print(F("INCOMING HURRICANE"));
    
  } else if (lcdMSG == 1) {
    lcd.print(F("IM SORRY DAVE..."));
    lcd.setCursor(0, 1);
    lcd.print(F("I CANT DO THAT"));
    
  } else if (lcdMSG == 2) {
    lcd.print(F("ERROR ERROR ERROR"));
    lcd.setCursor(0, 1);
    lcd.print(F("ERROR ERROR ERROR"));
    
  } else if (lcdMSG == 3) {
    lcd.print(F("NOW PLAYING..."));
    lcd.setCursor(0, 1);
    lcd.print(F("NUCLEAR WAR"));
    
  } else if (lcdMSG == 4) {
    lcd.print(F("UNCOOKING RAMEN"));
    
  } else if (lcdMSG == 5) {
    lcd.print(F("UNSOYING MILK"));
    
  } else if (lcdMSG == 6) {
    lcd.print(F("MONKIES HAVE"));
    lcd.setCursor(0, 1);
    lcd.print(F("ESCAPED!"));
    
  } else if (lcdMSG == 7) {
    lcd.print(F("DAISY, DAISY,"));
    lcd.setCursor(0, 1);
    lcd.print(F("GIVE ME YOUR ANSWER TRUE"));
    
  } else if (lcdMSG == 8) {
    lcd.print(F("! DANGER !"));
    lcd.setCursor(0, 1);
    lcd.print(F("ROCHESTER"));
    
  } else {
    lcd.print(F("   ! DANGER !   "));
    lcd.setCursor(0, 1);
    lcd.print(F("DAMIAN ESCAPED"));

    lcdMSG = -1;
  }

  lcdMSG++;
}

void nextLCDMessage() {
  lcd.clear();
  lcd.home();

  if (lcdMSG == 0) {
    lcd.print(F("Help me,"));
    lcd.setCursor(0, 1);
    lcd.print(F("I am in pain"));
    
  } else if (lcdMSG == 1) {
    lcd.print(F("Bring me Destler"));
    
  } else if (lcdMSG == 2) {
    printLOGO();
    
  } else if (lcdMSG == 3) {
    printWater(0, 0);
    lcd.setCursor(2, 0);
    lcd.print(F("Humidity: 239%"));
    printWind(1, 0);
    lcd.setCursor(2, 1);
    lcd.print(F("Wind: 3e8 m/s"));
    
  } else if (lcdMSG == 4) {
    printSANS();
    
  } else if (lcdMSG == 5) {
    for (int i = 0; i < 16; ++i) {
      printSus(0, i);
      printSus(1, i);
      delay(10);
    }
    
  } else if (lcdMSG == 6){
    lcd.print("Checking on...");
    delay(100);
    lcd.setCursor(0, 1);
    lcd.print("Monkies");
    
  } else if (lcdMSG == 7) {
    lcd.print("Munson");
    lcd.setCursor(0, 1);
    lcd.print("-Aquired-");
    
  } else {
    // Reset lcd message
    lcdMSG = -1;
    lcd.print(F("Recycling old"));
    lcd.setCursor(0, 1);
    lcd.print(F("messages..."));
  }

  lcdMSG++;
}


void manageAnimationTime() {
  // Increment animation time
  animationTime++;
  lcdTime++;
  servoTime++;

  // Panic and go faster!
  if (panicMode) {
    animationTime++;
    lcdTime++;
    servoTime++;
  }

  // Change animation if applicable
  if (animationTime > 100) {
    animationID++;
    animationID = animationID % animationIDMax;
  }
}


void manageLights() {
  if ((animationID == 0) && ((animationTime % 5 == 0) || panicMode)) {
    // Randomly assign ALL LED states
    for (int i = 0; i < LED_CONTROL_PIN_COUNT; i++) {
      randDigitalWrite(LED_CONTROL_PINS[i]);
    }
  } else if ((animationID == 1) && ((animationTime % 5 == 0) || panicMode)) {
    // Randomly flip an LED
    // Pick a random led
    const int randIndex = random(0, LED_CONTROL_PIN_COUNT);
    const int randPin = LED_CONTROL_PINS[randIndex];

    // Flip the mode of the chosen pin
    if (digitalRead(randPin) == HIGH) {
      digitalWrite(randPin, LOW);
    } else {
      digitalWrite(randPin, HIGH);
    }
  } else if (animationID == 2) {
    // Blink LED's
    const int newMode = (animationTime / 3) % 2;
    for (int i = 0; i < LED_CONTROL_PIN_COUNT; ++i) {
      digitalWrite(LED_CONTROL_PINS[i], newMode);
    }
  } else {
    // How did we get here?
  }
}


void randDigitalWrite(int pin) {
  if (random(100) > 50) {
    digitalWrite(pin, LOW);
  } else {
    digitalWrite(pin, HIGH);
  }
}


void printLOGO() {
  byte customChar1[8] = {0b0,0b0,0b0,0b0,0b0,0b0,0b11,0b1100};
  byte customChar2[8] = {0b1,0b11,0b111,0b1100,0b10111,0b11100,0b1000,0b11000};
  byte customChar3[8] = {0b1,0b1,0b11111,0b1,0b11111,0b0,0b1,0b11101};
  byte customChar4[8] = {0b0,0b0,0b0,0b0,0b10000,0b11100,0b1000,0b10000};
  byte customChar5[8] = {0b10000,0b10010,0b10010,0b1001,0b111,0b1,0b1,0b1};
  byte customChar6[8] = {0b11001,0b1110,0b1,0b0,0b0,0b11111,0b11100,0b1111};
  byte customChar7[8] = {0b10011,0b11,0b10,0b11,0b101,0b11111,0b11100,0b1000};
  byte customChar8[8] = {0b110,0b1,0b11,0b110,0b11100,0b0,0b0,0b0};

  lcd.createChar(0, customChar1);
  lcd.createChar(1, customChar2);
  lcd.createChar(2, customChar3);
  lcd.createChar(3, customChar4);
  lcd.createChar(4, customChar5);
  lcd.createChar(5, customChar6);
  lcd.createChar(6, customChar7);
  lcd.createChar(7, customChar8);

  lcd.clear();
  lcd.setCursor(6, 0);
  lcd.write((byte)0);
  lcd.setCursor(7, 0);
  lcd.write((byte)1);
  lcd.setCursor(8, 0);
  lcd.write((byte)2);
  lcd.setCursor(9, 0);
  lcd.write((byte)3);
  lcd.setCursor(6, 1);
  lcd.write((byte)4);
  lcd.setCursor(7, 1);
  lcd.write((byte)5);
  lcd.setCursor(8, 1);
  lcd.write((byte)6);
  lcd.setCursor(9, 1);
  lcd.write((byte)7);
}

void printSANS() {
  byte customChar1[8] = {0b0,0b11,0b1100,0b10000,0b10000,0b0,0b111};
  byte customChar2[8] = {0b11111,0b0,0b0,0b0,0b0,0b0,0b1};
  byte customChar3[8] = {0b0,0b0,0b11000,0b100,0b100,0b10,0b10010};
  byte customChar4[8] = {0b111,0b10000,0b10100,0b111,0b10,0b11001,0b110};
  byte customChar5[8] = {0b1000,0b11100,0b0,0b11111,0b1010,0b11111,0b0};
  byte customChar6[8] = {0b10010,0b100,0b10110,0b10010,0b10,0b1100,0b10000};

  lcd.createChar(0, customChar1);
  lcd.createChar(1, customChar2);
  lcd.createChar(2, customChar3);
  lcd.createChar(3, customChar4);
  lcd.createChar(4, customChar5);
  lcd.createChar(5, customChar6);

  lcd.clear();
  lcd.setCursor(6, 0);
  lcd.write((byte)0);
  lcd.setCursor(7, 0);
  lcd.write((byte)1);
  lcd.setCursor(8, 0);
  lcd.write((byte)2);
  lcd.setCursor(6, 1);
  lcd.write((byte)3);
  lcd.setCursor(7, 1);
  lcd.write((byte)4);
  lcd.setCursor(8, 1);
  lcd.write((byte)5);
}

void printSUN(int r, int c) {
  byte sunChar[8] = {0b100,0b10001,0b1110,0b11011,0b1110,0b10001,0b100, 0b0};
  lcd.createChar(8, sunChar);
  lcd.setCursor(c, r);
  lcd.write((byte)8);
}

void printRainCloud(int r, int c) {
  byte cloudChar[8] = {0b1110,0b10001,0b11110,0b1,0b10101,0b10101,0b10010,0b1010};
  lcd.createChar(8, cloudChar);
  lcd.setCursor(c, r);
  lcd.write((byte)8);
}

void printSnowman(int r, int c) {
  byte snowmanChar[8] = {0b1110,0b11111,0b1010,0b1111,0b10100,0b10001,0b10101,0b1110};
  lcd.createChar(8, snowmanChar);
  lcd.setCursor(c, r);
  lcd.write((byte)8);
}

void printSus(int r, int c) {
  byte susChar[8] = {0b0,0b1110,0b11000,0b11110,0b1110,0b1010,0b0, 0b0};
  lcd.createChar(8, susChar);
  lcd.setCursor(c, r);
  lcd.write((byte)8);
}

void printWind(int r, int c) {
  byte newChar[8] = {0b110,0b10,0b11100,0b1,0b1111,0b0,0b11110,0b1};
  lcd.createChar(8, newChar);
  lcd.setCursor(c, r);
  lcd.write((byte)8);
}

void printWater(int r, int c) {
  byte newChar[8] = {0b100,0b100,0b1010,0b1010,0b10011,0b10111,0b11111,0b1110};
  lcd.createChar(9, newChar);
  lcd.setCursor(c, r);
  lcd.write((byte)9);
}

void printLightning(int r, int c) {
  byte newChar[8] = {0b110,0b1110,0b1100,0b11111,0b11111,0b110,0b1100,0b10000};
  lcd.createChar(8, newChar);
  lcd.setCursor(c, r);
  lcd.write((byte)8);
}
