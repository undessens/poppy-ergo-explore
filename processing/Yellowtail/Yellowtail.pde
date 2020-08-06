import netP5.*;
import oscP5.*;

/**
 * Yellowtail
 * by Golan Levin (www.flong.com). 
 * 
 * Click, drag, and release to create a kinetic gesture.
 * 
 * Yellowtail (1998-2000) is an interactive software system for the gestural 
 * creation and performance of real-time abstract animation. Yellowtail repeats 
 * a user's strokes end-over-end, enabling simultaneous specification of a 
 * line's shape and quality of movement. Each line repeats according to its 
 * own period, producing an ever-changing and responsive display of lively, 
 * worm-like textures.
 */


import java.awt.Polygon;

Gesture gestureArray[];
final int nGestures = 5;  // Number of gestures
final int minMove = 13;     // Minimum travel for a new point
int currentGestureID;

Polygon tempP;
int tmpXp[];
int tmpYp[];

OscP5 oscP5;
int askedr;
int askedg;
int askedb;
float finalr;
float finalg;
float finalb;
int askedfr;
int askedfg;
int askedfb;
float finalfr;
float finalfg;
float finalfb;
int askedtr;
int askedtg;
int askedtb;
float finaltr;
float finaltg;
float finaltb;

PFont font;
int textx;
int texty;
/*
EXPERIENCE 8337
POPPY ERGO EXPLORING
ANOTHER POPPY ERGO THROUGH
CURIOSITY-DRIVEN LEARNING
*/


 
void setup() {
  //fullScreen(P2D, 2);
  size(640  , 480, P2D);
  background(0, 0, 0);
  finalr = 0;
  finalg = 0;
  finalb = 0;
  askedr = 0;
  askedb = 0;
  askedg = 0;
  finalfr = 230;
  finalfg = 230;
  finalfb = 230;
  askedfr = 230;
  askedfb = 230;
  askedfg = 230;
  finaltr = 230;
  finaltg = 230;
  finaltb = 230;
  askedtr = 230;
  askedtb = 230;
  askedtg = 230;
  noStroke();

  currentGestureID = -1;
  gestureArray = new Gesture[nGestures];
  for (int i = 0; i < nGestures; i++) {
    gestureArray[i] = new Gesture(width, height);
  }
  clearGestures();
  
  oscP5 = new OscP5(this,12342);
  String[] fontList = PFont.list();
  printArray(fontList);
  font = createFont("Damascus", 88);
  textFont(font);
  textAlign(CENTER, CENTER);
  textx = 950;
  texty = 250;
 
}


void draw() {
  
  //Update foreground
  float alpha = 0.007;
  finalr = finalr*( 1.0 - alpha ) + askedr*1.0*alpha;
  finalg = finalg*( 1.0 - alpha ) + askedg*1.0*alpha;
  finalb = finalb*( 1.0 - alpha ) + askedb*1.0*alpha;
  background(color(finalr, finalg, finalb));
  
  
  //Update geometry
  updateGeometry();
  
  // Draw Line 
  noStroke();
  float alphaForeground = 0.015;
  finalfr = finalfr*( 1.0 - alphaForeground ) + askedfr*1.0*alpha;
  finalfg = finalfg*( 1.0 - alphaForeground ) + askedfg*1.0*alpha;
  finalfb = finalfb*( 1.0 - alphaForeground ) + askedfb*1.0*alpha;
  fill(color(finalfr, finalfg, finalfb));
  for (int i = 0; i < nGestures; i++) {
    renderGesture(gestureArray[i], width, height);
  }
  
  //Draw Text
  
    
  float alphaText = 0.006;
  finaltr = finaltr*( 1.0 - alphaText ) + askedtr*1.0*alpha;
  finaltg = finaltg*( 1.0 - alphaText ) + askedtg*1.0*alpha;
  finaltb = finaltb*( 1.0 - alphaText ) + askedtb*1.0*alpha;
  if(( finaltr + finaltg + finaltg )> 4){
  fill(color(finaltr, finaltg, finaltb));
  String textToDisplay;
  textToDisplay = "EXPERIENCE 8337 \n POPPY ERGO EXPLORING ANOTHER \n POPPY ERGO THROUGH \n CURIOSITY-DRIVEN LEARNING";
 
  text(textToDisplay, textx, texty);
  
  }
  
  
}

void mousePressed() {
  currentGestureID = (currentGestureID+1) % nGestures;
  Gesture G = gestureArray[currentGestureID];
  G.clear();
  G.clearPolys();
  G.addPoint(mouseX, mouseY);
}


void mouseDragged() {
  if (currentGestureID >= 0) {
    Gesture G = gestureArray[currentGestureID];
    if (G.distToLast(mouseX, mouseY) > minMove) {
      G.addPoint(mouseX, mouseY);
      G.smooth();
      G.compile();
    }
  }
}


void keyPressed() {
  if (key == '+' || key == '=') {
    if (currentGestureID >= 0) {
      float th = gestureArray[currentGestureID].thickness;
      gestureArray[currentGestureID].thickness = min(96, th+1);
      gestureArray[currentGestureID].compile();
    }
  } else if (key == '-') {
    if (currentGestureID >= 0) {
      float th = gestureArray[currentGestureID].thickness;
      gestureArray[currentGestureID].thickness = max(2, th-1);
      gestureArray[currentGestureID].compile();
    }
  } else if (key == ' ') {
    clearGestures();
  }
}


