#/bin/bash

#Heizungssteuerung
/usr/bin/python3 /home/pi/Documents/BerniHeizung/python3/Heizung_Temperatur.py &
/usr/bin/python3 /home/pi/Documents/BerniHeizung/python3/Heizung_Steuerung_minimal.py &
