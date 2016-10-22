#!/usr/bin/python3
#-*- coding:utf-8 -*-
#Datei grafik-csv.py
from __future__ import division, print_function
import csv, pygame, pygame.gfxdraw, time, sys, spidev, threading, pigpio
import RPi.GPIO as GPIO
from pygame.locals import *
import pdb #for debugging pdb.set_trace()

#Funktionen ---------------------------------------------------------------------------------

def plotY():
    global plotCaption
    global plotYMin
    global plotYMax
    global plotB
    global plotH
    global plotFile
    global plotAktiv

    plotAktiv=1
    
    #Konstanten
    WHITE=(255,255,255)
    RED=(255,0,0)
    GREEN=(0,150,0)
    BLUE=(0,0,255)
    GREY=(200,200,200)
    boarder=50
    Steps=plotB-2*boarder+1 # für kleinste Schrittweite von 1px (muss Integer ergeben)
    
    #DatenBereich
    data=[]
    with open(plotFile)as f:
        cr=csv.reader(f)
        for line in cr:
            data.append(line)
            data=data[-Steps:]
    #DiagrammFlaeche
    pygame.init()
    surf=pygame.display.set_mode((plotB,plotH),0,32)
    surf.fill(WHITE)
    pygame.display.set_caption(plotCaption)
    myfont=pygame.font.SysFont('FreeSerif.ttf',16)

    #yAchse
    pygame.draw.line(surf,BLUE,(boarder,plotH-boarder),(boarder,boarder),2)
    pygame.draw.line(surf,BLUE,(plotB-boarder,plotH-boarder),(plotB-boarder,boarder),2)
    mulySkala1=0
    mulySkala=0
    stepySkala=15
    
    while mulySkala<stepySkala:
        mulySkala=mulySkala1
        ySkala=(plotYMax-plotYMin)/stepySkala*mulySkala+plotYMin
        yPos=int(plotH-(ySkala-plotYMin)/(plotYMax-plotYMin)*(plotH-2*boarder)-boarder-5)
        ytxt=u'%.1f°C' % ySkala
        textsurf=myfont.render(ytxt.encode('latin-1'),1,(0,0,0))
        surf.blit(textsurf,(5,yPos))
        pygame.draw.line(surf,GREY,(boarder,yPos+5),(plotB-boarder,yPos+5),1)
        mulySkala1=mulySkala+1

    #xAchse-Linien und Positionen der Skalenwerte
    pygame.draw.line(surf,BLUE,(boarder,plotH-boarder),(plotB-boarder,plotH-boarder),2)
    mulxSkala1=0
    mulxSkala=0
    stepxSkala=10 #anzahl skalenabschnitte
    (xA10,xA9,xA8,xA7,xA6,xA5,xA4,xA3,xA2,xA1,xA0)=(0,0,0,0,0,0,0,0,0,0,0)
    while mulxSkala<stepxSkala:
        mulxSkala=mulxSkala1
        xSkala=(Steps-1)/stepxSkala*mulxSkala # Punkte bis zum Skalenwert
        #xSkala=1
        xPos=int(plotB-(xSkala-0)/(Steps-0)*(plotB-2*boarder)-boarder)
        (xA10,xA9,xA8,xA7,xA6,xA5,xA4,xA3,xA2,xA1,xA0)=(xPos,xA10,xA9,xA8,xA7,xA6,xA5,xA4,xA3,xA2,xA1) # Speichern der Positionen xA0 bis xA10
        pygame.draw.line(surf, BLUE,(xPos, plotH-boarder-5),(xPos, plotH-boarder+10),2)
        mulxSkala1=mulxSkala+1

    # Punkte
    x=boarder #xPos erster Punkt
    x0=boarder #xPos des vorherigen Punktes
    xmul=0
    xmul1=0
    for messpunkt in data:
        if x0>boarder:  #speichern des vorgängers
            yPlot10=yPlot1
            yPlot20=yPlot2
        yValue1=float(messpunkt[1])
        yValue2=float(messpunkt[2])
        
        #Auslesen des Zeitstempels der y-Werte an den Positionen der x-Skala
        if x==xA10 or x==xA9 or x==xA8 or x==xA7 or x==xA6 or x==xA5 or x==xA4 or x==xA3 or x==xA2 or x==xA1 or x==xA0:
            xValue=float(messpunkt[0])
            timeLoc=time.localtime(xValue)
            Date=time.strftime("%d/%m/%y %H:%M:%S", timeLoc)            
            textsurf=myfont.render(Date.encode('latin-1'),1,(0,0,0))
            surf.blit(textsurf,(x-boarder+8,plotH-boarder+12))

        yPlotY1=int(plotH-(yValue1-plotYMin)/(plotYMax-plotYMin)*(plotH-2*boarder)-boarder)
        yPlotY2=int(plotH-(yValue2-plotYMin)/(plotYMax-plotYMin)*(plotH-2*boarder)-boarder)
        
        if yPlotY1>boarder and yPlotY1<plotH-boarder: 
            yPlot1=yPlotY1
        elif yPlotY1<boarder: # zu grosser Wert
            yPlot1=boarder
        elif yPlotY1>plotH-boarder: # zu kleiner Wert
            yPlot1=plotH-boarder
        if x0 is boarder: #für ersten Punkt auf y-Achse
            yPlot10=yPlot1

        if yPlotY2>boarder and yPlotY2<plotH-boarder: 
            yPlot2=yPlotY2
        elif yPlotY2<boarder: # zu grosser Wert
            yPlot2=boarder
        elif yPlotY2>plotH-boarder: # zu kleiner Wert
            yPlot2=plotH-boarder
        if x0 is boarder: #für ersten Punkt auf y-Achse
            yPlot20=yPlot2
            
        pygame.draw.line(surf,RED,(x0,yPlot10),(x,yPlot1),2) #Linie vom vorherigen Punkt zum aktuellen
        pygame.draw.line(surf,GREEN,(x0,yPlot20),(x,yPlot2),2) #Linie vom vorherigen Punkt zum aktuellen
        x0=x
        x+= 1 #Schrittweite fix auf kleinstmögliche        
    pygame.display.update()
    plotAktiv=0

