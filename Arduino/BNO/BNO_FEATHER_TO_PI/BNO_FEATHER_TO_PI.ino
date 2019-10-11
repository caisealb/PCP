////LIBRARIES///
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#include <Arduino.h>
#include <SPI.h>
#include "Adafruit_BLE.h"
#include "Adafruit_BluefruitLE_SPI.h"
#include "Adafruit_BluefruitLE_UART.h"

#include "BluefruitConfig.h"

#if SOFTWARE_SERIAL_AVAILABLE
#include <SoftwareSerial.h>
#endif


////DEFINITIONS & POINTERS////
#define BNO055_SAMPLERATE_DELAY_MS (1000)
Adafruit_BNO055 bno = Adafruit_BNO055(55);


////VARIABLES////
//For Bluetooth
int32_t imuServiceId;
int32_t distanceCharId;
int32_t speedCharId;
bool success;
//For distance calculation
float posRotations;
float negRotations;
float totalRotations;
float distFactor = 10;
float totalDistance;
float prevTotalDistance;
float currentSpeed;
unsigned long currentTime;
unsigned long prevTime;
int timerInterval = 1000;


////ROTATIONS STRUCTURE////
struct Rotations {
  float forward_rotations = 0;
  float reverse_rotations = 0;
} global_rotations;


bool not_first_loop = false; // Boolean variable to stop logging of first loop
float previous_axis_value = 666;  // Initial value so we don't account for it
// Creating our sensor object to handle the sensor, with initialization 12345
//Adafruit_BNO055 bno = Adafruit_BNO055(12345);

// Function to compute rotation on a given axis
// takes the axis that you want to use and variable it can change
// CAREFUL YOU MUST PASS ROTATIONS AS A POINTER
// (float axis, Rotations * rotations)
bool compute_rotations(float axis, Rotations * rotations) {
  static float initial_axis_value = axis;
  // variable to store initial axis value in compute rotations - declared static so that it stores
  // this value in between function calls, but no other functions can change its value
  //Variables declared as static will only be created and initialized the first time a function is called

  float offset_rot = (axis - previous_axis_value) / 360; // offset since previous measurement, in rotations

  // so we do not account for anything in the setup phase
  if (previous_axis_value == 666) {
    offset_rot = 0;
  }

  if (offset_rot >= 0) {
    (rotations->forward_rotations) += offset_rot;
  } else {
    (rotations->reverse_rotations) += offset_rot;
  }

  // place previous axis value
  previous_axis_value = axis;

  return (true); // returns true by default, do not remove, as it helps with the initial setup.
}



////BLUEFRUIT SETUP////
// Create the bluefruit object, either software serial...uncomment these lines
/*
  SoftwareSerial bluefruitSS = SoftwareSerial(BLUEFRUIT_SWUART_TXD_PIN, BLUEFRUIT_SWUART_RXD_PIN);

  Adafruit_BluefruitLE_UART ble(bluefruitSS, BLUEFRUIT_UART_MODE_PIN,
                      BLUEFRUIT_UART_CTS_PIN, BLUEFRUIT_UART_RTS_PIN);
*/

/* ...or hardware serial, which does not need the RTS/CTS pins. Uncomment this line */
// Adafruit_BluefruitLE_UART ble(BLUEFRUIT_HWSERIAL_NAME, BLUEFRUIT_UART_MODE_PIN);

/* ...hardware SPI, using SCK/MOSI/MISO hardware SPI pins and then user selected CS/IRQ/RST */
Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_CS, BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);

/* ...software SPI, using SCK/MOSI/MISO user-defined SPI pins and then user selected CS/IRQ/RST */
//Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_SCK, BLUEFRUIT_SPI_MISO,
//                             BLUEFRUIT_SPI_MOSI, BLUEFRUIT_SPI_CS,
//                             BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);

// A small helper
void error(const __FlashStringHelper*err) {
  Serial.println(err);
  while (1);
}





////SETUP////
void setup() {
  delay(500);
  Serial.begin(115200);
  randomSeed(micros());
  initSensor();
  initBLE();
}



////LOOP////
void loop(void) {

  sensors_event_t event;
  bno.getEvent(&event);
  float axis_value = event.orientation.x;   // replace this with whatever axis you're tracking
  not_first_loop = (not_first_loop) ? compute_rotations(axis_value, &global_rotations) : true;

  calcDist();
  calcSpeed();
  //Check if command executed
  if (!ble.waitForOK()) {
    error(F("Failed to get response!"));
  }
  //Delay before next measurement update
  delay(BNO055_SAMPLERATE_DELAY_MS);
}



