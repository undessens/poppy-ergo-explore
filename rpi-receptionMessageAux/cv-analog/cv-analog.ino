/*
 Fading

 This example shows how to fade an LED using the analogWrite() function.

 The circuit:
 * LED attached from digital pin 9 to ground.

 Created 1 Nov 2008
 By David A. Mellis
 modified 30 Aug 2011
 By Tom Igoe

 http://www.arduino.cc/en/Tutorial/Fading

 This example code is in the public domain.

 */


int ledPin = 10;    // LED connected to digital pin 9

void setup() {
  // nothing happens in setup
  Serial.begin(115200);
}

void loop() {
  
  
  if(Serial.available()>0){

    char msg = Serial.read();

  if(msg=='a'){

    analogWrite(ledPin,255);
  delay(1500);

  // fade out from max to min in increments of 5 points:
  for (int fadeValue = 255 ; fadeValue >= 0; fadeValue -= 4) {
    // sets the value (range from 0 to 255):
    analogWrite(ledPin, fadeValue);
    // wait for 30 milliseconds to see the dimming effect
    delay(30);
  }

  analogWrite(ledPin,0);


    
  }
  
  if(msg=='b'){

    analogWrite(ledPin,255);
    delay(1500);

    // fade out from max to min in increments of 5 points:
    for (int fadeValue = 255 ; fadeValue >= 0; fadeValue -= 4) {
      // sets the value (range from 0 to 255):
      analogWrite(ledPin, fadeValue);
      // wait for 30 milliseconds to see the dimming effect
      delay(30);
    }

    analogWrite(ledPin,0);

    analogWrite(ledPin,255);
    delay(200);

    // fade out from max to min in increments of 5 points:
    for (int fadeValue = 125 ; fadeValue >= 0; fadeValue -= 3) {
      // sets the value (range from 0 to 255):
      if(random(10)>7){
      analogWrite(ledPin, 200);
      delay(120);  
      }
      analogWrite(ledPin, fadeValue);
      delay(30);  
      
      // wait for 30 milliseconds to see the dimming effect
      
    }

    analogWrite(ledPin,0);

  
    
  }
    
    
  }
  
  /*
  // fade in from min to max in increments of 5 points:
  for (int fadeValue = 0 ; fadeValue <= 255; fadeValue += 5) {
    // sets the value (range from 0 to 255):
    analogWrite(ledPin, fadeValue);
    // wait for 30 milliseconds to see the dimming effect
    delay(30);
  }
  */
  
}


