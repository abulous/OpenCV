int[] loc1 = {1/4*width,1/4*height};
int[] loc2 = {3/4*width, 3/4*height};

boolean ascending1 = true;
boolean ascending2 = true;
float inc;

void shadows() {
  if (ascending1) {
    inc+=0.02;
    if (inc > width) { ascending = false; }
  } else {
    inc-=0.02;
    if (inc < 0) {ascending = true; }
  }
  //println(inc);


  loadPixels();
  for (int x=0; x<width; x++) {
    for (int y=0; y<height; y++) {
      int pixIndex = x + y*width;
      float tempX = map(x, 0,width, 0.01,TWO_PI);
      float tempY = map(y, 0,height, 0.01,TWO_PI);
      float special = sin(tempX*cos(tempX/(tempY+3) - inc));
      //println("special: " + special);
      float r = red(get(x,y));
      float g = green(get(x,y));
      float b = blue(get(x,y));
      pixels[pixIndex] = color(subColor(r, 100*special),subColor(g, 100*special),subColor(b, 100*special));
      
      
       
    }
  }
  updatePixels();
  


  //drawBez();
}

void drawBez() {
  strokeWeight(10);
  stroke(0,0,0, 100);
  noFill();
  
  bezier(0, 0, loc1[0], loc1[1], loc2[0], loc2[1], width, height);
  
}

void mousePressed() {
  
}


int addColor(float colChannel, float value) {
  float newChannel = colChannel + value;
  if (newChannel > 255) { newChannel = 255; }
  
  return (int)newChannel;
}
int subColor(float colChannel, float value) {
  float newChannel = colChannel - value;
  if (newChannel <0) { newChannel = 0; }
  
  return (int)newChannel;
}