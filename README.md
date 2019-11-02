<html lang="en">
  <head>
        <link rel="stylesheet" href="webPage.css">
  </head>

  <body>


     <div class="header">
       <h1>   Prototyping Conncected Products  </h1>
       <h3 style="font-size:50%">   Group 3: Caiseal Beardow, Yu Zhang & Kiki Deurvorst </h3>
     </div>

     <div class="row">
       <div class="leftcolumn">
         <div class="card" height="300">
           <h2> Our Project </h2>
           <h5>A connected wheelchair to track live workout data</h5>
           <p> Our project aims to support manual wheelchair users in maintaining an active lifestyle. We envision our project as a workout tracker, similar to existing commercial examples, such as NikeRun or FitBit, but adapted specifically to the physical properties of a manual wheelchair and the practicalities of its use. Using sensors, microprocessors and a Raspberry Pi, we connect the physical components of our system to a visual interface that shows users their workout progress and statistics in real-time. </p>
           <img src="pcp_images/wheelchair.jpg"/>
         </div>
         <div class="card">
           <h2> Design Brief </h2>
           <h5>Connecting a wheelchair</h5>
           <p> “While the population of wheelchair users is growing worldwide, it becomes urgent to design supportive technologies that fit their needs. We aim to develop products for improvement of the wheelchair users’ wellbeing. This design is a connected product that collects data from sensors and processes it in order to actuate user interactions embedded in the wheelchair.”
                Building upon this brief, we envision our target user group as (either full- or part-time) manual wheelchair users aiming to work towards or maintain a healthier, more active lifestyle. Features of our connected product include location, distance and activity tracking (via GPS and accelerometer sensors), visualised through a UX interface, with the intention of developing a mobile app-based product.
           </p>
         </div>
         <div class="card">
           <h2> System Architecture </h2>
           <h5> A sytematic overview of the architecture used for the prototype </h5>
           <img src="pcp_images/SYSTEM_ARCHITECTURE.jpg"/>
         </div>
         <div class="card">
           <h2> Components </h2>
          <p> The core of our connected system is a Raspberry Pi. The Pi runs a central Python script that receives data from sensors, processes it, initialises a server and websocket application, and sends processed data to this websocket.
            <br>
            <br>
            Associated HTML, CSS and JavaScript files are combined to produce an interactive web-based application that visualises users’ workout data in real-time.
            <br><br>
            We use two sensors to receive relevant data:
            <br>
            Adafruit BNO055 Absolute Orientation Sensor;
            <br>
            Adafruit Ultimate GPS Breakout.
            <br><br>
            When mounted on the wheelchair’s wheel axle, the BNO sensor provides us with rotation data that is then used to calculate cumulative distance travelled and, in combination with time elapsed,
            a user’s current speed. This data is sent to the Pi via Bluetooth using GATT commands.
            <br><br>
            The GPS sensor is connected to an Arduino Mega that collects and formats coordinates, then sends them to the Pi via serial communication.
            <br><br>
            The Python script running on the Pi parses these data and packages them in a format that is usable by the JavaScript files implemented in our web application. Using a websocket, data is visualised in real-time and updated accordingly as the user moves with their wheelchair.
          </p>
         </div>

         <div class="card">
           <h2> Technical Details </h2>
          <p class="title"> Connection of Feather to BNO055: </p>
            <p> The IMU (BNO055) along with the Feather is placed on the axle of one side of the wheelchair to calculate
              the distance of the wheelchair moves, the current speed of the wheelchair based on its rotation counts.
            <br> <br>
            	3V 	----- 	VIN<br>
            	GND 	----- 	GND<br>
            	SDA 	----- 	SDA<br>
            	SCL 	----- 	SCL
            <br><br>
             BNO055 is a 9 degrees of freedom IMU contains a gyroscope, an accelerometer and a magnetometer.
            <br>
            For detailed information, go to https://datacentricdesign.org/docs/2019/04/30/sensors-orientation
            </p>
            <br><br>

            <p class="title"> Feather to Pi (BLE) </p>
            <p>
                  Read GPS on arduino mega
                <br>
                  An Adafruit Ultimate GPS is connected to Arduino Mega. It collects GPS data of its location automatically once it is turned on.
                <br><br>
                  Connection of Mega to GPS:<br>
                	5V 	----- 	VIN<br>
                	GND	----- 	GND<br>
                	RX	----- 	TX1<br>
                	TX 	----- 	RX1
                  <br><br>
                  With an empty script running on Mega, the GPS sends raw NMEA data including connected satellite, current time, latitude, longitude, attitude to the serial port. Since only the latitude and longitude is needed to make a location in Google Map, Mega needs to run a script that can parse the raw data and only output the latitude and longitude data. To run the whole script, Adafruit GPS library needs to be added. Below shows the loop function of script, after parsing the NMEA data, the latitude (latdeg) and longitude (longdeg) needs to be printed and thus sent to the serial port. Here Serial.print(latdeg, 8) means in the serial port it prints out the latitude in a float with 8 decimals. If this is not specified, by default only 2 decimal float will be printed and sent by serial port. Google Map does require an 8 decimal float as its latitude and longitude input, so here it is needed to serial print 8 decimal.
                  <br> <br>For detailed information, go to https://datacentricdesign.org/docs/2019/04/30/sensors-gps.
                  <br><br>
            </p>

            <p class="title"> Mega to Pi (serial) </p>
            <p>
                  Read GPS on arduino mega<br>
                  An Adafruit Ultimate GPS is connected to Arduino Mega. It collects GPS data of its location automatically once it is turned on.
                <br><br>
                  Connection of Mega to GPS:<br>
                	5V 	----- 	VIN<br>
                	GND	----- 	GND<br>
                	RX	----- 	TX1<br>
                	TX 	----- 	RX1
                  <br><br>
                  With an empty script running on Mega, the GPS sends raw NMEA data including connected satellite, current time, latitude, longitude, attitude to the serial port. Since only the latitude and longitude is needed to make a location in Google Map, Mega needs to run a script that can parse the raw data and only output the latitude and longitude data. To run the whole script, Adafruit GPS library needs to be added. Below shows the loop function of script, after parsing the NMEA data, the latitude (latdeg) and longitude (longdeg) needs to be printed and thus sent to the serial port. Here Serial.print(latdeg, 8) means in the serial port it prints out the latitude in a float with 8 decimals. If this is not specified, by default only 2 decimal float will be printed and sent by serial port. Google Map does require an 8 decimal float as its latitude and longitude input, so here it is needed to serial print 8 decimal.
                  <br>
                  <br>For detailed information, go to https://datacentricdesign.org/docs/2019/04/30/sensors-gps.
                  <br>
            </p>
         </div>
       </div>


       <div class="rightcolumn">
         <div class="card" height="300">
           <h2> TU Delft Master Elective  </h2>
         <div class ="p2"> PCP stands for Prototyping connected products, an elective from the Industrial Design Engineering master at TU Delft. The elective is an introduction to prototyping IoT connected products. </div>
           <br>
           <img src="pcp_images/TUDelft.png" height="50%" width="50%"/>
         </div>
         <div class="card">
           <h2> About Us  </h2>
             <div id="pictureContainer">
               <img src="pcp_images/cais.jpg"/>
               <br>
                  <div class ="p2"> Caiseal Beardow - DFI </div>
                  <br>
               <img src="pcp_images/yu.jpg"/>
               <br>
                  <div class ="p2"> Yu Zhang - IPD </div>
                  <br>
               <img src="pcp_images/kiki.jpg"/>
                  <div class ="p2"> Kiki Deurvorst- DFI </div> <br><br>
             </div>
         </div>
         <div class="card">
           <h2> Components </h2>
             <div id="pictureContainer">
               <img src="pcp_images/IMU_setup.JPG"/>
               <br>
                  <div class ="p2"> The IMU and feather connected to the wheel of the wheelchair </div>
                  <br>
                  <br>
               <img src="pcp_images/GPS_setup.JPG"/>
               <br>
                  <div class ="p2"> The GPS sensor on an Arduino Mega, connected to the Pi over serial.  </div>
             </div>
         </div>
       </div>

    </div>

    <!-- <div class="footer">
      <h2>Footer</h2>
    </div> -->

  </body>
</html>
