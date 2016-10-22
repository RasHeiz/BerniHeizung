#!/usr/bin/python3
#-*- coding:utf-8 -*-
#Datei grafik-csv.py
from __future__ import division, print_function
import csv, pygame, pygame.gfxdraw, time, sys
from pygame.locals import *

def f(caption,yMin,yMax,tStep,B,H):
    #Konstanten
    WHITE=(255,255,255)
    RED=(255,0,0)
    BLUE=(0,0,255)
    GREY=(200,200,200)
    boarder=50
    Steps=B-2*boarder+1 # für kleinste Schrittweite von 1px (muss Integer ergeben)
    
    #DatenBereich
    data=[]
    with open('out.csv')as f:
        cr=csv.reader(f)
        for line in cr:
            data.append(line)
            data=data[-Steps:]
    #DiagrammFlaeche
    pygame.init()
    surf=pygame.display.set_mode((B,H),0,32)
    surf.fill(WHITE)
    pygame.display.set_caption(caption)
    myfont=pygame.font.SysFont('FreeSerif.ttf',14)
    
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
        pygame.draw.line(surf,RED,(x0,yPlot0),(x,yPlot),2)        
        x0=x
        x+= 1 #Schrittweite fix auf kleinstmögliche        
    pygame.display.update()

while True:
    tStep=1
    f('Temperatur-Plot',15,30,tStep,1000,400)
    time.sleep(tStep)
    
