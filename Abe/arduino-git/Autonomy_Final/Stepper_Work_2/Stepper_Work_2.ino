
/* 
  Control two steppers using EasyDriver v4.2s
  rtwomey@u.washington.edu
*/


int DIR1 = 2;
int STEP1 = 3;

int DIR2 = 8;
int STEP2 = 9;

void setup() {
  pinMode(DIR1, OUTPUT);
  pinMode(STEP1, OUTPUT); 
  pinMode(DIR2, OUTPUT);
  pinMode(STEP2, OUTPUT); 
}

void pan1(int direct, int steps, int wait){ 
  digitalWrite(DIR1, direct); 
  for(int i=0; i<steps; i++){ 
    digitalWrite(STEP1, HIGH); 
    digitalWrite(STEP1, LOW); 
    //delayMicroseconds(wait); 
    delay(wait); 
  }
}
  void  pan2(int direct, int steps, int wait){ 
  digitalWrite(DIR2, direct); 
  for(int i=0; i<steps; i++){ 
    digitalWrite(STEP2, HIGH); 
    digitalWrite(STEP2, LOW); 
    //delayMicroseconds(wait); 
    delay(wait);
  }
}

  void panBoth(int direct, int steps, int wait) {
  digitalWrite(DIR1, direct); 
  digitalWrite(DIR2, direct); 
  for(int i=0; i<steps; i++){ 
    digitalWrite(STEP1, HIGH); 
    digitalWrite(STEP1, LOW);
    digitalWrite(STEP2, HIGH); 
    digitalWrite(STEP2, LOW);
    delayMicroseconds(wait); 
  }
}




void loop() {


//    pan1(LOW, random(200,800), 1);// one revolution 200 steps/rev * 8 easyDriver precision. 1600 seems closest to true revolution
//    pan1(LOW, 1, 1);
//    pan1(HIGH, random(200,800),1);
//    pan1(HIGH, 1, random(500, 1000));
//
//    pan2(LOW, random(200,800), 1);// one revolution 200 steps/rev * 8 easyDriver precision. 1600 seems closest to true revolution
//    pan2(LOW, 1, 1);
//    pan2(HIGH, random(200,800),1);
//    pan2(HIGH, 1, random(500, 1000));
    

    panBoth(HIGH, 1600, 1000);// no movement, no sound with... delay(wait); ...delay=milliseconds. 1000 = 1 second
    panBoth(LOW, 1600, 1000);
//
//
//
//    panBoth(LOW, random(100,400), random(1, 2));// one revolution 200 steps/rev * 8 easyDriver precision. 1600 seems closest to true revolution
//    panBoth(LOW, 1, random(500, 5000));
//    panBoth(HIGH, random(100,400),random(1, 4));
//    panBoth(HIGH, 1, random(500, 1000));
//    
//
//    panBoth(HIGH, 1, random(500, 5000));// no movement, no sound with... delay(wait); ...delay=milliseconds. 1000 = 1 second
//    panBoth(LOW, 1, random(500, 5000));
  }
