#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi or BeagleBone Black.
import time
import Adafruit_CharLCD as LCD
import subprocess


# Raspberry Pi pin configuration:
lcd_rs        = 18  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 23
lcd_d4        = 24
lcd_d5        = 25
lcd_d6        = 8
lcd_d7        = 1
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)


# Print a two line message

lcd.home()
TR=subprocess.getoutput("/opt/vc/bin/vcgencmd measure_temp")
zeit=time.strftime("%y.%b %H:%M:%S")
message="K=111"+chr(223)+"C"+" A=111"+chr(223)+"C"+"\n"+"R="+TR[5:7]+chr(223)+"C Z10 100V"
lcd.message(message)

#lcd.clear()
