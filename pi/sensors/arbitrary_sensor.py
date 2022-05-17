#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lsusb to check device name
# dmesg | grep "tty" to find port name

import serial
import time
import queue
import threading
import re
import random
from dotenv import load_dotenv

class ArbitrarySensor:

    def __init__(self):
        load_dotenv()
        time.sleep(2)

    def get_uuid(self):
        return os.getenv('ARBITRARYID')
    
    def get_private_key(self):
        return os.getenv('ARBITRARY_PRIVKEY')

    def get_public_key(self):
        return os.getenv('ARBITRARY_PUBKEY')

    def generate_data(self):
        list_of_floats = []

        for i in range(5):
            list_of_floats.append(random.uniform(1, 10))

        return list_of_floats

    def get_data(self):
        return self.generate_data()
