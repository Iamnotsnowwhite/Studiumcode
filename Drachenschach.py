#Drachenschach
#Der Drache vereignigt die Bewegungsmöglichkeiten einer Drachen und eines Springers im klassischen Sachspiel:
#Springer: das Pferd 
#zusätzlich kann der Drache von pisition (i,j) zu (i',j'), wenn {|i-i'|,|j-j'|} = {1,2}
#{|i-i'|,|j-j'|} = {1,2} diese Bediegung simuliert genau wie ein Springer funktioniert.

import sys
n = 8
Drachen = [0]*n


# move =[(i + 2, j + 1), (i + 2, j - 1), (i - 2, j + 1), (i - 2, j - 1),(i + 1, j + 2), (i + 1, j - 2), (i - 1, j + 2), (i - 1, j - 2)]
sp    = {i:False for i in range(n)} # 行
diag1 = {i:False for i in range(2*n-1)} # 捺 2*n-1是对角线的数量
diag2 = {i:False for i in range(-n+1,n)} # 撇 
springer = {(i,j):False for i in range(n) for j in range(n)} # ist genau wie der Schachbrett
#erstellen die Schlüssel in dictionary

def springer_bewegung(i, j):

    moves = [(i + 2, j + 1), (i + 2, j - 1), (i - 2, j + 1), (i - 2, j - 1),
    (i + 1, j + 2), (i + 1, j - 2), (i - 1, j + 2), (i - 1, j - 2)]

    return [(x, y) for x, y in moves if 0 <= x < n and 0 <= y < n] # es kann nur im Bereich 0 bis n sein
    # list comprehention

def durchsuchen(i):
    global Aufrufe,Anzahl #globale Variable
    Aufrufe +=1 
    if i==n:
        Anzahl += 1
        print(Anzahl,Drachen) # hier wird nicht zu getroffen 
        return 
    for j in range(n):
        if not(sp[j] or diag1[i+j] or diag2[i-j]): # 检查骑士的移动
            moves = springer_bewegung(i, j)
            if all(not(0 <= x < n and 0 <= y < n and sp[y]) for x, y in moves):
                sp[j] = diag1[i+j] = diag2[i-j] = True
                moves = [True for _ in moves]
                durchsuchen(i + 1)
                # if keinKonflikt(i) == False: # wenn false dann gibt es Konflikt
                #     i += 1 
                #     durchsuchen(i)
                sp[j] = diag1[i+j] = diag2[i-j] = False 
                moves = [False for _ in moves]

def keinKonflikt(i):
    belegt_spalte = set()
    belegt_diag1 = set()
    belegt_diag2 = set()
    belegt_springer = set()
    for i,j in enumerate(Drachen):
        if not (
                teste_frei(belegt_spalte,j) and
                teste_frei(belegt_diag1,i+j) and
                teste_frei(belegt_diag2,i-j) and
                teste_frei(belegt_springer, (i-2,j-1))and
                teste_frei(belegt_springer, (i-1,j-2)) and
                teste_frei(belegt_springer, (i+1,j-2))and
                teste_frei(belegt_springer, (i-2,j+1)) and
                teste_frei(belegt_springer, (i-2,j+2)) and
                teste_frei(belegt_springer, (i+1,j+2)) and
                teste_frei(belegt_springer, (i+2,j+1))):
            return False
    return True

def teste_frei(ss,x):
    if x in ss: return False
    ss.add(x) # es ist eine sotierte Menge
    return True

Aufrufe=Anzahl=0 #initialisierung es beginnt bei 0 
durchsuchen(0) # wieder beginnt bei 0 
# sys.setrecursionlimit(3000)

print (Aufrufe,"Aufrufe.",Anzahl,"Lösungen") 
# from math import factorial
# print (f'{n}!={factorial(n)}.')

# print ("==================================")
# print ("primitive Methode")
