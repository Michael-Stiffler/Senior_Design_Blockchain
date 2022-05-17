# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 10:25:23 2022

@author: Brad
"""

import pyodbc
from datetime import datetime
import datetime as dt
import validation as val
server = 'server_name'
database = 'database_name'
username = 'username'
password = 'password'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                      server+';DATABASE='+database+';UID='+username+';PWD=' + password)
cursor = cnxn.cursor()

cursor.execute("SELECT @@version;")
row = cursor.fetchone()
while row:
    print(row)
    row = cursor.fetchone()

date = datetime.now()
timestamp = datetime.timestamp(date)
print(date)
print("testts = ", timestamp)

# count = cursor.execute("""
# INSERT INTO Sensor_Data (Transaction_ID, Time, Temperature, Humidity, X_value, Y_value, Sensor_ID)
# VALUES (?,?,?,?,?,?,?)""",
# '0x1234959329ILOVEBLOCKCHAINDATETEST', date, 70.8, 60.7, 50,100,"DHT22").rowcount
# cnxn.commit()
#print('Rows inserted: ' + str(count))


# trying to make something that can be nicely referenced in the server down here -Alex

def get24HFromEpoch(epoch: int):

    giventime = datetime.fromtimestamp(epoch/1000)
    givenplus24 = giventime + dt.timedelta(days=1)
    print()
    dataout = []

    query = "SELECT * FROM Sensor_Data"
    try:
        for row in cursor.execute(query):

            pulledtime = row[1]

            if (pulledtime >= giventime and pulledtime < givenplus24):
                dataout.append(row)

    except Exception as e:
        print(e)

    return dataout


def addEntryNOW(temperature, humidity, xval, yval, sensname, sig):
    print(sensname)

    date = datetime.now()  # - dt.timedelta(days=1)
    timestamp = datetime.timestamp(date)
    print(date)
    print("testts = ", timestamp)

    count = cursor.execute("""
    INSERT INTO Sensor_Data (Transaction_ID, Time, Temperature, Humidity, X_value, Y_value, Sensor_ID, Signature) 
    VALUES (?,?,?,?,?,?,?)""",
                           '0x1234959329ILOVEBLOCKCHAINDATETEST', date, temperature, humidity, xval, yval, sensname, sig).rowcount
    cnxn.commit()
    print('Rows inserted: ' + str(count))

# i know this is horribly redundant I'm sorry lmfao


def addEntry(n, tag):
    count = cursor.execute("""
    INSERT INTO Sensor_Data (Transaction_ID, Time, Temperature, Humidity, X_value, Y_value, Sensor_ID, Tag) 
    VALUES (?,?,?,?,?,?,?,?)""",
                           n[0], n[1], n[2], n[3], n[4], n[5], n[6], tag).rowcount  # actual brain rot happening
    cnxn.commit()
    print('Rows inserted: ' + str(count))
