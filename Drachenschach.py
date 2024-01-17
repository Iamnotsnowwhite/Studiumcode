#Drachenschach
#Der Drache vereignigt die Bewegungsmöglichkeiten einer Drachen und eines Springers im klassischen Sachspiel:
#Springer: das Pferd 
#zusätzlich kann der Drache von pisition (i,j) zu (i',j'), wenn {|i-i'|,|j-j'|} = {1,2}
#{|i-i'|,|j-j'|} = {1,2} diese Bedingung simuliert genau wie ein Spinger funktioniert.

n = 8
dame = [0]*n

sp    = {i:False for i in range(n)} # 行
diag1 = {i:False for i in range(2*n-1)} # 捺 2*n-1是对角线的数量
diag2 = {i:False for i in range(-n+1,n)} # 撇 
springer = {(i,j):False for i in range(n) for j in range(n)} # ist genau wie der Schachbrett
#erstellen die Schlüssel in dictionary

def durchsuchen(i):
    global Aufrufe,Anzahl #globale Variable
    Aufrufe+=1 
    if i==n:
        Anzahl += 1
        print (Anzahl, dame)
        return
    for j in range(n):
        dame[i]=j
        if not (sp[j] or diag1[i+j] or diag2[i-j] or checkspringer(i-1,j-2) or checkspringer(i-2,j-1) or checkspringer(i-1,j+2) or checkspringer(i-2,j+1) or checkspringer(i+1,j+2) or checkspringer(i+2,j+1) or checkspringer(i+2,j-1) or checkspringer(i+1,j-2) or checkspringer(i,j-2)):
            sp[j] = diag1[i+j] = diag2[i-j] = springer[checkspringer2(i-1,j-2)] = springer[checkspringer(i-2,j-1)] = springer[checkspringer(i-1,j+2)] = springer[checkspringer(i-2,j+1)] = springer[checkspringer(i+1,j+2)] = springer[checkspringer(i+2,j+1)] = springer[checkspringer(i+2,j-1)] = springer[checkspringer(i+1,j-2)] = True
            durchsuchen(i+1)
            sp[j] = diag1[i+j] = diag2[i-j] = springer[checkspringer2(i-1,j-2)] = springer[checkspringer(i-2,j-1)] = springer[checkspringer(i-1,j+2)] = springer[checkspringer(i-2,j+1)] = springer[checkspringer(i+1,j+2)] = springer[checkspringer(i+2,j+1)] = springer[checkspringer(i+2,j-1)] = springer[checkspringer(i+1,j-2)] = False # zwischen Initielisierung
        
def checkspringer(i,j):
    if i < 0 or i > 7 or j < 0 or j > 7 :
        return False
    else:
        return springer[(i,j)]
    
def checkspringer2(i,j):
    if i < 0 or i > 7 or j < 0 or j > 7 :
        return None
    else:
        return (i,j)

Aufrufe=Anzahl=0 #initialisierung es beginnt bei 0 
durchsuchen(0) # wieder beginnt bei 0 

print (Aufrufe,"Aufrufe.",Anzahl,"Lösungen") 
from math import factorial
print (f'{n}!={factorial(n)}.')

print ("==================================")
print ("primitive Methode")

print (Aufrufe,"Aufrufe.",Anzahl,"Lösungen")
print (f'{n}**{n}={n**n}. {n}**{n+1}//{n-1}={n**(n+1)//(n-1)}.')

"""
def kleinstes(n):
    while True:
        durchsuchen(0)   # Führe den Algorithmus aus
        if Anzahl == 0:  # Wenn keine Lösung gefunden wurde
            break
        n += 1

kleinstesbrett = kleinstes(2)
print(f"Kleinste Schachbrettgröße für n Drachen: {kleinstesbrett}")
"""
