import intReader

def TopoSort():
    print ("Topologischen Sortieren.")
    # Einlesen
    input = intReader.readInt() # 只读取整数
    n = next(input) 
    print("n ist", n)

    # Inititalisieren array:
    Knotenliste = [None] + [ Knoten(i) for i in range(1,n+1)] # 我的带有Knoten的列表
    print ("meine Knotenlist ist", Knotenliste)
    
    # Einlesen Kanten
    try:
        while True:
            e = Knotenliste[next(input)] # 入度为0
            f = Knotenliste[next(input)] # 下一个入度为0的元素
            x = Kante(e,f) # 我的kante
            e.Nachfolgerliste.append(x) #这是我的nachfolgerliste
            f.anzVorgänger+=1 # 
    except StopIteration:
        pass #忽略不计，不考虑
        
    # Vorbereiten:
    freieKnoten = [] #空列表
    for i in range(1,n+1): #
        e = Knotenliste[i]
        if e.anzVorgänger==0: #如果入度为0，append e in queue
            freieKnoten.append(e)

    # Sortieren:
    print("");
    for i in range(1,n+1):
        if freieKnoten == []:
            print("Die Eingabe enthält einen Kreis.")
            return
        # Wähle einen Knoten ohne Vorgänger
        x = freieKnoten.pop()
        print(x)
        # Entferne ausgehende Kanten:
        for z in x.Nachfolgerliste:
            z.v.anzVorgänger -= 1 #前驱数量减一
            if z.v.anzVorgänger == 0: #如前驱数量等于0， 放入queue中
                freieKnoten.append(z.v)

#通过使用这些类，您可以创建和操作图的节点和边，进行图算法的实现和分析。这是一种将图形概念转化为可操作的代码的方法。
class Knoten:
    def __init__(self, i):# 这是构造函数（初始化方法）；当创建一个新的 Knoten 对象时，它被调用。接受一个参数 i，它代表节点的名称或标识。
        self.Name = i #这是节点的名称或标识属性，它将被设置为构造函数传递的参数 i。
        self.anzVorgänger = 0 #这是节点的入度（in-degree）属性，表示指向这个节点的边的数量。一开始，这个属性被初始化为0
        self.Nachfolgerliste = [] #这是一个包含所有指向该节点的后继节点（邻接节点）的列表。一开始，这个列表为空
    def __str__(self): # 这是一个特殊方法，通常用于返回对象的字符串表示。在这里，它返回节点的名称，以便在打印节点对象时能够看到其名称。
        return str(self.Name)

class Kante:
    def __init__(self, u, v): #这是构造函数，用于创建一条边。它接受两个参数 u 和 v，这些参数代表边的起点和终点。
        self.u = u #这个属性表示边的起点节点。
        self.v = v #这个属性表示边的终点节点。

TopoSort()        

# print(TopoSort({(6, 4), (3, 5), (4, 2), (3, 4), (5, 4), (1, 2), (1, 6), (3, 6)}))







