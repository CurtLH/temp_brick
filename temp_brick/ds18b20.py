#! /usr/bin/env python
import os
import glob
import click
from datetime import datetime
import psycopg2

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


def read_sensor_raw():

    """return raw value from one sensor"""
    
    f = open('/sys/bus/w1/devices/28-0415a45a31ff/w1_slave', 'r')
    lines = f.readlines()
    f.close()
    
    return lines


def read_sensor():
    
    """parse raw value into temp"""

    lines = read_sensor_raw()
    
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_sensor_raw()
    equals_pos = lines[1].find('t=')
    
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = round(temp_c * 9.0 / 5.0 + 32.0, 1)
        return temp_f


def store_temp_inside():

    """store current temperature in database"""

    temp = read_sensor()
    now = datetime.now()

    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="apassword",
                            host="192.168.0.104") 

    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS inside_temp
                   (id SERIAL PRIMARY KEY NOT NULL,
                    datetime timestamp NOT NULL,
                    temp real NOT NULL)""")
    
    cur.execute("INSERT INTO inside_temp (datetime, temp) VALUES (%s, %s)", [now, temp])


if __name__ == '__main__':

    # get temp and store in db
    store_temp_inside()
