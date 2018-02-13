

void setup() {
  size(2000, 400);
  redBarSetup();
  paintBase();
  //sinesetup();
}

void draw() {
  paintBase();
  
  redBarDraw();
  shadows();
}