def Servo(servoPin, relaisPin, servoPos, servoSleep): #650-2450
    #Servo(3,38,1275,0.2)
    #1275 - 100V
    #1330 - 90V
    #1375 - 82V
    #1420 - 74V
    #1480 - 67V
    global servoAktiv
    servoAktiv=1
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(relaisPin, GPIO.OUT)
    pi=pigpio.pi()
    pi.set_mode(servoPin, pigpio.OUTPUT)
    
    GPIO.output(relaisPin, GPIO.LOW)
    time.sleep(0.5)        
    pi.set_servo_pulsewidth(servoPin, 1100)
    time.sleep(servoSleep)
    pi.set_servo_pulsewidth(servoPin, servoPos)
    time.sleep(0.5)
    GPIO.output(relaisPin, GPIO.HIGH)
    pi.stop()
    servoAktiv=0

def S3():
    global S3_status
    GPIO.setmode(GPIO.BOARD)
    S3_pin=32
    GPIO.setup(S3_pin, GPIO.OUT)
    S3=5
    while True:
        if S3_status is 0 and not S3 is 0:
            S3=0
            GPIO.output(S3_pin, GPIO.HIGH)
        if S3_status is 1 and not S3 is 1:
            S3=1
            GPIO.output(S3_pin, GPIO.LOW)
        time.sleep(1)

def S4():
    global S4_status
    GPIO.setmode(GPIO.BOARD)
    S4_pin=36
    GPIO.setup(S4_pin, GPIO.OUT)
    S4=5
    while True:
        if S4_status is 0 and not S4 is 0:
            S4=0
            GPIO.output(S4_pin, GPIO.HIGH)
        if S4_status is 1 and not S4 is 1:
            S4=1
            GPIO.output(S4_pin, GPIO.LOW)
        time.sleep(1)    

def tZ2():
    global t_Z2
    global tZ2Aktiv
    t_Z2=0             #timer reset
    tZ2Aktiv=1
    time.sleep(1)       #erster Zeitschritt
    while t_Z2 < 30:
        t_Z2=t_Z2+1        
        time.sleep(1)   #weitere Zeitschritte
    tZ2Aktiv=0

def tZ3():
    global t_Z3
    global tZ3Aktiv    
    t_Z3=0             #timer reset
    tZ3Aktiv=1
    time.sleep(1)       #erster Zeitschritt
    while t_Z3 < 30:
        t_Z3=t_Z3+1        
        time.sleep(1)   #weitere Zeitschritte
    tZ3Aktiv=0
        
def lastLine(file,Spalte):
    with open (file) as f:
        s=f.readlines()[-1]
        x=s.split(',')
        return float(x[Spalte])

def S2_taster(pin):
    global S2_status
    if GPIO.input(S2_pin) is 1:
        time.sleep(1)
        if GPIO.input(S2_pin) is 0:
            S2_status=1
            time.sleep(5)
            S2_status=0

#Parameter ----------------------------------------------------------------------------------

#Servo - Pin&Startwerte (globale Variablen)
servoAktiv=0
#servoPin=3
#servoPos=1500
#relaisPin=38

