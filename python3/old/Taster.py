#!/usr/bin/python3
import RPi.GPIO as GPIO
import time, sys

GPIO.setmode(GPIO.BOARD)
ledStatus=0

GPIO.setup(11, GPIO.IN)

def switch_on(pin):
    if GPIO.input(11) is 1:
        print(GPIO.input(11))
        time.sleep(1)
        print(GPIO.input(11))
        if GPIO.input(11) is 0:
            global ledStatus
            ledStatus = not ledStatus
            print(ledStatus)

GPIO.add_event_detect(11, GPIO.FALLING, bouncetime=1000)
GPIO.add_event_callback(11,switch_on)

try:
    while True:
        time.sleep(1)
        print(GPIO.input(11))
except KeyboardInterrupt:
    GPIO.cleanup()
    sys.exit()
