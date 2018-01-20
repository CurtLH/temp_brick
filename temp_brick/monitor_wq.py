#! /usr/bin/env python
from time import sleep
import RPi.GPIO as GPIO 
import lcd_functions as lf
import temperature_functions as tf
import psycopg2


def get_weather():

    """returns most recent temperature"""
    
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="apassword",
                            host="192.168.0.104") 

    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("""SELECT condition -> 'current_observation' -> 'temp_f' 
                   FROM arlington_weather_condition
                   WHERE id = (SELECT MAX(id) FROM arlington_weather_condition)""")


    temp_f = [i[0] for i in cur][0]


    return temp_f


def get_forecast():

    """returns most recent forecast"""
    
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="apassword",
                            host="192.168.0.104") 

    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("""SELECT forecast -> 'forecast' -> 'simpleforecast' -> 'forecastday' 
                    FROM arlington_weather_forecast 
                    WHERE id = (SELECT MAX(id) 
                                FROM arlington_weather_forecast);""")

    data = [i[0] for i in cur][0][0]

    low = str(data['low']['fahrenheit'])
    high = str(data['high']['fahrenheit'])

    return low, high


def pick_color(temp):

    """returns color name based on temp"""

    if temp >= 90.0:
        color = 'red'
    elif temp < 90.0 and temp >= 80.0:
        color = 'yellow'
    elif temp < 80.0 and temp >= 70.0:
        color = 'green'
    elif temp < 70.0 and temp >= 60.0:
        color = 'cyan'
    elif temp < 60.0 and temp >= 50.0:
        color = 'blue'
    else:
        color = 'white'

    return color


def monitor(wait=60):
    """continuous print latest temp to lcd"""

    try:

        # get lcd object
        lcd = lf.lcd

        # continuously read sensors
        while True:

                # get the latest temp
                temp = get_weather()
            
                # get low/high
                low, high = get_forecast()

                # pick background color based on temp
                temp_color = pick_color(temp)

                # create string to print to screen
                temp_str = "   Temp: {}\nHigh: {} Low: {}".format(temp, high, low)
                
                # display temp on LCD and set RGB color based on temp
                lf.display_text(temp_str, color=temp_color)

                # print temp to screen
                print(temp_str)
                
                # wait n seconds
                sleep(wait)

    except Exception, e:
        print(str(e))

    finally:
        lcd.clear()
        GPIO.cleanup()


if __name__ == '__main__':
    monitor()
