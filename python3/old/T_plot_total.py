#!/usr/bin/python3
#-*- coding:utf-8 -*-
#Datei grafik-csv.py
from __future__ import division, print_function
from time import strftime
import csv, pygame, pygame.gfxdraw, time, sys, spidev
from pygame.locals import *

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

def logT(T,file):
    date=strftime("%Y-%m-%d %H:%M:%S")
    with open(file,'a') as out:
        cw=csv.writer(out, delimiter=',', lineterminator='\n',quotechar='"')
        cw.writerow([date,T])

def plotY(caption,yMin,yMax,tStep,B,H,file):
    #Konstanten
    WHITE=(255,255,255)
    RED=(255,0,0)
    BLUE=(0,0,255)
    GREY=(200,200,200)
    boarder=50
    Steps=B-2*boarder+1 # für kleinste Schrittweite von 1px (muss Integer ergeben)
    
    #DatenBereich
    data=[]
    with open(file)as f:
        cr=csv.reader(f)
        for line in cr:
            data.append(line)
            data=data[-Steps:]
    #DiagrammFlaeche
    pygame.init()
    surf=pygame.display.set_mode((B,H),0,32)
    surf.fill(WHITE)
    pygame.display.set_caption(caption)
    myfont=pygame.font.SysFont('FreeSerif.ttf',16)
    
    #yAchse
    pygame.draw.line(surf,BLUE,(boarder,H-boarder),(boarder,boarder),1)
    pygame.draw.line(surf,BLUE,(B-boarder,H-boarder),(B-boarder,boarder),1)
    mulySkala1=0
    mulySkala=0
    stepySkala=15
    
    while mulySkala<stepySkala:
        mulySkala=mulySkala1
        ySkala=(yMax-yMin)/stepySkala*mulySkala+yMin
        yPos=int(H-(ySkala-yMin)/(yMax-yMin)*(H-2*boarder)-boarder-5)
        ytxt=u'%.1f°C' % ySkala
        textsurf=myfont.render(ytxt.encode('latin-1'),1,(0,0,0))
        surf.blit(textsurf,(5,yPos))
        pygame.draw.line(surf,GREY,(boarder,yPos+5),(B-boarder,yPos+5),1)
        mulySkala1=mulySkala+1

    #xAchse
    pygame.draw.line(surf,BLUE,(boarder,H-boarder),(B-boarder,H-boarder),1)
    mulxSkala1=0
    mulxSkala=0
    stepxSkala=10
    while mulxSkala<stepxSkala:
        mulxSkala=mulxSkala1
        xSkala=(Steps*tStep)/60/stepxSkala*mulxSkala
        #xSkala=1
        xPos=int(B-(xSkala-0)/(Steps*tStep/60-0)*(B-2*boarder)-boarder)
        xtxt=u'-%.1fmin' % xSkala
        textsurf=myfont.render(xtxt.encode('latin-1'),1,(0,0,0))
        surf.blit(textsurf,(xPos-15,H-boarder+10))
        mulxSkala1=mulxSkala+1         

    # Punkte
    x=boarder #xPos erster Punkt
    x0=boarder #xPos des vorherigen Punktes
    for messpunkt in data:
        if x0>boarder:
            yPlot0=yPlot
        yValue=float(messpunkt[1])
        yPlotY=int(H-(yValue-yMin)/(yMax-yMin)*(H-2*boarder)-boarder)
        if yPlotY>boarder:
            yPlot=yPlotY
        else:
            yPlot=H-boarder
        if x0 is boarder:
            yPlot0=yPlot
        pygame.draw.line(surf,RED,(x0,yPlot0),(x,yPlot),2) #Linie vom vorherigen Punkt zum aktuellen        
        x0=x
        x+= 1 #Schrittweite fix auf kleinstmögliche        
    pygame.display.update()

r=0
s=0
t=0
u=0
v=0
w=0
x=0
y=0
z=0
T=0

while True:
    Tfile='T.csv'
    tStep=1
    xtStep=15
    for i in range(1,xtStep+1):
        r=s
        s=t
        t=u
        u=v
        v=w
        w=x
        x=y
        y=z
        if T>0:
            z=T
        T=getT(0,1000,3.29406,0.00322)    
        if r>1:
            Tm=(r+s+t+u+v+w+x+y+z+T)/10
            print(Tm)
        time.sleep(tStep)    

    tStepPlot=xtStep*tStep
    logT(Tm,Tfile)    
    plotY('Temperatur-Plot',20,60,tStepPlot,1800,400,Tfile)

    
