
#!/usr/bin/env python3

# Import required library
from multiprocessing import Process, Pipe
from serial import Serial # To use serial comms with arduino
import signal  # To catch the Ctrl+C and end the program properly
import os  # To access environment variables
from dotenv import \
    load_dotenv  # To load the environment variables from the .env file
from time import sleep

# Serial comms
port = "/dev/ttyACM0"

def serialComms(conn):
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
            # sleep(5)
            try:
                ser.read()
                serData = (ser.readline().decode())
                print("Reading data...")
                print(serData)
                conn.open()
                conn.send(serData)
                conn.close()
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise
