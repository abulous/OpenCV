void eff1() {
  loadPixels();
  for (int x=0; x<width; x++) {
    for (int y=0; y<height; y++) {
      int pixIndex = x + y*width;
  
      //Various Effects
      
      
      
      if (x < width/10) {
        pixels[pixIndex] -= color(1,0,1);
      }
      else if (y < height/2) {
        pixels[pixIndex] += color(0,0,1);
      }
    }
  }
}