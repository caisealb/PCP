from dcd.entities.thing import Thing
from dcd.entities.property import PropertyType

from dotenv import load_dotenv
import os

load_dotenv()
THING_ID = os.environ['THING_ID']
THING_TOKEN = os.environ['THING_TOKEN']

my_thing = Thing(thing_ID=THING_ID, token=THING_TOKEN)
my_thing.read()
print(my_thing.to_json())

my_property = my_thing.find_or_create_property("My Random Property", PropertyType.THREE_DIMENSIONs)
print(my_property.to_json())
