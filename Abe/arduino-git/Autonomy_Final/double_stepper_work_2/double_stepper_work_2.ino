
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
    delay(wait); 
  }
}

void pan2(int direct, int steps, int wait){ 
  digitalWrite(DIR2, direct); 
  for(int i=0; i<steps; i++){ 
    digitalWrite(STEP2, HIGH); 
    digitalWrite(STEP2, LOW);
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
    delay(wait); 
  }
}

void loop() {
//  pan1(LOW, 1600, 1);
//  pan1(HIGH,  1600, 1);
//  pan2(LOW, 1600, 1);
//  pan2(HIGH, 1600, 1);

  panBoth(LOW, 3200, random(2, 6));
  panBoth(HIGH, 3200, random(2, 6));
 
 panBoth(LOW, 1600, random(2, 8));
 panBoth(HIGH, 1600, random(2, 8));
  
 // panBoth(HIGH,  1, random(10, 5000));

  panBoth(LOW, 800, random(8, 15));
  panBoth(HIGH, 800, random(8, 15));
   
 // panBoth(LOW,  1, random(10, 5000));

   panBoth(LOW, 1600, random(2, 8));
 panBoth(HIGH, 1600, random(2, 8));

  panBoth(LOW, 3200, random(2, 6));
  panBoth(HIGH, 3200, random(2, 6));

//panBoth(LOW,  1, random(10, 2000));

   panBoth(LOW, 800, random(8, 15));
  panBoth(HIGH, 800, random(8, 15));


  }


