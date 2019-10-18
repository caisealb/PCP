
#!/usr/bin/env python3

# Import required library
from multiprocessing import Process, Queue, Pipe #multiprocessing to implement pipe
from serial_pipe import serialComms #import process from serial_pipe.py
from serial import Serial # To use serial comms with arduino
import pygatt  # To access BLE GATT support
import signal  # To catch the Ctrl+C and end the program properly
import os  # To access environment variables
from dotenv import \
    load_dotenv  # To load the environment variables from the .env file

# from threading import Thread #threading library
from time import sleep
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit, send

# Serial comms
port = "/dev/ttyACM0"

# Bluetooth device mac address
load_dotenv()
BLUETOOTH_DEVICE_MAC = os.environ['BLUETOOTH_DEVICE_MAC']

# UUID of the GATT characteristic to subscribe
GATT_CHARACTERISTIC_DISTANCE = "02-11-88-33-44-55-66-77-88-99-AA-BB-CC-DD-EE-FF"
GATT_CHARACTERISTIC_SPEED = "02-11-88-22-33-44-55-66-77-88-AA-BB-CC-DD-EE-FF"

# Many devices, e.g. Fitbit, use random addressing, this is required to connect.
ADDRESS_TYPE = pygatt.BLEAddressType.random

distVal = 0
speedVal = 0


# ==== ==== ===== == =====  Web server

app = Flask(__name__)

app.config['SECRET KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/workout')
def distance():
    totalDis = distVal
    return render_template('workoutVis.html', totalDis=totalDis)
def speed():
    currentSpeed = speedVal
    return render_template('workoutVis.html', currentSpeed=currentSpeed)

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
       print("No socket?")
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
       print("No socket?")
    return speedVal



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


if __name__ == '__main__':
    #Connect to bluetooth and subscribe to characteristics
    connect_bluetooth()
    parent_conn, child_conn = Pipe()
    p = Process(target = serialComms, args = (child_conn,))
    p.start()
    print(parent_conn.recv())
    p.join()
    #Run socketIO app
    socketio.run(app, host = '0.0.0.0')


#
# if __name__ == '__main__':
#     # app.run(host='0.0.0.0')