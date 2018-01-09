#! /usr/bin/env python
from time import sleep
import RPi.GPIO as GPIO
import ds18b20_functions as ds18
import lcd_functions as lf
import temperature_functions as tf


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


def monitor(wait=5):
    """continuous reads all available sensors, and prints temps to lcd"""

    try:

        # get lcd object
        lcd = lf.lcd

        # get avail:able sensors
        sensors = ds18.sensors

        # continuously read sensors
        while True:

            # go through each available sensor
            for sensor in sensors:

                # read sensor
                temp = ds18.read_sensor(sensors[sensor])

                # convert temps from c to f
                temp = tf.convert_c_to_f(temp)

                # pick background color based on temp
                temp_color = pick_color(temp)

                # print temp to LCD
                temp_str = "{}:\n{}".format(sensor, temp)
                lf.display_text(temp_str, color=temp_color)

                # print temp to screen
                #print(temp_str)

                # wait n seconds
                sleep(wait)

    except Exception, e:
        print(str(e))

    finally:
        lcd.clear()
        GPIO.cleanup()


if __name__ == '__main__':
    monitor(wait=5)
