import sqlite3.dbapi2 as sqlite
import sys
import numpy as np
import math
import random
import networkx as nx
import folium

sys.stdout.reconfigure(encoding='utf-8')

conn = sqlite.connect('adresy.sqlite')
curs = conn.cursor()
"""
curs.execute("create table obce(id_obce integer primary key, meno_obce text)")
curs.execute("create table ulice(id_ulice integer primary key, meno_ulice text, id_obce integer, foreign key(id_obce) references obce(id_obce))")
curs.execute("create table cisla(id_domu integer primary key, cislo_domu text, lat float, long float, id_ulice integer, foreign key(id_ulice) references ulice(id_ulice))")
"""
"""
with open('Semestralka/obce.csv', encoding='utf-8') as f:
    for riadok in f:
        oid, omeno = riadok.strip().split(',')
        try:
            curs.execute("insert into obce(id_obce, meno_obce) values(?,?)", (int(oid), omeno))
        except sqlite.IntegrityError:
            pass
conn.commit()

with open('Semestralka/ulice.csv', encoding='utf-8') as f:
    for riadok in f:
        uid, omeno, oid = riadok[:-1].split(',')
        try:
            curs.execute("insert into ulice(id_ulice, meno_ulice, id_obce) values(?,?,?)", (int(uid), omeno, int(oid)))
        except sqlite.IntegrityError:
            pass
conn.commit()

with open('Semestralka/cisla.csv', encoding='utf-8') as f:
    for riadok in f:
        did, cdomu, la, lo, uid = riadok[:-1].split(',')
        try:
            curs.execute("insert into cisla(id_domu, cislo_domu ,lat, long, id_ulice) values(?,?,?,?,?)", (int(did), cdomu, float(la), float(lo), int(uid)))
        except sqlite.IntegrityError:
            pass
conn.commit()
"""
curs.execute("select distinct meno_obce, meno_ulice, cislo_domu, lat, long from obce join ulice on ulice.id_obce = obce.id_obce join cisla on cisla.id_ulice = ulice.id_ulice where meno_obce = 'Čadca'")
data = np.array(curs.fetchall())

