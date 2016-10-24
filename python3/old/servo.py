#!/usr/bin/python3
# servo.py
import time
import pigpio
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(38,GPIO.OUT)
GPIO.setup(32,GPIO.OUT)
GPIO.setup(36,GPIO.OUT)

GPIO.output(32,GPIO.HIGH)
GPIO.output(36,GPIO.LOW)





def servo(servo, pos):
    pi=pigpio.pi()
    pi.set_mode(servo, pigpio.OUTPUT)
    pi.set_servo_pulsewidth(servo, pos)
    time.sleep(1)
    pi.set_servo_pulsewidth(servo,0)
    pi.stop()



while True:
    GPIO.output(38, GPIO.LOW)
    time.sleep(0.5)
    servo(3,1100)
    time.sleep(0.1)
    servo(3,1330)#610-2450
    print("100V")
    GPIO.output(38, GPIO.HIGH)
    time.sleep(30)
    GPIO.output(38, GPIO.LOW)
    time.sleep(0.5)
    servo(3,1100)
    time.sleep(0.1)
    servo(3,1380)#610-2450
    print("90V")
    GPIO.output(38, GPIO.HIGH)
    time.sleep(30)
    GPIO.output(38, GPIO.LOW)
    time.sleep(0.5)
    servo(3,1100)
    time.sleep(0.1)
    servo(3,1420)#610-2450
    print("82V")
    GPIO.output(38, GPIO.HIGH)
    time.sleep(30)
    GPIO.output(38, GPIO.LOW)
    time.sleep(0.5)
    servo(3,1100)
    time.sleep(0.1)
    servo(3,1465)#610-2450
    print("74V")
    GPIO.output(38, GPIO.HIGH)
    time.sleep(30)
    GPIO.output(38, GPIO.LOW)
    time.sleep(0.5)
    servo(3,1100)
    time.sleep(0.1)
    servo(3,1505)#610-2450
    print("67V")
    GPIO.output(38, GPIO.HIGH)
    time.sleep(30)


    #1275 - 100V
    #1330 - 90V
    #1375 - 82V
    #1420 - 74V
    #1480 - 67V
    
    
    
    
    
