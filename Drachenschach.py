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
        if not (sp[j] or diag1[i+j] or diag2[i-j] or springer[(i,j)]):
            sp[j] = diag1[i+j] = diag2[i-j] = springer[(i,j)] = True
            durchsuchen(i+1)
            sp[j] = diag1[i+j] = diag2[i-j] = springer[(i,j)] = False # zwischen Initielisierung
        
Aufrufe=Anzahl=0 #initialisierung es beginnt bei 0 
durchsuchen(0) # wieder beginnt bei 0 

print (Aufrufe,"Aufrufe.",Anzahl,"Lösungen") 
from math import factorial
print (f'{n}!={factorial(n)}.')

print ("==================================")
print ("primitive Methode")

print (Aufrufe,"Aufrufe.",Anzahl,"Lösungen")
print (f'{n}**{n}={n**n}. {n}**{n+1}//{n-1}={n**(n+1)//(n-1)}.')

