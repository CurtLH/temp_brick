#!/usr/bin/python
import time
import Adafruit_CharLCD as LCD


# Raspberry Pi configuration:
lcd_rs = 27
lcd_en = 22
lcd_d4 = 25
lcd_d5 = 24
lcd_d6 = 23
lcd_d7 = 18
lcd_red = 5
lcd_green = 17
lcd_blue = 7

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

## Initialize the LCD using the pins above.
#lcd = LCD.Adafruit_RGBCharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
#                              lcd_columns, lcd_rows, lcd_red, lcd_green,
#                              lcd_blue, enable_pwm=True)

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, backlight=16, enable_pwm=True)


# Basic colors
colors = {'red': (1.0, 0.0, 0.0),
          'green': (0.0, 1.0, 0.0),
          'blue': (0.0, 0.0, 1.0),
          'yellow': (1.0, 1.0, 0.0),
          'cyan': (0.0, 1.0, 1.0),
          'magenta': (1.0, 0.0, 1.0),
          'white': (1.0, 1.0, 1.0)}


def get_colors(color):

    """returns tuple of numeric color representation"""

    c = colors[color]

    return c[0], c[1], c[2]


def display_text(text, color='cyan'):

    """prints text to LCD"""

    # get color values
    c0, c1, c2 = get_colors(color)

    # display text
    lcd.clear()
    lcd.set_color(c0, c1, c2)
    lcd.message(text)
