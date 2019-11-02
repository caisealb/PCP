<html lang="en">
  <head>
        <link rel="stylesheet" href="webPage.css">
  </head>

  <body>

     <div class="header">
       <h1>   Prototyping Connected Products  </h1>
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
           <img src="pcp_images/systemArchitecture_100.jpg"/>
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

         <div class="card">
           <h2> Process Overview </h2>

            <p class="title"> 1. Read speed & distance data on BNO and prepare for broadcasting using GATT service (BNO_FEATHER_TO_PI.ino) </p>
              <p class="tab">
              Read data from BNO with on feather <br>
              Process data on feather  (distance and speed)<br>
              Create GATT characteristics for speed and distance <br>
              Create GATT service (using ID’s)
              </p> <br>

            <p class="title"> 2. Subscribe to GATT service (WorkoutVis.py) </p>
              <p class="tab">
              Define characteristics in python script using ID’s  <br>
              Initialise Bluetooth adapter using pygatt library<br>
              Use PYGATT library to subscribe to characteristics set in arduino script
              </p><br>

            <p class="title"> 3. Read and print GPS data over serial (GPS_parsing.ino) </p>
              <p class="tab">
              Read longitude and latitude from gps sensor   <br>
              Parse using adafruit library <br>
              Printing it over serial
              </p><br>

            <p class="title"> 4. Read and process GPS data from serial (WorkoutVis.py) </p>
              <p class="tab">
              In python, we create a serial communication function that opens a connection with the serial port <br>
              Read incoming data and decode it (coming in as bytes <br>
              Place incoming data in an array and split by commas (strip and split functions)<br>
              Assign relevant index values to latitude and longitude variables <br>
              Place serial comms function inside thread - this separates out serial comms from the rest of the code and allows it to run concurrently. If we didn’t do this, serial comms would block the rest of the code as it includes a while loop.
              </p><br>

              <p class="title"> 5. Set up websocket (WorkoutVis.py) </p>
              <p class="tab">
              Set up websocket using flask and flask.io, creating routes for each app address (1 address = 1 HTML file)<br>
              Emit data as JSON objects, broadcasting to all instances of web page<br>
              Create websocket functions corresponding to each JSON object type
              </p><br>

              <p class="title"> 6. Actuate data through online webPage (html/css/js - start/workout/summary) </p>
              <p class="tab">
              Create web interface with HTML/CSS - three pages (start/workout/summary), link them together using Javascript <br>
              Create JS script that uses socket.io.js (JS file hosted online by socket.io developers) to receive JSON objects from Python script, parse JSON objects and assign the resulting data to variables<br>
              Use HTML DOM element objects to insert these variables into webpage structure (i.e. displayed text)<br>
              Use Google Maps API to use variables produced from GPS JSON objects as map coordinates <br>
              Create JS script that uses localStorage to keep track of accumulated user data in a session, then passes it to summary page HTML
              </p> <br>

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