#Plot Setup (globale Variablen)
plotAktiv=0
plotCaption='Temperatur-Plot'
plotYMin=15
plotYMax=120
plotB=1000
plotH=300
plotFile='Heizung_T.csv'

#Schrittkette - Startwert
Z=1 # ID des Zustands

#Abkuehlen? - Startwert
AK=0

#S3 S4 Startwert
S2_status=0
S3_status=0
S4_status=0

#Verzoegerung - verhindern, dass S3 und S4 gleichzeitig zu sind
delay=1

#S2 Pin 
S2_pin=11

#Timer - Startwerte
tZ2Aktiv=0
t_Z2=0
t_Z3=0

#Starten der Hintergrundprozesse ------------------------------------------------------------

#S3 S4 Ansteuerung starten
#print ("Insgesamt sind ", threading.active_count(), " Threads aktiv.")
thS3=threading.Thread(target=S3)
thS3.start()
#print ("Insgesamt sind ", threading.active_count(), " Threads aktiv.")
thS4=threading.Thread(target=S4)
thS4.start()
#print ("Insgesamt sind ", threading.active_count(), " Threads aktiv.")

#S2 Ueberwachung aktivieren   
GPIO.setmode(GPIO.BOARD)
GPIO.setup(S2_pin, GPIO.IN)        
GPIO.add_event_detect(S2_pin, GPIO.FALLING, bouncetime=1200)
GPIO.add_event_callback(S2_pin,S2_taster)

#Hauptprozess -------------------------------------------------------------------------------

try:
    while True:
        
        #print('thS3 ',thS3.isAlive())
        #print('thS4 ',thS4.isAlive())

        print('Zustand ',Z)
        
        if S2_status is 1:
            print('S2_status ', S2_status)
        if Z is 2:
            print('Timer30 ',t_Z2)
        if Z is 3:
            print('Timer30 ',t_Z3)       

        #Diagramm aktualisieren
        if plotAktiv is 0:
            thPlot=threading.Thread(target=plotY)
            thPlot.start()

        T_K=lastLine(plotFile,1)
        T_A=lastLine(plotFile,2)
        
        print('T_K= ',T_K,' T_A= ', T_A)

        if (Z is 2 and T_A<80 and t_Z2 is 30)or(T_A<75 and not Z is 2):
            Z=1
            AK=0
            S3_status=0
            S4_status=0

        if Z is 3 and T_A>75 and t_Z3 is 30 and AK is 1:
            Z=10
            AK=0
            S4_status=0
            time.sleep(delay)
            S3_status=1
            Servo(3,38,1325,0.2)
            
    
        #if Z is 1 and S2_status is 1:
        if S2_status is 1:
            if tZ2Aktiv is 0:
                thtZ2=threading.Thread(target=tZ2)
                thtZ2.start()
            Z=2
            S3_status=0
            time.sleep(delay)
            S4_status=1
                        

        if (Z is 2 and T_A>80 and t_Z2<30)or(Z is 4 and T_K<48):
            if Z is not 3:
                thtZ3=threading.Thread(target=tZ3)
                thtZ3.start()
            Z=3            
            S3_status=0
            time.sleep(delay)
            S4_status=1
            

        if (Z is 3 and T_K>52)or(Z is 5 and T_K<55):
            Z=4
            AK=1
            S4_status=0
            time.sleep(delay)
            S3_status=1
            Servo(3,38,1270,0.2)

        if (Z is 4 and T_K>59)or(Z is 6 and T_K<75):
            Z=5
            AK=0
            S4_status=0
            time.sleep(delay)
            S3_status=1
            Servo(3,38,1325,0.2)

        if (Z is 5 and T_K>78)or(Z is 7 and T_K<78):
            Z=6
            S4_status=0
            time.sleep(delay)
            S3_status=1
            Servo(3,38,1370,0.2)

        if (Z is 6 and T_K>81)or(Z is 8 and T_K<81):
            Z=7
            S4_status=0
            time.sleep(delay)
            S3_status=1
            Servo(3,38,1415,0.2)

        if (Z is 7 and T_K>84)or(Z is 9 and T_K<84):
            S4_status=0
            time.sleep(delay)
            S3_status=1
            if Z is 7:
                Servo(3,38,1470,0.2)
            if Z is 9:
                Servo(3,38,1470,5)
            Z=8
            
            

        if Z is 8 and T_K>87:
            Z=9
            S3_status=0
            S4_status=0
            
        time.sleep(2)

except KeyboardInterrupt:
       GPIO.cleanup()
       sys.exit()
    

        
                             

    
