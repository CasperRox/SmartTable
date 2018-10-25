int button = 5;
int led =13;


void setup() {
  Serial.begin(9600);
  pinMode(button, INPUT);
  pinMode(led, OUTPUT);
}

void loop() {
  
  if (digitalRead(button) == 1){
    Serial.println("1");
    digitalWrite(led, HIGH);
  }
  else{
    digitalWrite(led,LOW);
  }
  while(digitalRead(button) == 1){}
  delay(170);
}
