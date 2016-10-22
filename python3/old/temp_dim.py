#!/usr/bin/python3
from tkinter import *
import time
import csv

file='Heizung_T.csv'

# Reaktion auf Mausklick im Fenster
def T_K_change(value):
  T_A=float(value)
  T_K=T_A-50
  t=time.time()
  print(t,"T_K=",T_K, "T_A=",T_A)
  with open(file, 'a') as out:
            cw=csv.writer(out, delimiter=',', lineterminator='\n',quotechar='"')
            cw.writerow([t,T_K,T_A])
  

#def T_A_change(value):
  #T_A=value
  #print("T_A=",T_A)
  
# Programmende durch Windows-Close-Button
def win_close():
  
  mywin.quit()

# Programmende durch Strg+C im Terminal
def strg_c(signal, frame):
  win_close()

# regelmäßiger Aufruf, damit Strg+C funktioniert
def do_nothing():
  mywin.after(200, do_nothing)



# Benutzeroberfläche
mywin = Tk()
mywin.wm_title('LED-Helligkeit')
lbl1 = Label(mywin, text='T_K')
T_K = Scale(mywin, from_=0, to=200, orient=HORIZONTAL, command=T_K_change)
T_K.set(50)
lbl1.grid(column=0, row=0, padx=5, pady=5)
T_K.grid(column=0, row=1, padx=5, pady=5)

#lbl2 = Label(mywin, text='T_A')
#T_A = Scale(mywin, from_=0, to=100, orient=HORIZONTAL, command=T_A_change)
#T_A.set(50)
#lbl2.grid(column=0, row=2, padx=5, pady=5)
#T_A.grid(column=0, row=3, padx=5, pady=5)



# Ereignisse
mywin.protocol("WM_DELETE_WINDOW", win_close) # ordentliches Programmende, wenn Fenster geschlossen wird
mywin.after(200, do_nothing)         # damit Strg+C funktioniert
mywin.mainloop()




