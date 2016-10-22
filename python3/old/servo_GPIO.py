#!/usr/bin/python3
# servo.py
import time
import RPi.GPIO as GPIO

servo_pin=5

GPIO.setmode(GPIO.BOARD)


GPIO.setup(32,GPIO.OUT)
GPIO.output(32, GPIO.LOW)

GPIO.setup(servo_pin, GPIO.OUT)
p=GPIO.PWM(servo_pin,50)
p.start(7.5)


    
p.ChangeDutyCycle(9)
time.sleep(0.5)
p.ChangeDutyCycle(0)
        
time.sleep(60)

p.stop()
GPIO.cleanup()
