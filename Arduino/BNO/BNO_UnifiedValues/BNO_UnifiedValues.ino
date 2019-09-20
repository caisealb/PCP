

#include <Wire.h>                 // Library used for communication with I2C
#include <Adafruit_Sensor.h>      // Adafruit unified sensor library
#include <Adafruit_BNO055.h>      // Adafruit library for this breakout
#include <utility/imumaths.h>     // Utility to define vector, matrices and quaternions,
                                  // And their helper functions

// Here, we set the delay, in ms,  between fresh samples (the sample rate)
#define DELAY_MS 1000

// structure to store total rotations since IMU  initialized, forward and reverse
// initialized with a global variable global_rotations, this variable stores rotations
// on a particular axis, in both directions, since startup
struct Rotations {
  float forward_rotations = 0;
  float reverse_rotations = 0;
} global_rotations;


bool not_first_loop = false; // Boolean variable to stop logging of first loop
float previous_axis_value = 666;  // Initial value so we don't account for it
// Creating our sensor object to handle the sensor, with initialization 12345
Adafruit_BNO055 bno = Adafruit_BNO055(12345);

// Function to compute rotation on a given axis
// takes the axis that you want to use and variable it can change 
// CAREFUL YOU MUST PASS ROTATIONS AS A POINTER
// (float axis, Rotations * rotations)
bool compute_rotations(float axis, Rotations * rotations) {
  static float initial_axis_value = axis;
  // variable to store initial axis value in compute rotations - declared static so that it stores
  // this value in between function calls, but no other functions can change its value
  //Variables declared as static will only be created and initialized the first time a function is called
  
  float offset_rot = (axis-previous_axis_value) / 360; // offset since previous measurement, in rotations

  // so we do not account for anything in the setup phase
  if (previous_axis_value == 666) {
    offset_rot = 0;
  }

  if(offset_rot >= 0) {
    (rotations->forward_rotations) += offset_rot;
  } else {
    (rotations->reverse_rotations) += offset_rot;
  }
  
  // place previous axis value
  previous_axis_value = axis;
   
  return(true); // returns true by default, do not remove, as it helps with the initial setup.
}

// Arduino setup function (automatically called at startup)
void setup(void) {
  Serial.begin(9600);
  Serial.println("Lets begin our Orientation Sensor Test"); Serial.println("");

  // Initialise the sensor
  if(!bno.begin()) {
    // Problem detecting the BNO055 ... wiring error
    Serial.print("No BNO055 is detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  delay(1000);

  /* Display some basic information on this sensor */
  //displaySensorDetails();

  /* Optional: Display current status */
  //displaySensorStatus();

  bno.setExtCrystalUse(true);       // by doing this we are using an external 32khz
                                    // crystal (the one on the development board)
}



// Arduino loop function, called once 'setup' is complete 
void loop(void) {
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);
  
  /* Display the floating point data */
//  Serial.print("X: ");
//  Serial.print(event.orientation.x, 4);   // 4 decimal places
//  Serial.print("\tY: ");
//  Serial.print(event.orientation.y, 4);
//  Serial.print("\tZ: ");
//  Serial.print(event.orientation.z, 4);

  // if this is the first loop iteration, ignore position data (always zero)  
  //if its second loop iteration set the starting position for your axis 
  // if its another iteration, just continue computing the rotation data 

  float axis_value = event.orientation.x;   // replace this with whatever axis you're tracking
  not_first_loop = (not_first_loop)?compute_rotations(axis_value, &global_rotations) : true;

  //Calculate distance based on total pos and neg rotations
  float posRotations = (global_rotations.forward_rotations);
  float negRotations = (-global_rotations.reverse_rotations);
  float totalRotations = (posRotations + negRotations);
  int distFactor = 10;
  float totalDistance = (totalRotations*distFactor);

  Serial.println("");
  Serial.println("==============");
  Serial.println("Total Rotations in selected axis");
  Serial.print("Positive: ");
  Serial.println(global_rotations.forward_rotations);
  Serial.print("Negative: ");
  Serial.println(-global_rotations.reverse_rotations);
  Serial.print("Total rotations: ");
  Serial.println(totalRotations);
  Serial.print("Total distance: ");
  Serial.println(totalDistance);
  Serial.println("==============");

  
  /* Optional: Display calibration status */
  // displayCalStatus();

  /* Optional: Display sensor status (for debug purposes only) */
  //displaySensorStatus();

  /* New line for the next sample */
  Serial.println("");

  /* Wait the specified delay before requesting nex data */
  delay(DELAY_MS) ;
}
