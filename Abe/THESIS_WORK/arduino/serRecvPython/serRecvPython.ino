
int led = 13;
int n;

// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(led, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {

//  Serial.write(n);
//  Serial.println(n);
//  delay(1000);

 // char inByte = ' ';
  
  while(Serial.available()){
  n = Serial.read();
  }
Serial.println(n);

  
  if(n==49){
    digitalWrite(led, HIGH);
  }
  else{
    digitalWrite(led, LOW);
    }

delay(1000);


}
