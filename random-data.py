from random import random
import time
from dcd.entities.thing import Thing
from dcd.entities.property import PropertyType

from dotenv import load_dotenv
import os

#Thing ID and access token
load_dotenv()
THING_ID = os.environ['THING_ID']
THING_TOKEN = os.environ['THING_TOKEN']

#Instantiate thing with its credentials
my_thing = Thing(thing_id=THING_ID, token=THING_TOKEN)
#Fetch thing details
my_thing.read()
# print(my_thing.to_json())

#Create random properties
my_property = my_thing.find_or_create_property("My Random Property", PropertyType.THREE_DIMENSIONS)
#Print random property - includes name, ID and dimensions
print(my_property.to_json())

#Function that generates random values
def generate_dum_property_values(the_property):
    #Define a trio with current time and 3 random values
    values = (random(), random(), random())
    #Update values of property
    the_property.update_values(values)

#Call function to start generating dummy values
while True:
    generate_dum_property_values(my_property)
    #2-second break
    time.sleep(2)
