#!/usr/bin/python3
#-*- coding:utf-8 -*-
#Datei grafik-csv.py
from __future__ import division, print_function
import csv, pygame, pygame.gfxdraw, time, sys, spidev, threading, pigpio
from pygame.locals import *

def Servo():#610-2450
    global servo
    global pos
    global servoAktive
    servoAktive=1
    pi=pigpio.pi()
    pi.set_mode(servo, pigpio.OUTPUT)
    pi.set_servo_pulsewidth(servo, pos)
    time.sleep(5)
    pi.set_servo_pulsewidth(servo,0)
    pi.stop()
    servoAktive=0

def getT(port, RAdd, UMax, UMin):

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

def logT(Tm,tm,file):
    timeStamp=time.time()
    #date=strftime("%Y-%m-%d %H:%M:%S")
    with open(file,'a') as out:
        cw=csv.writer(out, delimiter=',', lineterminator='\n',quotechar='"')
        cw.writerow([tm,Tm])

def plotY():
    global caption
    global yMin
    global yMax
    global tStep
    global B
    global H
    global file
    
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
    pygame.draw.line(surf,BLUE,(boarder,H-boarder),(boarder,boarder),2)
    pygame.draw.line(surf,BLUE,(B-boarder,H-boarder),(B-boarder,boarder),2)
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

    #xAchse-Linien und Positionen der Skalenwerte
    pygame.draw.line(surf,BLUE,(boarder,H-boarder),(B-boarder,H-boarder),2)
    mulxSkala1=0
    mulxSkala=0
    stepxSkala=10
    (xA10,xA9,xA8,xA7,xA6,xA5,xA4,xA3,xA2,xA1,xA0)=(0,0,0,0,0,0,0,0,0,0,0)
    while mulxSkala<stepxSkala:
        mulxSkala=mulxSkala1
        xSkala=((Steps-1)*tStep)/3600/stepxSkala*mulxSkala
        #xSkala=1
        xPos=int(B-(xSkala-0)/(Steps*tStep/3600-0)*(B-2*boarder)-boarder)
        (xA10,xA9,xA8,xA7,xA6,xA5,xA4,xA3,xA2,xA1,xA0)=(xPos,xA10,xA9,xA8,xA7,xA6,xA5,xA4,xA3,xA2,xA1) # Speichern der Positionen xA0 bis xA10
        pygame.draw.line(surf, BLUE,(xPos, H-boarder-5),(xPos, H-boarder+10),2)
        mulxSkala1=mulxSkala+1

    

    # Punkte
    x=boarder #xPos erster Punkt
    x0=boarder #xPos des vorherigen Punktes
    xmul=0
    xmul1=0
    for messpunkt in data:
        if x0>boarder:  #speichern des vorgängers
            yPlot0=yPlot
        yValue=float(messpunkt[1])
        
        #Auslesen des Zeitstempels der y-Werte an den Positionen der x-Skala
        if x==xA10 or x==xA9 or x==xA8 or x==xA7 or x==xA6 or x==xA5 or x==xA4 or x==xA3 or x==xA2 or x==xA1 or x==xA0:
            xValue=float(messpunkt[0])
            timeLoc=time.localtime(xValue)
            Date=time.strftime("%d/%m/%y %H:%M:%S", timeLoc)            
            textsurf=myfont.render(Date.encode('latin-1'),1,(0,0,0))
            surf.blit(textsurf,(x-boarder+8,H-boarder+12))

        yPlotY=int(H-(yValue-yMin)/(yMax-yMin)*(H-2*boarder)-boarder)
        
        if yPlotY>boarder and yPlotY<H-boarder: 
            yPlot=yPlotY
        elif yPlotY<boarder: # zu grosse Werte
            yPlot=boarder
        elif yPlotY>H-boarder:
            yPlot=H-boarder
        if x0 is boarder: #für ersten Punkt auf y-Achse
            yPlot0=yPlot
        pygame.draw.line(surf,RED,(x0,yPlot0),(x,yPlot),2) #Linie vom vorherigen Punkt zum aktuellen        
        x0=x
        x+= 1 #Schrittweite fix auf kleinstmögliche        
    pygame.display.update()
    
#needed for Servo
servo=3
pos=1500
#needed for getT
spi=spidev.SpiDev()
spi.open(0,1)



