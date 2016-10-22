#!/usr/bin/python3
from tkinter import *
import tkinter.font as tkf
import RPi.GPIO as gpio
import time
import threading

BLINK=True
EIN=False
AUS=False

gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
gpio.setup(11, gpio.OUT, gpio.LOW)



mywin = Tk()
mywin.wm_title('Hello World')
myfont=tkf.Font(family='DejaVuSans', size=15)


class BLINKEN(threading.Thread):
    def run(self):
        global BLINK
        while BLINK:
            print("LED AN")
            gpio.output(11,GPIO.HIGH)
            time.sleep(1)
            print("LED AUS")
            gpio.output(11,GPIO.LOW)
            time.sleep(1)
           
def EIN_click():
    global BLINK
    global AUS
    global EIN
    EIN=True
    AUS=False
    BLINK=False
    print(EIN)
    print(AUS)
    print(BLINK)
    print("LED AN")
    gpio.output(11,gpio.LOW)
    
def AUS_click():
    global BLINK
    global AUS
    global EIN
    AUS=True
    EIN=False
    BLINK=False
    print(EIN)
    print(AUS)
    print(BLINK)
    print("LED AUS")
    gpio.output(11,gpio.HIGH)
    
def BLINK_click():
    global BLINK
    global AUS
    global EIN
    BLINK=True
    EIN=False
    AUS=False
    print(EIN)
    print(AUS)
    print(BLINK)
    BLINKEN().start()

def CLEAN():
    GPIO.output(11, gpio.LOW)
    GPIO.cleanup()
    sys.exit()

mylable=Label(mywin,text='Lass die Led tanzen!', font=myfont).pack()
mybutton1 = Button(mywin, text='Led EIN', command=EIN_click).pack(side=LEFT)
mybutton2 = Button(mywin, text='Led AUS', command=AUS_click).pack(side=LEFT)
mybutton3 = Button(mywin, text='Led BLINK', command=BLINK_click).pack(side=LEFT)
mybutton3 = Button(mywin, text='CLEAN GPIO', command=CLEAN).pack(side=LEFT)
mywin.mainloop()





















