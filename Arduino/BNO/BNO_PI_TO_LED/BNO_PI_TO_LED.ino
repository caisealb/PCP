////LIBRARIES////
#include <Adafruit_NeoPixel.h>    // Neopixel ring library
#include <Wire.h>                 // Library used for communication with I2C
#include <Adafruit_Sensor.h>      // Adafruit unified sensor library
#include <Adafruit_BNO055.h>      // Adafruit library for this breakout
#include <utility/imumaths.h>     // Utility to define vector, matrices and quaternions,

////DEFINITIONS////
// Here, we set the delay, in ms,  between fresh samples (the sample rate)
//#define DELAY_MS 1000

//Pins for neopixel connections
#define ringPin1 6
#define ringPin2 7
//Parameters for rings
Adafruit_NeoPixel ring1 = Adafruit_NeoPixel(16, ringPin1, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel ring2 = Adafruit_NeoPixel(16, ringPin2, NEO_GRB + NEO_KHZ800);


////VARIABLES////
float totalDistance;
float illumNo;
int illumNoRound;
int prevIllumNoRound;
int red;
int green;
int blue;

const byte numChars = 5;
char receivedChars[numChars];  
boolean newData = false;
int dataNumber = 0;




////SETUP////
void setup(void) {
  Serial.begin(9600);
  //Initialise LEDs
  ring1.begin();
  ring1.setBrightness(50);
  ring1.show();

  ring2.begin();
  ring2.setBrightness(50);
  ring2.show();

}




////LOOP////
void loop(void) {
  recvWithEndMarker();
  showNewNumber();
  distCounterLED();
  Serial.println(illumNoRound);

}


void recvWithEndMarker() {
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;

  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (rc != endMarker) {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars) {
        ndx = numChars - 1;
      }
    }
    else {
      receivedChars[ndx] = '\0'; // terminate the string
      ndx = 0;
      newData = true;
    }
  }
}

void showNewNumber() {
    if (newData == true) {
        dataNumber = 0;            
        dataNumber = atoi(receivedChars);  
        totalDistance = dataNumber;
        Serial.print("Received: ");
        Serial.println(receivedChars);
        Serial.print("Total distance: ");    
        Serial.println(dataNumber);     
        newData = false;
    }
}
