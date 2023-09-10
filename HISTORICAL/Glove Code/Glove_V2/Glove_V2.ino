
void setup() {
  Serial.begin(9600); 
}

void loop() {
  int F0 = analogRead(A0);
  int F1 = analogRead(A1);
  int F2 = analogRead(A2);
  int F3 = analogRead(A3);
  int F4 = analogRead(A4);


  Serial.println(" ");
  Serial.print(F0);
  Serial.print(" ");
  Serial.print(F1);
  Serial.print(" ");
  Serial.print(F2);
  Serial.print(" ");
  Serial.print(F3);
  Serial.print(" ");
  Serial.print(F4);

}
