int index = 0;
boolean ascending = true;

void paintBase() {
  if (ascending) {
    index+=3;
    if (index == 255) {ascending= false;}
  }
  else {
    index-=3;
    if (index == 0) {ascending= true;}
  }
  
  loadPixels();
  for (int x=0; x<width; x++) {
    for (int y=0; y<height; y++) {
      int pixIndex = x + y*width;
      //Update Pixels
      float X = map(x, 0, width, 0, 255);
      float Y = map(y, 0, height, 0, 255);
      float XY = map(X%(Y+1), 0, 255, 0, 255);
      pixels[pixIndex] = color(X, Y, 0);
      if (XY > 255) {print("XY: " + XY);}
    }
  }
  updatePixels();
}