////Initialise BLE////
void initBLE(void) {
  /* Initialise the module */
  Serial.print(F("Initialising the Bluefruit LE module: "));

  if ( !ble.begin(VERBOSE_MODE) )
  {
    error(F("Couldn't find Bluefruit, make sure it's in CoMmanD mode & check wiring?"));
  }
  Serial.println( F("OK!") );

  /* Perform a factory reset to make sure everything is in a known state */
  Serial.println(F("Performing a factory reset: "));
  if (! ble.factoryReset() ) {
    error(F("Couldn't factory reset"));
  }

  /* Disable command echo from Bluefruit */
  ble.echo(false);

  Serial.println("Requesting Bluefruit info:");
  /* Print Bluefruit information */
  ble.info();

  // this line is particularly required for Flora, but is a good idea
  // anyways for the super long lines ahead!
  // ble.setInterCharWriteDelay(5); // 5 ms

  /* Change the device name to make it easier to find */
  Serial.println(F("Setting device name to 'Wheel': "));

  if (! ble.sendCommandCheckOK(F("AT+GAPDEVNAME=Wheel"))) {
    error(F("Could not set device name."));
  }

  /* Add the BNO definition */
  /* Service ID should be 1 */
  Serial.println(F("Adding the BNO Service definition (UUID = 0x180D): "));
  success = ble.sendCommandWithIntReply( F("AT+GATTADDSERVICE=UUID128=00-11-00-11-44-55-66-77-88-99-AA-BB-CC-DD-EE-FF"), &imuServiceId);
  if (! success) {
    error(F("Could not add BNO service"));
  }

  /* Add the distance measurement characteristic */
  /* Chars ID for Measurement should be 1 */
  Serial.println(F("Adding the distance measurement characteristic (UUID = 0x2A37): "));
  success = ble.sendCommandWithIntReply( F("AT+GATTADDCHAR=UUID128=02-11-88-33-44-55-66-77-88-99-AA-BB-CC-DD-EE-FF,PROPERTIES=0x10,MIN_LEN=1,MAX_LEN=17,VALUE=\"\""), &distanceCharId);
  if (! success) {
    error(F("Could not add distance measurement characteristic"));
  }

  /* Add the speed measurement characteristic */
  /* Chars ID for Measurement should be 1 */
  Serial.println(F("Adding the speed measurement characteristic (UUID = 0x2A37): "));
  success = ble.sendCommandWithIntReply( F("AT+GATTADDCHAR=UUID128=02-11-88-22-33-44-55-66-77-88-AA-BB-CC-DD-EE-FF,PROPERTIES=0x10,MIN_LEN=1,MAX_LEN=17,VALUE=\"\""), &speedCharId);
  if (! success) {
    error(F("Could not add speed measurement characteristic"));
  }

  /* Reset the device for the new service setting changes to take effect */
  Serial.print(F("Performing a SW reset (service changes require a reset): "));
  ble.reset();

  Serial.println();
}



////Initalise BNO////
void initSensor(void) {
  if (!bno.begin()) {
    error(F("No BNO055 detected. Check your wiring or I2C address!"));
  }
  delay(1000);
  bno.setExtCrystalUse(true);
}





////DISTANCE VALUE////
void calcDist() {
  //Calculate distance based on total pos and neg rotations
  posRotations = (global_rotations.forward_rotations);
  negRotations = (-global_rotations.reverse_rotations);
  totalRotations = (posRotations + negRotations);
  totalDistance = (totalRotations * distFactor);


  // Command is sent when \n (\r) or println is called
  // AT+GATTCHAR=CharacteristicID,value
  ble.print( F("AT+GATTCHAR=") );
  ble.print( distanceCharId );
  ble.print( F(",") );
  ble.println(String(totalDistance));
  Serial.println(totalRotations);

}


////SPEED VALUE////

void calcSpeed() {
  currentTime = millis();
  if (currentTime - prevTime > timerInterval) {
    float distDiff = totalDistance - prevTotalDistance;
    currentSpeed = distDiff; //equal to because it's measured every 1 second - same as dividing by 1, i.e. itself
  }
  
  // Command is sent when \n (\r) or println is called
  // AT+GATTCHAR=CharacteristicID,value
  ble.print( F("AT+GATTCHAR=") );
  ble.print( speedCharId );
  ble.print( F(",") );
  ble.println(String(currentSpeed));
  Serial.println(currentSpeed);
  
  prevTime = millis();
  prevTotalDistance = totalDistance;
}
