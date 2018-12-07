int button = 5;
int led =13;
int count = 0;
int buttonPressCount = 0;

void setup() {
  Serial.begin(9600);
  pinMode(button, INPUT);
  pinMode(led, OUTPUT);
}

void loop() {
  if (digitalRead(button) == 1){
//    Serial.println("1");
    buttonPressCount++;
    digitalWrite(led, HIGH);
  }
  else{
    digitalWrite(led,LOW);
  }
  while(digitalRead(button) == 1){}
  delay(170);
  if (buttonPressCount > 0){
//    Serial.println(count);
    if (++count % 10 == 0){
      Serial.println(buttonPressCount);
      buttonPressCount = 0;
      count = 0;
    }
  }
}
