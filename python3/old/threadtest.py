import threading, time
 
 
zaehler1=0
zaehler2=0
 
def Thread1():
    global zaehler1
    print ("Starte Unterprogramm Thread1." )
    while 1:
        time.sleep(20)
        zaehler1=zaehler1+1
        print  ("Thread 1: zaehler=", zaehler1 )
        print ("Thread1")
 
def Thread2():
    global zaehler1, zaehler2
    print ("Starte Unterprogramm Thread2." )
    while 1:
        time.sleep(10)
        zaehler2=zaehler2+1
        print ( "Thread 2: zaehler=", zaehler2 )
        print ( "Differenz der beiden Zaehler=",zaehler2-zaehler1 )
        print ( "Thread2" )
 
th1=threading.Thread(target=Thread1)
th2=threading.Thread(target=Thread2)
 
print( "Th1 ist aktiv: ", th1.isAlive())
print ("Th2 ist aktiv: ", th2.isAlive())
print ("Insgesamt sind ", threading.active_count(), " Threads aktiv.")
 
th1.start()
 
print ("Th1 ist aktiv: ", th1.isAlive())
print( "Th2 ist aktiv: ", th2.isAlive())
print ("Insgesamt sind ", threading.active_count(), " Threads aktiv.")
 
th2.start()
 
print ('Th1 ist aktiv: ', th1.isAlive())
print ("Th2 ist aktiv: ", th2.isAlive())
print ("Insgesamt sind ", threading.active_count(), " Threads aktiv.")
