
/* 
  Control ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,LolloPop0p
  one stepper using an EasyDriver v4.2
  rtwomey@u.washington.edu
*/

int DIR = 2;
int STEP = 3;

void setup() {
  pinMode(DIR, OUTPUT);
  pinMode(STEP, OUTPUT); 
}

void pan1(int direct, int steps, int wait){ 
  digitalWrite(DIR, direct); 
  for(int i=0; i<steps; i++){ 
    digitalWrite(STEP, LOW); 
    digitalWrite(STEP, HIGH); 
    delayMicroseconds(wait);
  }
} 



void loop() {

  pan1(HIGH, 1600, 4000);// one revolution 200 steps/rev * 8 easyDriver precision. 1600 seems closest to true revolution
//  delayMicroseconds(wait); 
  
  pan1(LOW, 1600, 4000);
}


