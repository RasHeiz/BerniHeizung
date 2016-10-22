#!/usr/bin/python3
import RPi.GPIO as GPIO
import time, sys

GPIO.setmode(GPIO.BOARD)
ledStatus=0

relais1=12
GPIO.setup(relais1, GPIO.OUT)

try:
    while True:
        GPIO.output(relais1, GPIO.LOW)
        print("low")
        time.sleep(5)
        GPIO.output(relais1, GPIO.HIGH)
        print("high")
        time.sleep(5)
except KeyboardInterrupt:
       GPIO.cleanup()
       sys.exit()
