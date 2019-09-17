//Variables
#define fsrPin A0

int sensorValue = -10000;
int prevSensorValue = -10000;
int deviation = 0;
double voltageValue;
double newtonValue;


void setup() {
 Serial.begin(9600);
 pinMode(fsrPin, INPUT);

 deviation = 10;
}

  double convertToNewtons(double voltage){
  /*General fitting model: 
       f(x) = a*exp(b*x) + c*exp(d*x)
     Coefficients (with 95% confidence bounds):
       a =     0.01419  (0.01163, 0.01676)
       b =      0.9523  (0.8922, 1.012)
       c =    -0.01461  (-0.02317, -0.006043)
       d =      -2.231  (-6.605, 2.142)
       Goodness of fit:
       SSE: 7.906e-06
       R-square: 0.9999
       Adjusted R-square: 0.9997
       RMSE: 0.001988
  */
  
  double a = 0.01419;
  double b = 0.9523;
  double c = -0.01461;
  double d = -2.231;

  return((a*exp(b*voltage) + c*exp(d*voltage))*9.81); //9.81 multiplication converts KgF to Newtons
  }


void loop() {
 delay(100); //Corresponds to 10Hz sample rate
 sensorValue = analogRead(fsrPin);
 if(sensorValue >= (prevSensorValue - deviation) && sensorValue <= (prevSensorValue + deviation))
  return;

  voltageValue = double((sensorValue*5))/1023; //convert to voltage
  newtonValue = convertToNewtons(voltageValue); //actual force value

  Serial.print("Pressure, ");
  Serial.println(sensorValue);
  //Serial.print(" (0-1023) steps, ");
  //Serial.print(", ");
  //Serial.print(voltageValue);
  //Serial.print(" (v), ");
  //Serial.print(", ");
 //Serial.println(newtonValue);
  //Serial.println(" N.");

  prevSensorValue = sensorValue;
 
}