def sphericalDistance(d1, l1, d2, l2):
    '''Funkcia vracia vzdialenosť medzi dvoma bodmi na zemskom povrchu v km'''
    R = 6378
    phi1 = math.radians(d1)
    phi2 = math.radians(d2)
    lambda1 = math.radians(l1)
    lambda2 = math.radians(l2)
    deltaPhi = phi2 - phi1
    deltaLambda = lambda2 - lambda1
    a = math.sin(deltaPhi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(deltaLambda/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

def generatePoints(count):
    list = [0]
    for i in range(0, count):
        index = random.randint(0, len(data))
        if index not in list:
            list.append(index)
    return list

def loadEdgesEnhanced(graph, vertices):
    for i in range(0, len(vertices)):
        for j in range(0, len(vertices)):
            if(i != j):
                d1 = float(data[vertices[i]][3])
                l1 = float(data[vertices[i]][4])
                d2 = float(data[vertices[j]][3])
                l2 = float(data[vertices[j]][4])
                graph.add_edge(vertices[i], vertices[j], weight=sphericalDistance(d1, l1, d2, l2))

def SpanningTreeMatching(array):
    G = nx.Graph()
    vertices = array
    edges = loadEdgesEnhanced(G, array)

    minimumSpanningTree = nx.minimum_spanning_tree(G)#najdi najlacnejšiu kostru

    verticesOddDegree = [v for v, d in minimumSpanningTree.degree() if d % 2 == 1]#najdi vrcholy neparneho stupna

    #zostroj uplny graf z vrcholov neparneho stupna
    completeGraph = nx.Graph()
    for u, v, d in G.edges(data=True):
        if(u in verticesOddDegree and v in verticesOddDegree):
            completeGraph.add_edge(u, v, weight=G[u][v]['weight'])
    
    matching = nx.algorithms.matching.min_weight_matching(completeGraph, weight="weight") #najdi parenie s min cenou


    #hrany parenia pridaj k najlacnejsej kostre a mas multigraf s vrcholmi parneho stupna
    multiGraph = nx.MultiGraph()
    multiGraph.add_edges_from(minimumSpanningTree.edges(data=True))
    for u, v in matching:
        multiGraph.add_edge(u, v, weight=G[u][v]["weight"])

    T = list(nx.eulerian_circuit(multiGraph))#najdi uzavrety eulerovsky tah
        
    #redukuj eulerovsky tah
    result = [T[0][0]]
    summation = 0
    for u, v in T:
        if(v not in result):
            result.append(v)
            summation += multiGraph[u][v][0]["weight"]

    result.append(T[0][0])
    try:
        summation += G[result[len(result) - 1]][result[len(result) - 2]]["weight"]
    except:
        summation += G[result[len(result) - 2]][result[len(result) - 1]]["weight"]

    print("Cesta podla algoritmu kostry a parenia je:")
    print(result)
    print("cena: " + str(summation))
    return result

def Greedy(array):
    graphGreedy = nx.Graph()
    vertices = array
    loadEdgesEnhanced(graphGreedy, array)
    hamilton = []
    firstNode = array[0]
    hamilton.append(firstNode)
    while(len(hamilton) < len(vertices)):
        smallestEdge = None
        cost = float('inf')
        #do cyklu vloz najlacnejsiu hranu incidentnu s aktualnym vrcholom a koncovy vrchol nie je v cykle
        for u, v, d in graphGreedy.edges(data=True):
            if(u == firstNode):
                if(v not in hamilton):
                    if(cost > float(d["weight"])):
                        smallestEdge = (u, v, float(d["weight"]))
                        cost = float(d["weight"])
            if(v == firstNode):
                if(u not in hamilton):
                    if(cost > float(d["weight"])):
                        smallestEdge = (v, u, float(d["weight"]))
                        cost = float(d["weight"])
                        
        if smallestEdge == None:
            break
        hamilton.append(smallestEdge[1])
        firstNode = smallestEdge[1]
    

    hamilton.append(array[0])
    summation = 0
    prevNode = hamilton[0]
    for v in hamilton:
        if(v != prevNode):
            try:
                summation += graphGreedy[prevNode][v]["weight"]
            except:
                summation += graphGreedy[v][prevNode]["weight"]
            prevNode = v

    print("Cesta podla Greedy algoritmu je:")
    print(hamilton)
    print("cena: " + str(summation))
    return hamilton


def DoubleSpannigTree(array):
    G = nx.Graph()
    loadEdgesEnhanced(G, array)

    minimumSpanningTree = nx.minimum_spanning_tree(G)

    multiGraph = nx.MultiGraph()
    multiGraph.add_edges_from(minimumSpanningTree.edges(data=True))
    multiGraph.add_edges_from(minimumSpanningTree.edges(data=True))

    T = list(nx.eulerian_circuit(multiGraph))

    result = [T[0][0]]
    summation = 0
    prevNode = T[0][0]
    for u, v in T:
        if(v not in result):
            result.append(v)
            summation += G[prevNode][v]["weight"]
            prevNode = v

    result.append(T[0][0])
    try:
        summation += G[result[len(result) - 1]][result[len(result) - 2]]["weight"]
    except:
        summation += G[result[len(result) - 2]][result[len(result) - 1]]["weight"]

    print("Cesta podla algoritmu kostry a parenia je:")
    print(result)
    print("cena: " + str(summation))
    return result

def saveToHTML(array, name):
    m = folium.Map(location=[49.43855509999999, 18.7897828], zoom_start=15)

    for i, val in enumerate(array):
        location = data[val]
        col = "blue"
        if i == 0 or i == len(array) - 1:
            col = "green"
        folium.Marker([float(location[3]), float(location[4])], popup=location[1] + ' ' + location[2], icon=folium.Icon(color=col)).add_to(m)
        if(i + 1 < len(array)):
            iCoords = [float(location[3]), float(location[4])]
            secondLocation = data[array[i+1]]
            jCoords = [float(secondLocation[3]), float(secondLocation[4])]
            polyline = folium.PolyLine(locations=[iCoords, jCoords]).add_to(m)
            folium.Tooltip(i+1).add_to(polyline)
    m.save(name)

while True:
    numberOfPoints = int(input("Zadaj počet vrcholov, ktore sa maju vygenerovať: "))

    arr = generatePoints(numberOfPoints)
    print("\n")
    sp = SpanningTreeMatching(arr)
    print("\n")
    ham = Greedy(arr)
    print("\n")
    doubleTree = DoubleSpannigTree(arr)
    print("\n")
    saveToHTML(sp, 'spanningTree.html')
    saveToHTML(ham, 'greedy.html')
    saveToHTML(doubleTree, 'DoubleSpanningTree.html')
    
    next = input("Chceš pokračovať y/n: ")
    if(next != 'y'):
        break

