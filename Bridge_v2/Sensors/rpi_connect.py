## connection au raspberry et recolte des mesures des capteurs

# Script to read temperature data from the DHT11:
# Import first Adafruit DHT bibliotheek.
import Adafruit_DHT
import time
als = True
while als: 
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4) #on gpio pin 4 or pin 7
    if humidity is not None and temperature is not None:
      humidity = round(humidity, 2)
      temperature = round(temperature, 2)
      print(f'Temperature = {temperature}*C  Humidity = {humidity}%')
    else:
      print('can not connect to the sensor!')
    time.sleep(60) # read data every minute


## Update from the Script above with modification of writing the data to a CSV.file:
# Import first Adafruit DHT bibliotheek.
#time.strftime("%I:%M:%S")
import Adafruit_DHT
import time
import csv
import sys
csvfile = "temp.csv"
als = True
while als: 
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4) # gpio pin 4 or pin number 7
    if humidity is not None and temperature is not None:
      humidity = round(humidity, 2)
      temperature = round(temperature, 2)
      print(f'Temperature = {temperature}*C  Humidity = {humidity}%')
    else:
      print('can not connect to the sensor!')
    timeC = time.strftime("%I")+':' +time.strftime("%M")+':'+time.strftime("%S")
    data = [temperature, timeC]

    with open(csvfile, "a")as output:
        writer = csv.writer(output, delimiter=",", lineterminator = '\n')
        writer.writerow(data)
    time.sleep(6) # update script every 60 seconds


## Code to run on the rapsberry Pi

import socket
import numpy as np
import encodings
import Adafruit_DHT ## need to be installed


HOST = '192.168.1.4'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


def random_data():
    pin = 4
    sensor = Adafruit_DHT.DHT22
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        temperature = int(temperature)
        humidity = int(humidity)
        print(f'Temp={temperature}*C  Humidity={humidity}%')
        print(f"data was written on database T{temperature} H{humidity}")
        data = f'{temperature},{humidity}'
        return data


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

                    my_data = random_data()

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
