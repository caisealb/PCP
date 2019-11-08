<html lang="en">
  <head>
        <link rel="stylesheet" href="webPage.css">
  </head>

  <body>

     <div class="header">
       <h1>   Wheelchair Workout Tracker  </h1>
       <h3 style="font-size:50%">   Prototyping Connected Products - Group 3
         <br> Caiseal Beardow, Yu Zhang & Kiki Deurvorst </h3>
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
              <br>
                Building upon this brief, we envision our target user group as (either full- or part-time) manual wheelchair users aiming to work towards or maintain a healthier, more active lifestyle. Features of our connected product include location, distance and activity tracking (via GPS and accelerometer sensors), visualised through a UX interface, with the intention of developing a mobile app-based product.
           </p>
         </div>

         <div class="card">
           <h2> System Architecture </h2>
           <h5> A sytematic overview of the architecture used for the prototype </h5>
           <img src="pcp_images/systemdiagram2.png"/>
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
           <h2> Process Summary </h2>
           <h5> For a detailed explanation of all the steps, refer to the technical details below. </h5>

            <p class="title">  1. Read IMU data from feather </p>
              <p class="tab">
                Read data from BNO with on feather      <br>
                Process data on feather  (distance and speed)   <br>
              </p> <br>

            <p class="title"> 2. Set up GATT service on feather </p>
              <p class="tab">
                Create GATT characteristics for speed and distance       <br>
                Create GATT service (using ID’s)  <br>
              </p><br>

            <p class="title">   3. Subscribe to GATT service on pi    </p>
              <p class="tab">
                Define characteristics in python script using ID’s    <br>
                Initialise Bluetooth adapter using pygatt library    <br>
                Use PYGATT library to subscribe to characteristics set in arduino script<br>
              </p><br>


            <p class="title"> 4. Read and print GPS data over serial  </p>
              <p class="tab">
                Read longitude and latitude from gps sensor    <br>
                Parse using adafruit library       <br>
                Print it over serial<br>
              </p><br>

              <p class="title"> 5. Read and process GPS data from serial  </p>
              <p class="tab">
                In python, we create a serial communication function that opens a connection with the serial port       <br>
                Read incoming data and decode it (coming in as bytes               <br>
                Place incoming data in an array and split by commas (strip and split functions)     <br>
                Assign relevant index values to latitude and longitude variables              <br>
                Place serial comms function inside thread - this separates out serial comms from the rest of the code and allows it to run concurrently. If we didn’t do this, serial comms would block the rest of the code as it includes a while loop.<br>
              </p><br>

              <p class="title"> 6. Set up websocket  </p>
              <p class="tab">
                Set up websocket using flask and flask.io, creating routes for each app address (1 address = 1 HTML file)<br>
                Emit data as JSON objects, broadcasting to all instances of web page<br>
                Create websocket functions corresponding to each JSON object type<br>
              </p> <br>

              <p class="title"> 7. WebApp - Actuate data on online webPage   </p>
              <p class="tab">
                Create web interface with HTML/CSS - three pages (start/workout/summary), link them together using Javascript <br>
                Create JS script that uses socket.io.js (JS file hosted online by socket.io developers) to receive JSON objects from Python script, parse JSON objects and assign the resulting data to variables<br>
                Use HTML DOM element objects to insert these variables into webpage structure (i.e. displayed text)<br>
              </p> <br>

              <p class="title"> 8. Google Maps API  </p>
              <p class="tab">
                Use Google Maps API to use variables produced from GPS JSON objects as map coordinates <br>
              </p> <br>

              <p class="title"> 9. Localstorage for workout summary </p>
              <p class="tab">
                Create JS script that uses localStorage to keep track of accumulated user data in a session, then passes it to summary page HTML <br>
              </p> <br>

            </div>





         <div class="card">
           <h2> Technical Details of the Process </h2>


<!-- step1 -->
  <p class="title"> Step 1: Read IMU data on feather </p>
          <p> The IMU (BNO055) along with the Feather is placed on the axle of one side of the wheelchair. It calculates the cumulative number of rotations made by the wheel, which is then processed to calculate cumulative distance travelled and current speed.
            <br> <br>
            <img src="pcp_images/Feather_Wheel.JPG"/>
            <br> <br>
            Connection of Feather to BNO055:<br>
            	3V 	----- 	VIN<br>
            	GND 	----- 	GND<br>
            	SDA 	----- 	SDA<br>
            	SCL 	----- 	SCL
            <br><br>
            BNO055 is a 9 degrees of freedom IMU. It contains a gyroscope, an accelerometer and a magnetometer. To run this sensor in Arduino, the Adafruit Sensor and Adafruit BNO055 library need to be included.
            <br><br>
            <img src="pcp_images/axisvalue.JPG"/>
            <br><br>
            After creating a sensor event, by calling the orientation function and specifying the axis (here is x from xyz), the Euler angle of the sensor position around that axis will be calculated. In the case of our wheelchair, the axis of the wheel overlaps with the x axis of the sensor, so the Euler angle of the sensor along the x-axis corresponds to the wheel’s rotation.
            <br> <br>
            <img src="pcp_images/distspeed.JPG"/>
            <br><br>
            Based on that, we can calculate cumulative total wheel rotations and multiply this by the circumference of the wheel to find distance travelled. Then the speed can be calculated at a set time interval.
            <br>
            For detailed information, go to https://datacentricdesign.org/docs/2019/04/30/sensors-orientation
          </p>

<!-- step 2  -->
  <p class="title"> Step 2: Feather to Pi (BLE) </p>
          <p>
                In order to send data between the feather and the pi, we need to set up GATT characteristics and a GATT service on the feather.
                <br><br>
                <img src="pcp_images/gatt_feather.jpg"/>
                <br><br>
          </p>

<!-- step 3  -->
<p class="title"> Step 3: Subscribe to GATT service </p>
          <p>
                We define the characteristics in our python script using the same ID’s set in the arduino script.
                <br><br>
                <img src="pcp_images/subscribe_GATT.jpg"/>
                <br><br>
                We must then initialise the Bluetooth adapter using the pygatt library and use this library to subscribe to the characteristics.
                <br><br>
                <img src="pcp_images/import_pygatt.jpg"/>
                <br><br>
                <img src="pcp_images/gatt_subscribe.jpg"/>
                <br><br>
          </p>

<!-- step 4  -->
<p class="title"> Step 4: Read GPS on arduino mega </p>
            <p>
                An Adafruit Ultimate GPS is connected to Arduino Mega. It collects GPS data of its location automatically once it is turned on.
                <br><br>
                <img src="pcp_images/GPS_setup.JPG"/>
                <br><br>
                  Connection of Mega to GPS:<br>
                	5V 	----- 	VIN<br>
                	GND	----- 	GND<br>
                  RX	----- 	TX1<br>
                  TX 	----- 	RX1
                  <br><br>
                With an empty script running on the Mega, the GPS sends raw NMEA data including connected satellite, current time, latitude, longitude and altitude to the serial port. Since only the latitude and longitude is needed to define a location in the Google Maps API, the Mega needs to run a script that can parse the raw data and then output the latitude and longitude data. To run the whole script, the Adafruit GPS library needs to be included. The image below shows the loop function of the script. After parsing the NMEA data, the latitude (latdeg) and longitude (longdeg) needs to be printed and thus sent to the serial port. Here Serial.print(latdeg, 8) formats the latitude data as a float value with 8 decimals. If this is not specified, by default only 2 decimal places will be printed. Google Maps requires an 8 decimal float as its latitude and longitude input, so here it is needed to serial print 8 decimal places.
                  <br><br>
                  <img src="pcp_images/GPScode.JPG"/>
                  <br><br>
                  For detailed information, go to https://datacentricdesign.org/docs/2019/04/30/sensors-gps.
                  <br><br>
            </p>

<!-- step 5  -->
<p class="title"> Step 5: Read GPS data from serial, process in thread  </p>
            <p>
                  In python, we create a serial communication function that opens a connection with the serial port.
                  <br><br>
                  <img src="pcp_images/serial_py.jpg"/>
                  <br><br>
                  In order to use the incoming data, which is coming in as bytes, we need to decode it. We then place the incoming data in an array and split it by commas (strip and split functions). (In our preceding Arduino script, we printed latitude and longitude data with commas in between, to allow us to split the data in this way.)
                  <br><br>
                  <img src="pcp_images/decode_split.jpg"/>
                  <br><br>
                  We then assign data at relevant index values to latitude and longitude variables that can be sent through a websocket.
                  <br><br>
                  <img src="pcp_images/variablesSocket.jpg"/>
                  <br><br>
                  We also place the serial comms function inside a thread - this separates out serial comms from the rest of the code and allows it to run concurrently. If we didn’t do this, serial comms would block the rest of the code as it includes a while loop. Threading allows us to place serial comms in a separate flow of execution.
                  <br><br>
                  <img src="pcp_images/thread.jpg"/>
                  <br><br>
            </p>


<!-- step 6  -->
<p class="title"> Step 6: Websocket  </p>
            <p>
                  In order to display our continuously updating GPS, speed and distance data in a browser, we must set up a websocket. We do this using flask and flask_socketio, creating routes for each app address (1 address = 1 HTML file).
                  <br><br>
                  <img src="pcp_images/flask.jpg"/>
                  <br><br>
                  <img src="pcp_images/route.jpg"/>
                  <br><br>
                  The data is emitted as JSON objects, broadcasting to all instances of web page.We create websocket functions corresponding to each JSON object that we send.
                  <br><br>
                  <img src="pcp_images/json.jpg"/>
                  <br><br>
            </p>


<!-- step 7  -->
<p class="title"> Step 7: WebApp </p>
                <p>
                      In order to display the data in the browser, we designed three HTML pages that correspond with each other. The “Start” page includes a countdown, directing the user to the workout overview in which a route is plotted using a Google Maps API (next section). It also shows the current speed, distance and time of the workout. Users can stop the workout which directs them to a summary page, containing an overview of their workout. Refer to workout/summary/start.html/js/css for details.
                      <br><br>
                      <img src="pcp_images/interfaceStart.jpg"/>
                      <br><br>
                      <img src="pcp_images/interface.jpg"/>
                      <br><br>
                      We created a JS script that uses socket.io.js (JS file hosted online by socket.io developers) to receive JSON objects from the Python script, parse these JSON objects and assign the resulting data to variables. We make use of HTML DOM element objects to insert these variables into the webpage structure (getElementByID).
                      <br><br>
                      <img src="pcp_images/json_html.jpg"/>
                      <br><br>
                </p>


<!-- step 8  -->
<p class="title"> Step 8: Google Maps API </p>
                <p>
                  To implement a Google map in a webpage, a Google Maps Javascript API is needed. For information on how to implement this API, go to https://developers.google.com/maps/documentation/javascript/get-api-key.
                  To actually activate your API key, you need to go to your Google Cloud Platform account page and fill in your credit card information - but don’t worry, using the API is free! In the Javascript file, add   <script src="https://maps.googleapis.com/maps/api/js?key=YOURAPIKEY&libraries=drawing&callback=initMap" async defer></script>.
                  <br><br>
                  Additionally, the function initMap needs to be called to initialize the map on the webpage. As shown, a map variable needs to be identified, its zoom in level, center and styles can be customized by you.
                  <br><br>
                  <img src="pcp_images/initmap.JPG"/>
                  <br><br>
                  To draw out the live route of the user while moving, the position of the user needs to be updated - in this case, once every second. As shown, when the new latitude and longitude come in over the websocket, we combine them as an object and they are added to the locations array. Then the Polyline function will draw out the route based on the locations array. Since we want to draw out a live route which changes all the time, we call the updatePosition function every second.
                  <br><br>
                  <img src="pcp_images/updateposition.JPG"/>
                  <br><br>
                  For more tutorials about this API, go to https://developers.google.com/maps/documentation/javascript/adding-a-google-map
                  <br><br>
                </p>

<!-- step 9  -->
<p class="title"> Step 9: Workout summary </p>
                <p>
                When users press the stop button, all session data must be gathered in the summary page. We created a JS script that uses localStorage to keep track of accumulated user data in a session, then passes it to the summary page HTML.
                <br><br>
                <img src="pcp_images/localStorage.jpg"/>
                <br><br>
                </p>
         </div>
         
        <div class="card">
       <h2> Videos of the prototype </h2>
<video>
  <source src="IMG_4695.mov" type="video/mp4">
</video>
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
