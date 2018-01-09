#! /usr/bin/env python
import os
import glob
import click

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# name and file path for all sensors
sensor_ids = {'sensor1' : '/sys/bus/w1/devices/28-0415a44740ff/w1_slave', 
              'sensor2' : '/sys/bus/w1/devices/28-0415a455b8ff/w1_slave',
              'sensor3' : '',
              'sensor4' : '',
              'sensor5' : ''}

# check directory to find which sensors are available
base_dir = '/sys/bus/w1/devices/'
devices = glob.glob(base_dir + "28*")

# get paths for only active sensors
sensors = {}
for sensor in sensor_ids:
    if sensor_ids[sensor][:35] in devices:
        sensors[sensor] = sensor_ids[sensor]


def read_sensor_raw(device_file):

    """return raw value from one sensor"""
    
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    
    return lines


def read_sensor(device_file):
    
    """parse raw value into temp"""

    lines = read_sensor_raw(device_file)
    
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_sensor_raw()
    equals_pos = lines[1].find('t=')
    
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        
        return temp_c


def read_multiple_sensors(sensors):

    """takes reading from all sensors"""

    # create an empty dict to add sensor readings to
    readings = {}
    
    # get readings for all sensor files within sensors
    for sensor in sensors.keys():
        readings[sensor] = read_sensor(sensors[sensor])

    return readings


@click.command()
@click.option('--device', type=click.Choice(sensors.keys()), 
              help='select the sensor to read')
def cli(device):

    """read the temperature of a sensor"""

    print(read_sensor(sensors[device]))

if __name__ == '__main__':
   cli()
