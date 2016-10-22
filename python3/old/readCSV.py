import csv
def lastLine(file,Spalte):
    with open (file) as f:
        s=f.readlines()[-1]
        x=s.split(',')
        return float(x[Spalte])

T_K=lastLine('Heizung_T.csv',0)
print(T_K)        
F=T_K+1
print(F)
