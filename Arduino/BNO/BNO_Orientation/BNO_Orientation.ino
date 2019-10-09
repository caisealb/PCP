#include <Wire.h>                 // Library used for communication with I2C
#include <Adafruit_Sensor.h>      // Adafruit unified sensor library
#include <Adafruit_BNO055.h>      // Adafruit library for this breakout
#include <utility/imumaths.h>     // Utility to define vector, matrices and quaternions,
#define DELAY_MS 500

Adafruit_BNO055 bno = Adafruit_BNO055(12345);

void setup(void)
{
  Serial.begin(9600);
  Serial.println("Lets begin our Orientation Sensor Test"); Serial.println("");

  /* Initialise the sensor */
  if (!bno.begin())
  {
    Serial.print("No BNO055 is detected ... Check your wiring or I2C ADDR!");
    while (1);
  }

  delay(1000);
  
  sensor_t sensor;
  bno.getSensor(&sensor);
  uint8_t system_status, self_test_results, system_error;
  system_status = self_test_results = system_error = 0;
  bno.getSystemStatus(&system_status, &self_test_results, &system_error);
  uint8_t system, gyro, accel, mag;     // variable for gyroscope, accelerometer and magnetometer
  system = gyro = accel = mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);
  bno.setExtCrystalUse(true);       // by doing this we are using an external 32khz crystal (the one on the development board)
}

void loop(void)
{
  /* Get a new sensor event */
  sensors_event_t event;
  bno.getEvent(&event);

  /* Display the floating point data */
  Serial.print("X: ");
  Serial.print(event.orientation.x, 2);   // 4 decimal places
  Serial.println("");
  delay(DELAY_MS) ;
}
