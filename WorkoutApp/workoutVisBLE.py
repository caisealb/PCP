
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

from threading import Thread #threading library
from time import sleep
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit, send

# Serial comms
port = "/dev/ttyACM0"

# Bluetooth
load_dotenv()
BLUETOOTH_DEVICE_MAC = os.environ['BLUETOOTH_DEVICE_MAC']

# UUID of the GATT characteristic to subscribe
GATT_CHARACTERISTIC_DISTANCE = "02-11-88-33-44-55-66-77-88-99-AA-BB-CC-DD-EE-FF"
GATT_CHARACTERISTIC_SPEED = "02-11-88-22-33-44-55-66-77-88-AA-BB-CC-DD-EE-FF"
GATT_CHARACTERISTIC_RESET = "02-11-88-11-22-33-44-55-66-77-AA-BB-CC-DD-EE-FF"

# Many devices, e.g. Fitbit, use random addressing, this is required to connect.
ADDRESS_TYPE = pygatt.BLEAddressType.random

distVal = 0
speedVal = 0

# Bluetooth connection
print("Starting Bluetooth...")

bleAdapter = pygatt.GATTToolBackend()
bleAdapter.start()
wheel = bleAdapter.connect(BLUETOOTH_DEVICE_MAC, address_type=ADDRESS_TYPE)

# print("connecting to Bluetooth device...")

# ==== ==== ===== == =====  Web server ==== ==== ===== == =====

app = Flask(__name__)

app.config['SECRET KEY'] = 'secret!'
socketio = SocketIO(app)


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
    sendResetMSG()
    return render_template('summary.html')



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


def handle_distance_data(handle, value_bytes):
    #handle -- integer, characteristic read handle the data was received on
    #value_bytes -- bytearray, the data returned in the notification
    print("Received distance data: %s (handle %d)" % (str(value_bytes), handle))
    values = [float(x) for x in value_bytes.decode('utf-8').split(",")]
    global distVal
    distVal = (float(value_bytes))
    print(distVal)

    try:
       socketio.emit('distance', '{"distance": "%s"}' % str(distVal), broadcast=True)
    except:
       print("No socket - distance")
    return distVal

def handle_speed_data(handle, value_bytes):
    #handle -- integer, characteristic read handle the data was received on
    #value_bytes -- bytearray, the data returned in the notification
    print("Received speed data: %s (handle %d)" % (str(value_bytes), handle))
    values = [float(x) for x in value_bytes.decode('utf-8').split(",")]
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
    # Use the BLE adapter to connect to our device
    try:
        print("subscribing...")
        # Subscribe to the GATT service
        wheel.subscribe(GATT_CHARACTERISTIC_DISTANCE, callback=handle_distance_data)
        wheel.subscribe(GATT_CHARACTERISTIC_SPEED, callback=handle_speed_data)
        print("subscribed!")

    except:
        print("Not connected")

def sendResetMSG():
        print("Sending reset msg...")
        wheel.char_write(GATT_CHARACTERISTIC_RESET, bytearray([0xFF]))

        # print("Can't send msg")


# Register our Keyboard handler to exit
signal.signal(signal.SIGINT, keyboard_interrupt_handler)

# ==== ==== ===== == =====  Serial comms ==== ==== ===== == =====
#Run serial comms
def serialComms():
    # print("test1")
    # while not connected:
    #     connected = True
    #
    #     while True:
    #         print("test2")
    #         reading = ser.readLine().decode()
    #         print(reading)
    ser = Serial(port, 115200, timeout = 1)
    print(ser.name)

    if (ser.isOpen() == False):
        try:
            ser.open()
            print("port opened")
        except:
             # print("Can't open serial connection :(")
            print("Unexpected error:", sys.exc_info()[0])
            raise
    print("Serial port open!")
    while True:
        # if ser.inWaiting()>0:
            # inputValue = ser.read()
            # print(inputValue)
            sleep(5)
            try:
                ser.read()
                serData = (ser.readline().decode())
                print("Reading data...")
                # print(serData)

                # print(serData)
                dataElements = [x.strip() for x in serData.split(',')]
                print(dataElements)
                # # latitudes = dataElements[1::5]
                if (len(dataElements) > 3):
                    latFloat = float(dataElements[1])
                    print("Latitude:")
                    print(latFloat)
                    # # longitudes = dataElements[3::5]
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
                print("Unexpected error:", sys.exc_info()[0])
                raise

# ==== ==== ===== == =====  Run ==== ==== ===== == =====

connect_bluetooth()
thread = Thread(target = serialComms)
thread.start()

if __name__ == '__main__':
    #Run socketIO app
    socketio.run(app, host = '0.0.0.0')
