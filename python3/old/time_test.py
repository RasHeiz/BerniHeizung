from time import *


# 11 Zeitangaben jeweils mit Pause
for i in range(11): 
  wert = time()

  if i == 0:
    startwert = wert
  elif i == 10:
    endwert = wert

  print (i, wert)
  sleep(1.5)

# Durchschnittlicher Abstand
diff = (endwert - startwert) / 10
print ("Abstand: ", diff)
