##### CODE THAT RUN ON THE RASPBERRY #####

# Get Data
# import Adafruit_DHT
import time
import datetime as dt
#time.strftime('%I:%M:%S')
import csv
import sys
import re,uuid
from pprint import pprint

def get_mac_address():
    # ether en0 or wlan0
    mac = ''.join(re.findall('..', '%012x' % uuid.getnode())) 
    return mac

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
    timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #f"{time.strftime('%Y')}-{time.strftime('%m')}-{time.strftime('%d')} {time.strftime('%I')}:{time.strftime('%M')}:{time.strftime('%S')}"
    
    # Save Data
    if humidity is not None and temperature is not None:
        temperature = round(temperature, 2)
        humidity = round(humidity, 3)
        return temperature, humidity, timestamp

# Send Data
import requests

def fake_data_for_demo(n):
    temperature = [34, 40, 38, 41, 43, 39]
    humididy = [47,56,45,44,59,48]
    timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return temperature[n],humididy[n],timestamp

def send_data(temperature:float, humidity:float, timestamp:str, mac_address:str, _serviceId:int):

    # url_heroku = 'https://eco-capt-bridge.herokuapp.com/sensors'
    url = 'http://127.0.0.1:5000/sensors'

    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'temperature':temperature,
        'humidity': humidity,
        'timestamp' : timestamp,
        "mac_address": mac_address,
        '_serviceId':_serviceId
    }
    
    pprint(data)

    resp = requests.post(url, headers=headers, json=data)

    return resp
    

if __name__ == '__main__':
    
    csvfile = 'temp.csv'
    isActive = False
    _serviceId = 0
    mac_address = get_mac_address()

    while isActive : 
        temperature,humidity,timestamp = get_sensors_data(pin=4)
        if humidity is not None and temperature is not None:
            print(f'Temperature = {temperature}*C  Humidity = {humidity}%')
        else:
            print('can not connect to the sensor!')
        # timeC =f'{time.strftime('%Y')}-{time.strftime('%m')}-{time.strftime('%d')} {time.strftime('%I')}:{time.strftime('%M')}:{time.strftime('%S')}' 
        
        data = [temperature, humidity, timestamp, mac_address,_serviceId]

        # Add line of new data to the file
        # with open(csvfile, 'a')as output:
        #     writer = csv.writer(output, delimiter=',', lineterminator = '\n')
        #     writer.writerow(data)

        resp = send_data(temperature, humidity, timestamp, mac_address, _serviceId)
        print(data)
        time.sleep(10) # update script every 10 seconds
    # temperature,humidity,timestamp = get_sensors_data(pin=4)
    # resp = send_data(temperature, humidity, timestamp, mac_address, _serviceId)

    for i in range(5):
        print(f"\n\nPHASHE {i}\n\n")
        n = 0        
        while n < 6 :
            temperature, humidity, timestamp = fake_data_for_demo(n)
            if i == 2 :
                temperature = temperature + 4*i
            elif i == 4:
                temperature = temperature
            else :
                temperature = temperature + 2*i

            resp = send_data(temperature, humidity, timestamp,
                            mac_address, _serviceId)
            n += 1
            print("\n")
            time.sleep(20)
