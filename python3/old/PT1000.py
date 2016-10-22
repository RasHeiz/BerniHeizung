#!/usr/bin/python3
import spidev
import time
import csv
spi=spidev.SpiDev()
spi.open(0,1)

wert=1

la11=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #Liste antwort1[1]
la12=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #Liste antowrt1[2]
la21=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #Liste antwort2[1]
la22=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #Liste antowrt2[2]
lt=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #Liste zeitstempel
tStep=1
mtStep=10
eps=1e-20
file='T.csv'

while True:

    for i in range(0,mtStep): 

        #0-128 1-144 2-160 3-176 4-192 5-208 6-224 7-240
        antwort1=spi.xfer([1,128,0])
        antwort2=spi.xfer([1,240,0])
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


    #sortiert listen der nach grösse und entfernt 3 höchsten und 3 niedrigsten Werte
    print(la11)
    La11=list(la11)
    La11.sort()
    del La11[20]
    del La11[19]
    del La11[18]
    del La11[0]
    del La11[0]
    del La11[0]
    print(La11)

    print(la12)
    La12=list(la12)
    La12.sort()
    del La12[20]
    del La12[19]
    del La12[18]
    del La12[0]
    del La12[0]
    del La12[0]
    print(La12)

    print(la21)
    La21=list(la21)
    La21.sort()
    del La21[20]
    del La21[19]
    del La21[18]
    del La21[0]
    del La21[0]
    del La21[0]
    print(La21)

    print(la22)
    La22=list(la22)
    La22.sort()
    del La22[20]
    del La22[19]
    del La22[18]
    del La22[0]
    del La22[0]
    del La22[0]
    print(La22)

    #Mittelwert der reduzierten listen
    La11m=sum(La11)/len(La11)
    print(La11m)
    La12m=sum(La12)/len(La12)
    print(La12m)
    La21m=sum(La21)/len(La21)
    print(La21m)
    La22m=sum(La22)/len(La22)
    print(La22m)

        
    
    if 0<= antwort1[1]<=3:
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

    timeLoc=time.localtime(lt[11])
    date=time.strftime("%d/%m/%y %H:%M:%S", timeLoc)
    print(date)

    print(la22)
    print(la12)
    if la21[0]>0 or la11[0]>0:
        with open(file, 'a') as out:
            cw=csv.writer(out, delimiter=',', lineterminator='\n',quotechar='"')
            cw.writerow([lt[11],T1,T2])
            
            
        
