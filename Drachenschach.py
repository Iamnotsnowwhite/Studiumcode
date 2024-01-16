#Drachenschach
#Der Drache vereignigt die Bewegungsmöglichkeiten einer Drachen und eines Springers im klassischen Sachspiel:
#Springer: das Pferd 
#zusätzlich kann der Drache von pisition (i,j) zu (i',j'), wenn {|i-i'|,|j-j'|} = {1,2}
#{|i-i'|,|j-j'|} = {1,2} diese Bedingung simuliert genau wie ein Spinger funktioniert.

n = 8
Drachen = [0]*n

sp    = {i:False for i in range(n)} # 行
diag1 = {i:False for i in range(2*n-1)} # 捺 2*n-1是对角线的数量
diag2 = {i:False for i in range(-n+1,n)} # 撇 
springer = {(i,j):False for i in range(n) for j in range(n)} # ist genau wie der Schachbrett
#erstellen die Schlüssel in dictionary

def versuche(i):
    global Aufrufe # Variable Aufrufe ist ein rekursive Prozedur 
    Aufrufe+=1
    if i==n:# dann ist es fertig
        bearbeite() # geht zu Funktion bearbeite
    else:
        for j in range(n):
            Drachen[i]=j #在每行格子中写上j作为value
            versuche(i+1) #行加一

def bearbeite():
    global Anzahl
    if keinKonflikt(): #überprüfen ob ein Konflikt existiert 
        Anzahl += 1

def keinKonflikt(): # hier muss was geändert werden
    belegt_spalte = set()
    belegt_diag1 = set()
    belegt_diag2 = set()
    belegt_springerstelle = set()
    for i,j in enumerate(Drachen): # enumerate 同时访问我的key与value
        if not (
                teste_frei(belegt_spalte,j) and
                teste_frei(belegt_diag1,i+j) and
                teste_frei(belegt_diag2,i-j) and
                teste_frei(belegt_springerstelle,((i+j+1),(i-j+2)))):
            return False
    return True

def teste_frei(ss,x):
    if x in ss: return False
    ss.add(x) # es ist eine sotierte Menge
    return True

Aufrufe=Anzahl=0
versuche(0)

print (Aufrufe,"Aufrufe.",Anzahl,"Lösungen")
print (f'{n}**{n}={n**n}. {n}**{n+1}//{n-1}={n**(n+1)//(n-1)}.')

