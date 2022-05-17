import socket
from sensors import arduino_sensor, arbitrary_sensor
import time
from sign_data import *
from dotenv import load_dotenv
import os
import hashlib
import secrets
import json


def main():
    load_dotenv()

    UUID = os.getenv('UUID_ENROLLMENT')
    HOST = os.getenv('HOST')
    PORT = int(os.getenv('PORT'))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

 #   list_of_sensors = [arduino_sensor.ArduinoSensor(), arbitrary_sensor.ArbitrarySensor()]

    list_of_sensors = [arduino_sensor.ArduinoSensor()]
    grab_data_for_sensors(s, list_of_sensors, UUID)


def grab_data_for_sensors(s, list_of_sensors, UUID):

    FORMAT = "utf-8"
    while True:
        for sensor in list_of_sensors:

            data = sensor.get_data()

            if len(data) > 0:
                data.pop(2)

                str_data = '|'.join(str(e) for e in data)
                encode = SignData(str_data, UUID)
                json_data = json.dumps(encode)

                s.send(json_data.encode(FORMAT))
                reply = s.recv(1024).decode(FORMAT)

                print(reply)

            time.sleep(.1)


if __name__ == "__main__":
    main()
