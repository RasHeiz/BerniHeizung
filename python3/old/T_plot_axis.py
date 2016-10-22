#!/usr/bin/python3
#-*- coding:utf-8 -*-
#Datei grafik-csv.py
from __future__ import division, print_function
import csv, pygame, pygame.gfxdraw, time, sys
from pygame.locals import *

def f(ANZOHL):
    #Konstanten
    (B,H)=(800,600)
    (TMIN,TMAX)=(15,50)
    (ANZSTEP)= ANZOHL
    WHITE=(255,255,255)
    RED=(255,0,0)
    GREEN=(0,255,0)
    BLUE=(0,0,255)
    GREY=(200,200,200)
    boarder=40

    data=[]
    with open('out.csv')as f:
        cr=csv.reader(f)
        for line in cr:
            data.append(line)
            data=data[-ANZSTEP:]
    print(data)

    pygame.init()
    surf=pygame.display.set_mode((B,H),0,32)
    surf.fill(WHITE)
    pygame.display.set_caption('Temperatur-Plot')
    myfont=pygame.font.SysFont('FreeSerif.ttf',14)
    x=boarder
    
    mulySkala1=0
    mulySkala=0
    stepySkala=15
    while mulySkala<stepySkala:
        mulySkala=mulySkala1
        ySkala=(TMAX-TMIN)/stepySkala*mulySkala+TMIN
        yPos=int(H-(ySkala-TMIN)/(TMAX-TMIN)*(H-2*boarder)-boarder-5)
        ytxt=u'%.1f°C' % ySkala
        textsurf=myfont.render(ytxt.encode('latin-1'),1,(0,0,0))
        surf.blit(textsurf,(5,yPos))
        pygame.draw.line(surf,GREY,(boarder,yPos+5),(B-boarder,yPos+5),1)
        mulySkala1=mulySkala+1

    mulxSkala1=0
    mulxSkala=0
    stepxSkala=10
    while mulxSkala<stepxSkala:
        mulxSkala=mulxSkala1
        xSkala=(145*5)/60/stepxSkala*mulxSkala
        #xSkala=1
        xPos=int(B-(xSkala-0)/(145*5/60-0)*(B-2*boarder)-boarder-10)
        xtxt=u'-%.1fmin' % xSkala
        textsurf=myfont.render(xtxt.encode('latin-1'),1,(0,0,0))
        surf.blit(textsurf,(xPos,H-25))
        mulxSkala1=mulxSkala+1 

    pygame.draw.line(surf,BLUE,(boarder,H-boarder),(B-boarder,H-boarder),1)
    pygame.draw.line(surf,BLUE,(boarder,H-boarder),(boarder,boarder),1)
    #pygame.draw.line(surf,BLUE,(B-boarder,H-boarder),(B-boarder,boarder),1)    
        

    for messpunkt in data:
        tPlot=float(messpunkt[1])
        # print(tPlot)
        yPlotY=int(H-(tPlot-TMIN)/(TMAX-TMIN)*(H-2*boarder)-boarder)
        if yPlotY>boarder:
            yPlot=yPlotY
        else:
            yPlot=H-boarder
            
        pygame.gfxdraw.aacircle(surf, x, yPlot, 1, RED)
        pygame.gfxdraw.filled_circle(surf, x, yPlot, 1, RED)
        
        #txt=u'%.1f°C' % tPlot
        #textsurf=myfont.render(txt.encode('latin-1'),1,(0,0,0))
        #surf.blit(textsurf,(x,yPlot-30))

        x+=B // (ANZSTEP)

    pygame.display.update()

while True:
    f(145)
    time.sleep(1)
    