void renderGesture(Gesture gesture, int w, int h) {
  if (gesture.exists && gesture.activated) {
    if (gesture.nPolys > 0) {
      Polygon polygons[] = gesture.polygons;
      int crosses[] = gesture.crosses;

      int xpts[];
      int ypts[];
      Polygon p;
      int cr;

      beginShape(QUADS);
      int gnp = gesture.nPolys;
      for (int i=0; i<gnp; i++) {

        p = polygons[i];
        xpts = p.xpoints;
        ypts = p.ypoints;

        vertex(xpts[0], ypts[0]);
        vertex(xpts[1], ypts[1]);
        vertex(xpts[2], ypts[2]);
        vertex(xpts[3], ypts[3]);

        if ((cr = crosses[i]) > 0) {
          if ((cr & 3)>0) {
            vertex(xpts[0]+w, ypts[0]);
            vertex(xpts[1]+w, ypts[1]);
            vertex(xpts[2]+w, ypts[2]);
            vertex(xpts[3]+w, ypts[3]);

            vertex(xpts[0]-w, ypts[0]);
            vertex(xpts[1]-w, ypts[1]);
            vertex(xpts[2]-w, ypts[2]);
            vertex(xpts[3]-w, ypts[3]);
          }
          if ((cr & 12)>0) {
            vertex(xpts[0], ypts[0]+h);
            vertex(xpts[1], ypts[1]+h);
            vertex(xpts[2], ypts[2]+h);
            vertex(xpts[3], ypts[3]+h);

            vertex(xpts[0], ypts[0]-h);
            vertex(xpts[1], ypts[1]-h);
            vertex(xpts[2], ypts[2]-h);
            vertex(xpts[3], ypts[3]-h);
          }

          // I have knowingly retained the small flaw of not
          // completely dealing with the corner conditions
          // (the case in which both of the above are true).
        }
      }
      endShape();
    }
  }
}

void updateGeometry() {
  Gesture J;
  for (int g=0; g<nGestures; g++) {
    if ((J=gestureArray[g]).exists) {
      if (g!=currentGestureID) {
        advanceGesture(J);
      } else if (!mousePressed) {
        advanceGesture(J);
      }
    }
  }
}

void advanceGesture(Gesture gesture) {
  // Move a Gesture one step
  if (gesture.exists) { // check
    int nPts = gesture.nPoints;
    int nPts1 = nPts-1;
    Vec3f path[];
    float jx = gesture.jumpDx;
    float jy = gesture.jumpDy;

    if (nPts > 0) {
      path = gesture.path;
      for (int i = nPts1; i > 0; i--) {
        path[i].x = path[i-1].x;
        path[i].y = path[i-1].y;
      }
      path[0].x = path[nPts1].x - jx;
      path[0].y = path[nPts1].y - jy;
      gesture.compile();
    }
  }
}

void clearGestures() {
  for (int i = 0; i < nGestures; i++) {
    gestureArray[i].clear();
  }
}

void oscEvent(OscMessage theOscMessage) {
  /* check if theOscMessage has the address pattern we are looking for. */
  
  if(theOscMessage.checkAddrPattern("/activate")==true) {
    /* check if the typetag is the right one. */
    if(theOscMessage.checkTypetag("ii")) {
      /* parse theOscMessage and extract the values from the osc message arguments. */
      int index = theOscMessage.get(0).intValue();
      int value = theOscMessage.get(1).intValue(); 
      print("### received an osc message /activate with typetag ii.");
      if(index<nGestures){
        Gesture J;
        (J=gestureArray[index]).activated=(value>0);
      }
      return;
    }  
  } 
  
  if(theOscMessage.checkAddrPattern("/foreground")==true) {
    /* check if the typetag is the right one. */
    if(theOscMessage.checkTypetag("iii")) {
      /* parse theOscMessage and extract the values from the osc message arguments. */
      askedfr = theOscMessage.get(0).intValue();
      askedfg = theOscMessage.get(1).intValue();
      askedfb = theOscMessage.get(2).intValue();

      print("### Forefround changed");
      return;
    }  
  } 
  
  if(theOscMessage.checkAddrPattern("/text")==true) {
    /* check if the typetag is the right one. */
    if(theOscMessage.checkTypetag("iii")) {
      /* parse theOscMessage and extract the values from the osc message arguments. */
      askedtr = theOscMessage.get(0).intValue();
      askedtg = theOscMessage.get(1).intValue();
      askedtb = theOscMessage.get(2).intValue();

      println("### text changed");
      return;
    }  
  } 
  
  if(theOscMessage.checkAddrPattern("/background")==true) {
    /* check if the typetag is the right one. */
    if(theOscMessage.checkTypetag("iii")) {
      /* parse theOscMessage and extract the values from the osc message arguments. */
      askedr = theOscMessage.get(0).intValue();
      askedg = theOscMessage.get(1).intValue();
      askedb = theOscMessage.get(2).intValue();
      
      return;
    }  
  } 
  
  
  
  
  
}
