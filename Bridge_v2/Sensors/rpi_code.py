# Get Data
import Adafruit_DHT
import time
#time.strftime("%I:%M:%S")
import csv
import sys

def get_sensors_data(pin:int):
    # Sensors are Adafruit_DHT.DHT22
    sensor = Adafruit_DHT.DHT22

    # # Raspberry Pi with DHT sensor connected to GPIO4 and GPIO11.
    # pin = 4
    # pin = 11

    # Grab a sensor reading.  
    # The read_retry method which will retry up to 15 times to get a sensor reading 
    # (waiting 2 seconds between each retry).
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    
    # Save Data
    if humidity is not None and temperature is not None:
        temperature = round(temperature, 2)
        humidity = round(humidity, 3)
        return temperature,humidity


if __name__ == "__main__":

    csvfile = "temp.csv"
    als = True

    while als: 
        temperature,humidity = get_sensors_data(pin=11)
        if humidity is not None and temperature is not None:
            print(f'Temperature = {temperature}*C  Humidity = {humidity}%')
        else:
            print('can not connect to the sensor!')
        timeC =f"{time.strftime('%Y')}-{time.strftime('%m')}-{time.strftime('%d')} {time.strftime('%I')}:{time.strftime('%M')}:{time.strftime('%S')}" 
        
        data = [temperature, humidity, timeC]

        # Add line of new data to the file
        with open(csvfile, "a")as output:
            writer = csv.writer(output, delimiter=",", lineterminator = '\n')
            writer.writerow(data)

        time.sleep(10) # update script every 60 seconds


# Send Data


## Code to run on the rapsberry Pi

import socket
import numpy as np
import encodings
import Adafruit_DHT ## need to be installed


HOST = '192.168.0.37'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


def my_server():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Server Started waiting for client to connect ")
        s.bind((HOST, PORT))
        s.listen(5)
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)
            while True:

                data = conn.recv(1024).decode('utf-8')

                if str(data) == "Data" or str(data) == "data":

                    print("Ok Sending data ")

                    temperature,humidity = get_sensors_data(pin=4)
                    data = f'{temperature},{humidity}'

                    x_encoded_data = my_data.encode('utf-8')

                    conn.sendall(x_encoded_data)

                elif str(data) == "Quit":
                    print("shutting down server ")
                    break

                if not data:
                    break
                else:
                    pass


if __name__ == '__main__':
    while 1:
        my_server()
