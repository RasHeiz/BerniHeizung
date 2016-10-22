#!/usr/bin/python3
import spidev
import time
from time import strftime
import csv

def getT(port, RAdd, UMax, UMin):
    spi=spidev.SpiDev()
    spi.open(0,1)
    
    if port is 0:
        Port=128
    elif port is 1:
        Port=144
    elif port is 2:
        Port=160
    elif port is 3:
        Port=176
    elif port is 4:
        Port=192
    elif port is 5:
        Port=208
    elif port is 6:
        Port=224
    elif port is 7:
        Port=240
        
    antwort=spi.xfer([1,Port,0])
    if 0<= antwort[1]<=3:
        URange=UMax-UMin
        wert=((antwort[1]*256)+antwort[2])*0.00322
        # print(wert," V",)
        if wert>0:
            R=(URange-wert)/(wert)*RAdd
            # print(ohm," Ohm",)
            T=1.1072597754889e-5*R*R+0.2331563968*R-244.1819649032
            # print(temp," °C",)
        else:
            T=0
    else:
        T=0
    return T

def logT(T):
    date=strftime("%Y-%m-%d %H:%M:%S")
    with open('out.csv','a') as out:
        cw=csv.writer(out, delimiter=',', lineterminator='\n',quotechar='"')
        cw.writerow([date,T])
    


w=1
x=1
y=1
z=1
T=1

while True:
    tStep=1
    w=x
    x=y
    y=z
    if T>0:
        z=T
    T=getT(0,1000,3.29406,0.00322)    
    if w>1:
        Tm=(w+x+y+z+T)/5
        print(Tm)
        logT(Tm)    
    time.sleep(1)
    
