import gab.opencv.*;
import processing.video.*;
import java.awt.*;

Capture video;
OpenCV opencv;

void redBarSetup() {
  video = new Capture(this, 640/2, 480/2);
  opencv = new OpenCV(this, 640/2, 480/2);
  opencv.loadCascade(OpenCV.CASCADE_FRONTALFACE);  

  video.start();
  
}

void redBarDraw() {
  opencv.loadImage(video);
  Rectangle[] faces = opencv.detect();
  for (int i = 0; i < faces.length; i++) {
    redBar(map(faces[i].x, 0,video.width, width,0));
  }
  //redBar(mouseX);
}

void redBar(float xLoc) {
  loadPixels();
  for (int x=0; x<width; x++) {
    for (int y=0; y<height; y++) {
      int pixIndex = x + y*width;
  
      //Various Effects
      int maxDiff = 50;
      if (abs(xLoc - x) < maxDiff) {
        int diff = (int) abs(xLoc-x);
        float r = red(get(x,y));
        float g = green(get(x,y));
        float b = blue(get(x,y));
        float newR = (r>maxDiff)? (r-diff):0 ;
        float newG = (g>maxDiff)? (g-diff):0 ;
        float newB = (b>maxDiff)? (b-diff):0 ;
        float newRed = getNewChannel(255, r, diff, maxDiff);
        //float newRed = map(red(get(x,y)) + 100/(diff+1), red(get(x,y)),355, 0,255);
        pixels[pixIndex] = color(newRed,g,b); //,newG,newB);
      }
      
      //pixels[x + y*width] = color(
    }
  }
  updatePixels();
}




float getNewChannel(float target, float current, float difference, float maxDifference) {
  float avg = target * (1/difference) + current * difference;
  avg /= difference;
  
  avg =  map(difference, 0,maxDifference, target,current);
  //print("+-------------------+\n");
  //print(String.format("|  difference = %03.0f |\n", difference));
  //print(String.format("|     maxDiff = %03.0f |\n", maxDifference));
  //print(String.format("| currChannel = %03.0f |\n", current));
  //print(String.format("|   targetVal = %03.0f |\n", target));
  //print(              "|                   |\n");
  //print(String.format("|      OUTPUT = %03.0f |\n", avg));
  //print(              "+-------------------+\n\n");
  
  
  return avg;
}

void captureEvent(Capture c) {
  c.read();
}