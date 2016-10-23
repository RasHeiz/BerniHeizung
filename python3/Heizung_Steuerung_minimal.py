#!/usr/bin/python3
#-*- coding:utf-8 -*-
#Datei grafik-csv.py
from __future__ import division, print_function
import csv, pygame, pygame.gfxdraw, time, sys, spidev, threading, pigpio
import Adafruit_CharLCD as LCD
import subprocess, os
import RPi.GPIO as GPIO
from pygame.locals import *
import pdb #for debugging pdb.set_trace()
import logging

GPIO.setmode(GPIO.BCM)

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
    logging.debug('Start Servo to Pos %s ',servoPos)
    #Servo(3,38,1275,0.2)
    #1275 - 100V
    #1330 - 90V
    #1375 - 82V
    #1420 - 74V
    #1480 - 67V
    global servoAktiv
    servoAktiv=1
    
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
    logging.debug('Stop Servo to Pos %s ',servoPos)

def S3():
    logging.debug('S3 überwachung start')
    global S3_status
    #GPIO.setmode(GPIO.BCM)
    S3_pin=16#board36
    GPIO.setup(S3_pin, GPIO.OUT)
    S3=5
    while True:
        if S3_status is 0 and not S3 is 0:
            S3=0
            GPIO.output(S3_pin, GPIO.HIGH)
            logging.debug('S3 aus')
        if S3_status is 1 and not S3 is 1:
            S3=1
            GPIO.output(S3_pin, GPIO.LOW)
            logging.debug('S3 an')
        time.sleep(1)

def S4():
    logging.debug('S4 überwachung start')
    global S4_status
    #GPIO.setmode(GPIO.BCM)
    S4_pin=12#board32
    GPIO.setup(S4_pin, GPIO.OUT)
    S4=5
    while True:
        if S4_status is 0 and not S4 is 0:
            S4=0
            GPIO.output(S4_pin, GPIO.HIGH)
            logging.debug('S4 aus')
        if S4_status is 1 and not S4 is 1:
            S4=1
            GPIO.output(S4_pin, GPIO.LOW)
            logging.debug('S4 an')
        time.sleep(1)    

def tZ2():
    logging.debug('Start timer tZ2')
    global t_Z2
    global tZ2Aktiv
    t_Z2=0             #timer reset
    tZ2Aktiv=1
    time.sleep(1)       #erster Zeitschritt
    while t_Z2 < 30:
        t_Z2=t_Z2+1        
        time.sleep(1)   #weitere Zeitschritte
    tZ2Aktiv=0
    logging.debug('Stop timer tZ2')

def tZ3():
    logging.debug('Start timer tZ3')
    global t_Z3
    global tZ3Aktiv    
    t_Z3=0             #timer reset
    tZ3Aktiv=1
    time.sleep(1)       #erster Zeitschritt
    while t_Z3 < 30:
        t_Z3=t_Z3+1        
        time.sleep(1)   #weitere Zeitschritte
    tZ3Aktiv=0
    logging.debug('Stop timer tZ3')
        
def lastLine(file,Spalte):
    logging.debug('Start lesen der aktuellen Temperatur %s', Spalte)
    with open (file) as f:
        s=f.readlines()[-1]
        x=s.split(',')
    logging.debug('Stop lesen der aktuellen Temperatur %s', Spalte)
    return float(x[Spalte])
    

def S2_taster(pin):
    logging.debug('Start S2_taster aktion')
    global S2_status
    GPIO.setmode(GPIO.BCM)
    if GPIO.input(S2_pin) is 1:
        time.sleep(1)
        if GPIO.input(S2_pin) is 0:
            S2_status=1
            time.sleep(5)
            S2_status=0
    logging.debug('Start S2_taster aktion')

#Parameter ----------------------------------------------------------------------------------

# Raspberry Pi pin configuration:
lcd_rs        = 18  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 23
lcd_d4        = 24
lcd_d5        = 25
lcd_d6        = 8
lcd_d7        = 1
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

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
plotFile='/home/pi/Documents/BerniHeizung/python3/Heizung_T.csv'

#Schrittkette - Startwert
Z=0 # ID des Zustands
ZU=0 #Spannung des entsprechenden Zusatandes

#Abkuehlen? - Startwert
AK=0

#S3 S4 Startwert
S2_status=0
S3_status=0
S4_status=0

#Verzoegerung - verhindern, dass S3 und S4 gleichzeitig zu sind
delay=1

#S2 Pin 
S2_pin=17#board11

#Timer - Startwerte
tZ2Aktiv=0
t_Z2=0
t_Z3=0

#Temperaturen - Startwerte
T_K=0
T_A=0

#Starten der Hintergrundprozesse ------------------------------------------------------------

#logfile
logDate=time.time()
logDate1=time.localtime(logDate)
logDate2=str(time.strftime("%d%m%y_%H%M%S", logDate1))
logfile='/home/pi/Documents/BerniHeizung/python3/log/LOG_HzngStrng_'+logDate2+'.log'
logging.basicConfig(filename=logfile, level=logging.DEBUG)


