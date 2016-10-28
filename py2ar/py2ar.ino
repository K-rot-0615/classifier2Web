void setup() {
  pinMode(13,OUTPUT);

  Serial.begin(9600);
}

void loop() {
  int inputchar = Serial.read();

  if(inputchar != -1){
    switch(inputchar){
      case 's':
        digitalWrite(13,HIGH);
        break;
      case 'q':
        digitalWrite(13,LOW);
        break;
    }
  }
}
