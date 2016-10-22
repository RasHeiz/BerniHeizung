#!/usr/bin/python3
#-*- coding:utf-8 -*-
#Datei grafik-csv.py
from __future__ import division, print_function
import csv, pygame, pygame.gfxdraw, time, sys
from pygame.locals import *

def f(ANZOHL):
    #Konstanten
    (B,H)=(800,600)
    (TMIN,TMAX)=(20,50)
    (ANZSEK)= ANZOHL
    WHITE=(255,255,255)
    RED=(255,0,0)
    GREEN=(0,255,0)
    BLUE=(0,0,255)

    data=[]
    with open('out.csv')as f:
        cr=csv.reader(f)
        for line in cr:
            data.append(line)
            data=data[-ANZSEK:]
    print(data)

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

        pygame.gfxdraw.aacircle(surf, x, yPlot, 2, RED)
        pygame.gfxdraw.filled_circle(surf, x, yPlot, 2, RED)

        #txt=u'%.1f°C' % tPlot
        #textsurf=myfont.render(txt.encode('latin-1'),1,(0,0,0))
        #surf.blit(textsurf,(x,yPlot-30))

        x+=B // (ANZSEK+1)

    pygame.display.update()

f(150)
    
