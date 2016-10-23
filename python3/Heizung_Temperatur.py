#!/usr/bin/python3
import spidev
import time
import csv
import os
import logging
spi=spidev.SpiDev()
spi.open(0,1)

#logfile
logDate=time.time()
logDate1=time.localtime(logDate)
logDate2=str(time.strftime("%d%m%y_%H%M%S", logDate1))
logfile='/home/pi/Documents/BerniHeizung/python3/log/LOG_HzngT.log'
logging.basicConfig(filename=logfile, level=logging.DEBUG)

la11=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #liste antwort1[1]
la12=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #liste antowrt1[2]
la21=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #liste antwort2[1]
la22=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #liste antwort2[2]
lt=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #liste zeitstempel
tStep=1
mtStep=10
eps=1e-20
file='/home/pi/Documents/BerniHeizung/python3/Heizung_T.csv'
Datum0_0=0

open(logfile, 'w').close() #logfile leeren

while True:

    if os.path.isfile(logfile) is True:
        logSize=os.path.getsize(logfile)
        print(logSize)
        if logSize > 500000:
            open(logfile, 'w').close() #logfile leeren

# Zeitabgleich, damit neues csv. file angelegt wird
    Datum0=time.time()
    print(Datum0)
    ZeitDiff=Datum0-Datum0_0
    print(ZeitDiff)
    print(os.path.isfile(file))
    if ZeitDiff > 60 and os.path.isfile(file) is True: # archiviert .csv-file, wenn bestimmtes alter überschritten ist        
        logging.debug('.csv file wird archiviert')
        Datum0_0=Datum0
        Datum1=time.localtime(Datum0)
        Datum2=str(time.strftime("%d%m%y_%H%M%S", Datum1))
        print(Datum2)        
        print("Datum aktualisiert")
        file_old="/home/pi/Documents/BerniHeizung/python3/T_log/"+Datum2+".csv"
        print(str(file_old))
        os.rename(file, file_old)

# Liste mit n=mtStep Werten füllen
    logging.debug('Start T-werte erfassen')
    for i in range(0,mtStep): 

        #0-128 1-144 2-160 3-176 4-192 5-208 6-224 7-240
        antwort1=spi.xfer([1,128,0])
        antwort2=spi.xfer([1,176,0])
        t=time.time()

        #entfernt ersten wert, fügt neuen wert hinzu
        del la11[0]
        la11.append(antwort1[1])
        del la12[0]
        la12.append(antwort1[2])
        del la21[0]
        la21.append(antwort2[1])
        del la22[0]
        la22.append(antwort2[2])
        del lt[0]
        lt.append(t)        
        time.sleep(tStep)

#sortiert listen nach grösse und entfernt 3 höchsten und 3 niedrigsten werte
    logging.debug('t-liste sortieren und werte löschen')
    La11=list(la11)
    La11.sort()
    del La11[20]
    del La11[19]
    del La11[18]
    del La11[0]
    del La11[0]
    del La11[0]
    
    La12=list(la12)
    La12.sort()
    del La12[20]
    del La12[19]
    del La12[18]
    del La12[0]
    del La12[0]
    del La12[0]
    
    La21=list(la21)
    La21.sort()
    del La21[20]
    del La21[19]
    del La21[18]
    del La21[0]
    del La21[0]
    del La21[0]
    
    La22=list(la22)
    La22.sort()
    del La22[20]
    del La22[19]
    del La22[18]
    del La22[0]
    del La22[0]
    del La22[0]
    
#mittelwert der reduzierten listen
    logging.debug('Mittelwerte berechnen')
    La11m=sum(La11)/len(La11)    
    La12m=sum(La12)/len(La12)
    
    La21m=sum(La21)/len(La21)    
    La22m=sum(La22)/len(La22)        
    
    if 0<= antwort1[1]<=3:
        logging.debug('Mittelwert 1 in T umrechnen')
        vMax1=3.29406
        vMin1=0.00322
        vRange1=vMax1-vMin1
        rAdd1=1000

        wert1=((La11m*256)+La12m)*0.00322+eps
        print(wert1," V",)

        R1=(vRange1-wert1)/(wert1)*rAdd1            
        T1=round(1.1072597754889e-5*R1*R1+0.2331563968*R1-244.1819649032,2)
        print(T1," °C",)
            
    if 0<= antwort2[1]<=3:
        logging.debug('Mittelwert 2 in T umrechnen')
        vMax2=3.29406
        vMin2=0.00322
        vRange2=vMax2-vMin2
        rAdd2=1000

        wert2=((La21m*256)+La22m)*0.00322+eps
        print(wert2," V",)
        
        R2=(vRange2-wert2)/(wert2)*rAdd2
        T2=round(1.1072597754889e-5*R2*R2+0.2331563968*R2-244.1819649032,2)
        round(T2,2)
        print(T2," °C",)

    logging.debug('Zeitpunkt der mittleren temperatur auslesen')
    timeLoc=time.localtime(lt[11])
    date=time.strftime("%d/%m/%y %H:%M:%S", timeLoc)
    print(date)

#Schreiben der temperaturen und zeit in liste, falls sinnvolle werte vorhanden
    
    if la21[0]>0 or la11[0]>0:
        logging.debug('Werte sind vorhanden --> schreiben in .csv')
        with open(file, 'a') as out:
            cw=csv.writer(out, delimiter=',', lineterminator='\n',quotechar='"')
            cw.writerow([lt[11],T1,T2])
        logging.debug('Werte in .csv geschrieben')
            
            
        
