
#!/usr/bin/env python3
# ==== ==== ===== == ===== Libraries and variables ==== ==== ===== == =====
# Import required library
from serial import Serial # To use serial comms with arduino
from operator import itemgetter
import pygatt  # To access BLE GATT support
import signal  # To catch the Ctrl+C and end the program properly
import os  # To access environment variables
from dotenv import \
    load_dotenv  # To load the environment variables from the .env file
#threading library
from threading import Thread
from time import sleep
#flask and socketIO
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit, send
#DCD hub
from dcd.entities.thing import Thing
from dcd.entities.property import PropertyType

# Serial comms
port = "/dev/ttyACM0"

# Bluetooth device mac address
load_dotenv()
BLUETOOTH_DEVICE_MAC = os.environ['BLUETOOTH_DEVICE_MAC']
THING_ID = os.environ['THING_ID']
THING_TOKEN = os.environ['THING_TOKEN']

# UUID of the GATT characteristic to subscribe
GATT_CHARACTERISTIC_DISTANCE = "02-11-88-33-44-55-66-77-88-99-AA-BB-CC-DD-EE-FF"
GATT_CHARACTERISTIC_SPEED = "02-11-88-22-33-44-55-66-77-88-AA-BB-CC-DD-EE-FF"

# Many devices, e.g. Fitbit, use random addressing, this is required to connect.
ADDRESS_TYPE = pygatt.BLEAddressType.random

distVal = 0
speedVal = 0

# ==== ==== ===== == ===== DCD Hub ==== ==== ===== == =====

# Instantiate a thing with its credential, then read its properties from the DCD Hub
my_thing = Thing(thing_id=THING_ID, token=THING_TOKEN)
my_thing.read()

def find_or_create(property_name, property_type):
    #Search a property by name, create it if not found, then return it.
    if my_thing.find_property_by_name(property_name) is None:
        my_thing.create_property(name=property_name,
                                 property_type=property_type)
    return my_thing.find_property_by_name(property_name)


# ==== ==== ===== == =====  Web server ==== ==== ===== == =====

app = Flask(__name__)

app.config['SECRET KEY'] = 'secret!'
socketio = SocketIO(app)

# App routes - functions and templates for various addresses
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/workout')
def distance():
    totalDis = distVal
    return render_template('Workout.html', totalDis=totalDis)
def speed():
    currentSpeed = speedVal
    return render_template('Workout.html', currentSpeed=currentSpeed)

@app.route('/summary')
def summary():
    return render_template('summary.html')

# Websocket functions - broadcast various data to all instances of web app
@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
    emit('json', json, broadcast=True)

@socketio.on('distance')
def handle_distance(json):
    print(float(json['distance']))

@socketio.on('speed')
def handle_speed(json):
    print(float(json['speed']))

@socketio.on('latitude')
def handle_speed(json):
    print(float(json['latitude']))

@socketio.on('longitude')
def handle_speed(json):
    print(float(json['longitude']))


# Handle distance data received via BLE from Feather
def handle_distance_data(handle, value_bytes):
    #handle -- integer, characteristic read handle the data was received on
    #value_bytes -- bytearray, the data returned in the notification
    print("Received distance data: %s (handle %d)" % (str(value_bytes), handle))
    values = [float(x) for x in value_bytes.decode('utf-8').split(",")]
    find_or_create("Distance", PropertyType.ONE_DIMENSION).update_values(values)
    global distVal
    distVal = (float(value_bytes))
    print(distVal)

    try:
       socketio.emit('distance', '{"distance": "%s"}' % str(distVal), broadcast=True)
    except:
       print("No socket - distance")
    return distVal

# Handle speed data received via BLE from Feather
def handle_speed_data(handle, value_bytes):
    #handle -- integer, characteristic read handle the data was received on
    #value_bytes -- bytearray, the data returned in the notification
    print("Received speed data: %s (handle %d)" % (str(value_bytes), handle))
    values = [float(x) for x in value_bytes.decode('utf-8').split(",")]
    find_or_create("Speed", PropertyType.ONE_DIMENSION).update_values(values)
    global speedVal
    speedVal = (float(value_bytes))
    print(speedVal)

    try:
       socketio.emit('speed', '{"speed": "%s"}' % str(speedVal), broadcast=True)
    except:
       print("No socket - speed")
    return speedVal


# ==== ==== ===== == =====  Bluetooth ==== ==== ===== == =====

def discover_characteristic(device):
    #List characteristics of a device
    for uuid in device.discover_characteristics().keys():
        try:
            print("Read UUID" + str(uuid) + "   " + str(device.char_read(uuid)))
        except:
            print("Something wrong with " + str(uuid))

def read_characteristic(device, characteristic_id):
    #Read a characteristic
    return device.char_read(characteristic_id)


def keyboard_interrupt_handler(signal_num, frame):
    #Make sure we close our program properly
    print("Exiting...".format(signal_num))
    wheel.unsubscribe(GATT_CHARACTERISTIC_DISTANCE)
    exit(0)

def connect_bluetooth():
    print("Starting Bluetooth...")
    # Start a BLE adapter
    bleAdapter = pygatt.GATTToolBackend()
    bleAdapter.start()

    print("connecting to Bluetooth device...")
    # Use the BLE adapter to connect to our device
    try:
        wheel = bleAdapter.connect(BLUETOOTH_DEVICE_MAC, address_type=ADDRESS_TYPE)

        print("subscribing...")
        # Subscribe to the GATT service
        wheel.subscribe(GATT_CHARACTERISTIC_DISTANCE, callback=handle_distance_data)
        wheel.subscribe(GATT_CHARACTERISTIC_SPEED, callback=handle_speed_data)
        print("subscribed!")
    except:
        print("Not connected")

# Register our Keyboard handler to exit
signal.signal(signal.SIGINT, keyboard_interrupt_handler)

# ==== ==== ===== == =====  Serial comms ==== ==== ===== == =====
#Run serial comms
def serialComms():
    ser = Serial(port, 115200, timeout = 1)
    print(ser.name)

    if (ser.isOpen() == False):
        try:
            ser.open()
            print("Serial port open!")
        except:
            print("Unexpected serial error:", sys.exc_info()[0])
            raise
    while True:
            sleep(1)
            try:
                ser.read()
                serData = (ser.readline().decode())
                print("Reading data...")
                dataElements = [x.strip() for x in serData.split(',')]
                print(dataElements)

                if (len(dataElements) > 3):
                    latFloat = float(dataElements[1])
                    print("Latitude:")
                    print(latFloat)
                    longFloat = float(dataElements[3])
                    print("Longitude:")
                    print(longFloat)
                    try:
                        socketio.emit('latitude', '{"latitude": "%s"}' % str(latFloat), broadcast=True)
                        socketio.emit('longitude', '{"longitude": "%s"}' % str(longFloat), broadcast=True)
                    except:
                        print("No socket - lat/long")
                else:
                    print("Problem with GPS data")
            except:
                print("Unexpected serial error:", sys.exc_info()[0])
                raise

# ==== ==== ===== == =====  Run ==== ==== ===== == =====

connect_bluetooth()
# Run serial comms in separate thread to allow serial and BLE simultaneously (non-blocking)
thread = Thread(target = serialComms)
thread.start()

if __name__ == '__main__':
    #Run socketIO app
    socketio.run(app, host='0.0.0.0')