(Tp, tp)= (0,0)
(Tq, tq)= (0,0)
(Tr, tr)= (0,0)
(Ts, ts)= (0,0)
(Tt, tt)= (0,0)
(Tu, tu)= (0,0)
(Tv, tv)= (0,0)
(Tw, tw)= (0,0)
(Tx, tx)= (0,0)
(Ty, ty)= (0,0)
(Tz, tz)= (0,0)
(Tmm0,Tmm1,Tmm2,Tmm3,Tmm4,Tmm5,Tmm6,Tmm7,Tmm8)=(0,0,0,0,0,0,0,0,0)
(tmm0,tmm1,tmm2,tmm3,tmm4,tmm5,tmm6,tmm7,tmm8)=(0,0,0,0,0,0,0,0,0)
(Tmm00,Tmm01,Tmm02,Tmm03,Tmm04)=(0,0,0,0,0)
(tmm00,tmm01,tmm02,tmm03,tmm04)=(0,0,0,0,0)

tAbsz=0
tAbs=0
T=0
servoAktive=0
Tm=0

Tfile='T.csv'
tStepM=1
xtStepM=4 # muss grösser 10 sein

while True:
    for i in range(1,xtStepM+1):
        if T>0:
            (Tp,tp)=(Tq,tq)
            (Tq,tq)=(Tr,tr)
            (Tr,tr)=(Ts,ts)
            (Ts,ts)=(Tt,tt)
            (Tt,tt)=(Tu,tu)
            (Tu,tu)=(Tv,tv)
            (Tv,tv)=(Tw,tw)
            (Tw,tw)=(Tx,tx)
            (Tx,tx)=(Ty,ty)
            (Ty,ty)=(Tz,tz)                
            (Tz,tz)=(T,t)
            tAbsz=tAbs
        T=getT(0,1000,3.3,0.0)
        #print("T[°C]=", T)
        tAbs=time.time()
        t=tAbs-tAbsz
        if Tr>1:
            #print("T[°C]=",Tr,Ts,Tt,Tu,Tv,Tw,Tx,Ty,Tz,T)
            prodTt=(Tp*tp+Tq*tq+Tr*tr+Ts*ts+Tt*tt+Tu*tu+Tv*tv+Tw*tw+Tx*tx+Ty*ty+Tz*tz+T*t)
            sumt=(tp+tq+tr+ts+tt+tu+tv+tw+tx+ty+tz+t)
            Tm=prodTt/sumt
            print("Tm[°C]=", Tm)
            tm=tAbs-sumt/2

            Tmm0=Tmm1
            Tmm1=Tmm2
            Tmm2=Tmm3
            Tmm3=Tmm4
            Tmm4=Tmm5
            Tmm5=Tmm6
            Tmm6=Tmm7
            Tmm7=Tmm8
            Tmm8=Tm

            tmm0=tmm1
            tmm1=tmm2
            tmm2=tmm3
            tmm3=tmm4
            tmm4=tmm5
            tmm5=tmm6
            tmm6=tmm7
            tmm7=tmm8
            tmm8=tm

            tmm=tmm5
            
            Tmm=(Tmm0+Tmm1+Tmm2+Tmm3+Tmm4+Tmm5+Tmm6+Tmm7+Tmm8)/9
            print(Tmm, "(",Tmm0, Tmm1, Tmm2, Tmm3, Tmm4 ,Tmm5,Tmm6,Tmm7,Tmm8,")")
            print(tStepM)
        time.sleep(tStepM)

    if Tr>1:
        Tmm00=Tmm01
        Tmm01=Tmm02
        Tmm02=Tmm03
        Tmm03=Tmm04
        Tmm04=Tmm

        Tmmm=(Tmm00+Tmm01+Tmm02+Tmm03+Tmm04)/5

        tmm00=tmm01
        tmm01=tmm02
        tmm02=tmm03
        tmm03=tmm04
        tmm04=tmm

        tmmm=tmm02
    

    if Tr>1:
        tStepPlot=xtStepM*tStepM
        logT(Tmmm,tmmm,Tfile)

        caption='Temperatur-Plot'
        yMin=20
        yMax=80
        tStep=tStepPlot
        B=1600
        H=500
        file=Tfile
        #plotY('Temperatur-Plot',15,30,tStepPlot,1800,400,Tfile)
        th2=threading.Thread(target=plotY)
        th2.start()

        
                             

    
