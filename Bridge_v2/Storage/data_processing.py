## gere l'arrivee des données en provenance du raspberry pi
## stocke ces données dans une base de données (temp ? Mongo ? Ram ?)
## compare ces données au seuil, stats etc.. pour les alertes 
## compare ces données aux data prédites


import socket
import threading
import time


HOST = '192.168.0.37' #'https://eco-capt-bridge.herokuapp.com'  # The server's hostname or IP address
PORT = 65432       # The port used by the server


def process_data_from_server(x):
    x1, y1 = x.split(",")
    return x1, y1


def my_client():
    # run the client after 11 seconds
    threading.Timer(11, my_client).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        my = input("Enter command ")

        #my = "Data"

        my_inp = my.encode('utf-8')

        s.sendall(my_inp)

        data = s.recv(1024).decode('utf-8')

        x_temperature, y_humidity = process_data_from_server(data)

        print("Temperature {}".format(x_temperature))
        print("Humidity {}".format(y_humidity))

        s.close()
        time.sleep(5)


if __name__ == "__main__":
    while 1:
        my_client()
