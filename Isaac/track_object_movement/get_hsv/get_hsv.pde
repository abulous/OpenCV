import processing.video.*;

Capture video;
color c;
float v, h;
boolean mFlag = false;

void setup()  {
  size(640, 480);
  video = new Capture(this, 640, 480);
  video.start();
  textSize(30);
  stroke(0,255,0);
  colorMode(HSB,255);
}

void draw()  {
  // show feed
  image(video, 0, 0);
  
  // draw a rectangle
  fill(255,255,255,0);
  strokeWeight(3);
  rect(315,235,10,10);
  
  //get pixel value
  c = get(320,240);
  colorMode(HSB,255);
  h = hue(c);
  
  fill(255,0,0);
  strokeWeight(1);
  text(h, 15, 45);
}

void captureEvent(Capture video) {
  video.read();
}

void mousePressed() {
  print("hue: ");
  println(h);
}