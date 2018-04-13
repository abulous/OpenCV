#include <Servo.h> 


Servo myservo0, myservo1, myservo2, myservo3, myservo4;  

int servo0Start = 0, servo1Start = 10, servo2Start = 10, servo3Start = 10, servo4Start = 91;
int servo0Pos = servo0Start, servo1Pos = servo1Start, servo2Pos = servo2Start, servo3Pos = servo3Start, servo4Pos = servo4Start;
int servo0End = 120, servo1End = 180, servo2End = 180, servo3End = 180, servo4End = 180;
int servo0Increment = 1, servo1Increment = 1, servo2Increment = 1, servo3Increment = 1, servo4Increment = 1;
long servo0Interval = 30, servo1Interval = 30, servo2Interval = 30, servo3Interval = 30, servo4Interval = 30;
long servo0LastUpdate = -10000, servo1LastUpdate = -10000, servo2LastUpdate = -10000, servo3LastUpdate = -10000, servo4LastUpdate = -10000;
int val0, val1;
int proxval0, proxval1;
int proxpin0 = 0, proxpin1 = 1;

void setup() {
  
   Serial.begin(9600);
  myservo0.attach(11); // skinny prism
 myservo1.attach(10); // fat prism 
 myservo2.attach(6); // camera
  myservo3.attach(5); // convex
  // myservo4.attach(5); // concave
 
  
   
}

void loop()
{
  
// val0 = analogRead(proxpin0);
//  //int serialValue = val0 / 8; 
//  val0 = map(val0, 0, 550, 0, 170);  
//
//if (val0 > 90)
// myservo0.write(95);
// Serial.println(val0);
//
////if (myservo == 95)
////    Serial.write(serialValue);
//
//
//
//val1 = analogRead(proxpin1); 
// val1 = map(val1, 0, 550, 0, 170); 
// if (val1 > 90) 
//myservo0.write(0);
//Serial.println(val1);


  
  unsigned long currentMillis = millis();
// myservo4.write(95);
 
 
 
 // SERVO 0 

 if(currentMillis - servo0LastUpdate > servo0Interval){
   servo0Pos += servo0Increment;
   
   // end?
  servo0End = random(120, 180);
   if(servo0Pos >= servo0End)
   servo0Increment = -1; // move backward
   
 // are we at the beginning?
 servo0Start = random(10, 30);
   if(servo0Pos <= servo0Start)
     servo0Increment = 1; // move forward
     
   myservo0.write(servo0Pos);
   
   servo0LastUpdate = currentMillis;
 
 }
 
 
 // SERVO 1
 if(currentMillis - servo1LastUpdate > servo1Interval) {
   servo1Pos += servo1Increment;
   
   // are we at the end?
    servo1End = random(120, 180);
   if(servo1Pos >= servo1End)
     servo1Increment = -1; // move backward
     
   // are we at the beginning?
   servo1Start = random(10, 30);
   if(servo1Pos <= servo1Start)
     servo1Increment = 1; // move forward
     
   myservo1.write(servo1Pos);
   
   servo1LastUpdate = currentMillis;
 }
 
 // SERVO 2

 
 if(currentMillis - servo2LastUpdate > servo2Interval) {
   servo2Pos += servo2Increment;
   
   // are we at the end?
   servo2End = random(120, 150);
   if(servo2Pos >= servo2End)
     servo2Increment = -1; // move backward
     
   // are we at the beginning?
   servo2Start = random(0, 30);
   if(servo2Pos <= servo2Start)
     servo2Increment = 1; // move forward
     
   myservo2.write(servo2Pos);
   
   servo2LastUpdate = currentMillis;


 }
 
 // SERVO 3
 
 if(currentMillis - servo3LastUpdate > servo3Interval) {
   servo3Pos += servo3Increment;
   
   // are we at the end?
   servo3End = random(120, 180);
   if(servo3Pos >= servo3End)
     servo3Increment = -1; // move backward
     
   // are we at the beginning?
   servo3Start = random(10, 30);
   if(servo3Pos <= servo3Start)
     servo3Increment = 1; // move forward
     
   myservo3.write(servo3Pos);
   
   servo3LastUpdate = currentMillis;
     }
    

}

