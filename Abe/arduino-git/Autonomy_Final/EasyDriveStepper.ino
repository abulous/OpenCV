
/* 
  Control two steppers using EasyDriver v4.2s
  rtwomey@u.washington.edu
*/


#include <Servo.h> 

int DIR1 = 2;
int STEP1 = 3;


Servo myservo, myservo1;  

int servo0Start = 15, servo1Start = 45;
int servo0Pos = servo0Start, servo1Pos = servo1Start;
int servo0End = 170, servo1End = 100;
int servo0Increment = 1, servo1Increment = 1;
long servo0Interval = 120, servo1Interval = 280;
long servo0LastUpdate = -10000, servo1LastUpdate = -10000;


void setup() {
  Serial.begin(9600);
  myservo.attach(9);
  pinMode(DIR1, OUTPUT);
  pinMode(STEP1, OUTPUT); 
   myservo.attach(9);
 myservo1.attach(5);
 
}

void pan1(int direct, int steps, int wait){ 
  digitalWrite(DIR1, direct); 
  for(int i=0; i<steps; i++){ 
    digitalWrite(STEP1, HIGH); 
    digitalWrite(STEP1, LOW); 
    delayMicroseconds(wait); 
  }
}


void loop() {

 unsigned long currentMillis = millis();

 for(pos = 0; pos < 180; pos += 1)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    pan1(LOW, 6, 2000);
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(15);                       // waits 15ms for the servo to reach the position 
  } 
  for(pos = 180; pos>=1; pos-=1)     // goes from 180 degrees to 0 degrees 
  {                                
    pan1(HIGH, 6, 2000);
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(15);                       // waits 15ms for the servo to reach the position 
  } 

  
}


