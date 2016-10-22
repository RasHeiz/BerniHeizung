#!/usr/bin/python3
#-*- coding:utf-8 -*-
#Datei grafik-csv.py
from __future__ import division, print_function
import spidev
from time import strftime

import csv, pygame, pygame.gfxdraw, time, sys
from pygame.locals import *

spi=spidev.SpiDev()
spi.open(0,1)

wert=1
w=1
x=1
y=1
z=1
temp=1

#Konstanten
(B,H)=(800,600)
(TMIN,TMAX)=(15,50)
(ANZSEK)= 10
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

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

    data=[]
    with open('out.csv')as f:
        cr=csv.reader(f)
        for line in cr:
            data.append(line)
            data=data[-ANZSEK:]
    # print(data)

    pygame.init()
    surf=pygame.display.set_mode((B,H),0,32)
    surf.fill(WHITE)
    pygame.display.set_caption('Temperatur-Plot')
    myfont=pygame.font.SysFont('FreeSerif.ttf',14)
    x=20

    for messpunkt in data:
        tPlot=float(messpunkt[1])
        # print(tPlot)
        yPlot=int(H-(tPlot-TMIN)/(TMAX-TMIN)*H)

        pygame.gfxdraw.aacircle(surf, x, yPlot, 5, RED)
        pygame.gfxdraw.filled_circle(surf, x, yPlot, 5, RED)

        txt=u'%.1f°C' % tPlot
        textsurf=myfont.render(txt.encode('latin-1'),1,(0,0,0))
        surf.blit(textsurf,(x+5,yPlot-12))

        x+=B // (ANZSEK+1)

    pygame.display.update()
    time.sleep(1)