#S3 S4 Ansteuerung starten
#print ("Insgesamt sind ", threading.active_count(), " Threads aktiv.")
thS3=threading.Thread(target=S3)
thS3.start()
logging.debug('S3 im hintergrund gestartet')
#print ("Insgesamt sind ", threading.active_count(), " Threads aktiv.")
thS4=threading.Thread(target=S4)
thS4.start()
logging.debug('S4 im hintergrund gestartet')
#print ("Insgesamt sind ", threading.active_count(), " Threads aktiv.")

#S2 Ueberwachung aktivieren   
#GPIO.setmode(GPIO.BCM)
GPIO.setup(S2_pin, GPIO.IN)        
GPIO.add_event_detect(S2_pin, GPIO.FALLING, bouncetime=1200)
GPIO.add_event_callback(S2_pin,S2_taster)
logging.debug('S2_taster eventüberwachung gestartet')

# Initialize the LCD using the pins above.
#GPIO.setmode(GPIO.BCM)
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)
logging.debug('LCD ansteuerung initialisiert')

#Hauptprozess -------------------------------------------------------------------------------
lcd.clear()
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
        #if plotAktiv is 0:
        #    thPlot=threading.Thread(target=plotY)
        #    thPlot.start()

        # lesen der temperaturen, wenn Heizung_T existiert
        if os.path.isfile(plotFile) is True:
            T_K=lastLine(plotFile,1)
            T_A=lastLine(plotFile,2)

        lcd.clear()
        logging.debug('LCD clear')
        lcd.home()
        logging.debug('LCD cursor an Pos1')
        TR=subprocess.getoutput("/opt/vc/bin/vcgencmd measure_temp")
        message="K="+str(T_K)[0:3]+chr(223)+"C"+" A="+str(T_A)[0:3]+chr(223)+"C "+"\n"+"R="+TR[5:7]+chr(223)+"C Z"+str(Z)+" "+str(ZU)+"V "
        lcd.message(message)
        logging.debug('LCD show message')
        
        print('T_K= ',T_K,' T_A= ', T_A, ' T_R= ',TR[5:9])

        if ((Z is 2 and T_A<80 and t_Z2 is 30)or(T_A<75 and not Z is 2)) and not Z is 1:
            logging.debug('Z1 start')
            Z=1
            AK=0
            S3_status=0
            S4_status=0
            logging.debug('Z1 ok')

        if Z is 3 and T_A>75 and t_Z3 is 30 and AK is 1:
            logging.debug('Z10 start')
            Z=10
            ZU=90
            AK=0
            S4_status=0
            time.sleep(delay)
            S3_status=1
            Servo(3,20,1325,0.2)
            logging.debug('Z10 ok')
            
    
        #if Z is 1 and S2_status is 1:
        if S2_status is 1:
            logging.debug('Z2 start')
            if tZ2Aktiv is 0:
                thtZ2=threading.Thread(target=tZ2)
                thtZ2.start()
            Z=2
            ZU=230
            S3_status=0
            time.sleep(delay)
            S4_status=1
            logging.debug('Z2 ok')
                        

        if (Z is 2 and T_A>80 and t_Z2<30)or(Z is 4 and T_K<48):
            logging.debug('Z3 start')
            if Z is not 3:
                thtZ3=threading.Thread(target=tZ3)
                thtZ3.start()
            Z=3
            ZU=230
            S3_status=0
            time.sleep(delay)
            S4_status=1
            logging.debug('Z3 ok')
            

        if (Z is 3 and T_K>52)or(Z is 5 and T_K<55):
            logging.debug('Z4 start')
            Z=4
            ZU=100
            AK=1
            S4_status=0
            time.sleep(delay)
            S3_status=1
            Servo(3,20,1270,0.2)
            logging.debug('Z4 ok')

        if (Z is 4 and T_K>59)or(Z is 6 and T_K<75):
            logging.debug('Z5 start')
            Z=5
            ZU=90
            AK=0
            S4_status=0
            time.sleep(delay)
            S3_status=1
            Servo(3,20,1325,0.2)
            logging.debug('Z5 ok')

        if (Z is 5 and T_K>78)or(Z is 7 and T_K<78):
            logging.debug('Z6 start')
            Z=6
            ZU=82
            S4_status=0
            time.sleep(delay)
            S3_status=1
            Servo(3,20,1370,0.2)
            logging.debug('Z6 ok')

        if (Z is 6 and T_K>81)or(Z is 8 and T_K<81):
            logging.debug('Z7 start')
            Z=7
            ZU=74
            S4_status=0
            time.sleep(delay)
            S3_status=1
            Servo(3,20,1415,0.2)
            logging.debug('Z7 ok')

        if (Z is 7 and T_K>84)or(Z is 9 and T_K<84):
            logging.debug('Z8 start')
            S4_status=0
            time.sleep(delay)
            S3_status=1
            if Z is 7:
                Servo(3,20,1470,0.2)
            if Z is 9:
                Servo(3,20,1470,5)
            Z=8
            ZU=67
            logging.debug('Z8 ok')
            
            

        if Z is 8 and T_K>87:
            logging.debug('Z9 start')
            Z=9
            ZU=0
            S3_status=0
            S4_status=0
            logging.debug('Z9 ok')
            
        time.sleep(2)

except KeyboardInterrupt:
        lcd.clear()
        GPIO.cleanup()
        sys.exit()
    

        
                             

    
