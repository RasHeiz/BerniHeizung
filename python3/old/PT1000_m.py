#!/usr/bin/python3
import spidev
import time
from time import strftime
import csv
spi=spidev.SpiDev()
spi.open(0,1)

wert=1
w=1
x=1
y=1
z=1
temp=1

while True:
    w=x
    x=y
    y=z
    z=temp
    antwort=spi.xfer([1,128,0])
    if 0<= antwort[1]<=3:
        vMax=3.29406
        vMin=0.00322
        vRange=vMax-vMin
        rAdd=1000
        wert=((antwort[1]*256)+antwort[2])*0.00322
        # print(wert," V",)
        if wert<0 or wert>0:
            ohm=(vRange-wert)/(wert)*rAdd
            # print(ohm," Ohm",)
            temp=1.1072597754889e-5*ohm*ohm+0.2331563968*ohm-244.1819649032
            print(temp," °C",)
            print(z)
            print(y)
            print(x)
            print(w)
        date=strftime("%Y-%m-%d %H:%M:%S")
        # print(date)
        tempM=(w+x+y+z+temp)/5
        print(tempM)
        with open('out.csv','a') as out:
            cw=csv.writer(out, delimiter=',', lineterminator='\n',quotechar='"')
            cw.writerow([date,tempM])
    time.sleep(3)
