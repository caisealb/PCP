
#!/usr/bin/env python3

# Import required library
import pygatt  # To access BLE GATT support
import signal  # To catch the Ctrl+C and end the program properly
import os  # To access environment variables
from dotenv import \
    load_dotenv  # To load the environment variables from the .env file


# The thing ID and access token
load_dotenv()
BLUETOOTH_DEVICE_MAC = os.environ['BLUETOOTH_DEVICE_MAC']

# UUID of the GATT characteristic to subscribe
GATT_CHARACTERISTIC_DISTANCE = "02-11-88-33-44-55-66-77-88-99-AA-BB-CC-DD-EE-FF"

# Many devices, e.g. Fitbit, use random addressing, this is required to connect.
ADDRESS_TYPE = pygatt.BLEAddressType.random


def handle_distance_data(handle, value_bytes):
    #handle -- integer, characteristic read handle the data was received on
    #value_bytes -- bytearray, the data returned in the notification
    print("Received data: %s (handle %d)" % (str(value_bytes), handle))
    values = [float(x) for x in value_bytes.decode('utf-8').split(",")]


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


# Start a BLE adapter
bleAdapter = pygatt.GATTToolBackend()
bleAdapter.start()

# Use the BLE adapter to connect to our device
wheel = bleAdapter.connect(BLUETOOTH_DEVICE_MAC, address_type=ADDRESS_TYPE)

# Subscribe to the GATT service
wheel.subscribe(GATT_CHARACTERISTIC_DISTANCE,
                     callback=handle_distance_data)

# Register our Keyboard handler to exit
signal.signal(signal.SIGINT, keyboard_interrupt_handler)


from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/distance')
def distance():
    return render_template('distanceVis.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
