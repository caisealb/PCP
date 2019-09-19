from dcd.entities.thing import Thing
from dcd.entities.property import PropertyType

from dotenv import load_dotenv
import os
import serial

#Thing ID and access token
load_dotenv()
THING_ID = os.environ['THING_ID']
THING_TOKEN = os.environ['THING_TOKEN']

my_thing = Thing(thing_id=THING_ID, token=THING_TOKEN)
my_thing.read()


#Create random properties
my_property = my_thing.find_or_create_property("pressure", PropertyType.ONE_DIMENSION)
#Read serial port
ser = serial.Serial(
    port = os.environ['SERIAL'],
    baudrate = 9600,
    timeout = 2)

#Read next line from serial port and update property values
def serial_to_property_values():
    #Read one line
    line_bytes = ser.readline()
    #If line is not empty
    if len(line_bytes) > 0:
        #Convert bytes to string
        line = line_bytes.decode('utf-8')
        #Split string using commas as separator
        values = line.split(',')
        #Remove first element of list and print the rest
        values.pop(0)
        print(values)

        if my_property is not None:
            my_property.update_values([float(x) for x in values])
        else:
            print('Warning: unknown property' + property_id)

while True:
    serial_to_property_values()
