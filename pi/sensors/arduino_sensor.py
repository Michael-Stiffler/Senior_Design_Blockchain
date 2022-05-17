#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
# dmesg | grep "tty" to find port name

import serial
import time
import queue
import threading
import re

class ArduinoSensor:

    def __init__(self):       
        self.arduino = serial.Serial("/dev/ttyACM0", 9600)
        time.sleep(2)

    def generate_data(self):
        byte_array = self.arduino.readline()
        time.sleep(0.1)
        if "X:" in str(byte_array) and r"\n" in str(byte_array):
            data = byte_array.decode().rstrip()
            return self.clean_data(data)
        else:
            return ""

    def get_data(self):
        return self.generate_data()

    def clean_data(self, data):
        data_ = data
        data_list = [float(s) for s in re.findall(r'-?\d+\.?\d*', data)]
        return data_list
