#!/usr/bin/env python

import psycopg2
import ds18b20_functions as ds18b20
import temperature_functions as tf
from datetime import datetime
from time import sleep

# connect to the databse
conn = psycopg2.connect(database="postgres",
                        user="postgres",
                        password="apassword",
                        host="192.168.0.105",
                        port="5432")

# enable autocommit
conn.autocommit = True

# define cursor
cur = conn.cursor()

# create a table
cur.execute("""CREATE TABLE IF NOT EXISTS temps
               (id SERIAL PRIMARY KEY NOT NULL,
                datetime timestamp NOT NULL,
                room real NOT NULL,
                vent real NOT NULL)""")

# get sensor paths
vent_sensor = ds18b20.sensor_ids['sensor1']
room_sensor = ds18b20.sensor_ids['sensor2']

# continuously read temps
while True:

    # read sensor location
    vent_temp = ds18b20.read_sensor(vent_sensor)
    vent_temp = tf.convert_c_to_f(vent_temp)
    room_temp = ds18b20.read_sensor(room_sensor)
    room_temp = tf.convert_c_to_f(room_temp)

    # get current datetime
    dt_now = datetime.now()

    # put reading into databse
    cur.execute("INSERT INTO temps (datetime, room, vent) VALUES (%s, %s, %s)", [dt_now, room_temp, vent_temp])
    print("{} - room: {}, vent {}".format(dt_now.strftime("%Y-%M-%d %H:%M"), room_temp, vent_temp))

    # sleep for 60 seconds
    sleep(60)
