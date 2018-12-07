//#include <TimerOne.h>

int button = 5;
int led =13;
int count = 0;

void setup() {
  Serial.begin(9600);
  pinMode(button, INPUT);
  pinMode(led, OUTPUT);
}

void loop() {
//  Serial.print(count);
  if (digitalRead(button) == 1){
//    Serial.println("1");
    digitalWrite(led, HIGH);
    if (count > 10){
      Serial.println("1");
      count = 0;
    }
  }

  else{
    digitalWrite(led,LOW);
  }
  
  while(digitalRead(button) == 1){}
  delay(170);
  count++;

  if (count > 1000) {
    count = 0;
  }
}
