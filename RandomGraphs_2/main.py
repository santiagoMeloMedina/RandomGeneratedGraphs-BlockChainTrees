import makeGraph as mg
import metrics as mtcs
import granularity as gr

import random
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import deque


seed = 672
type = 1
psmall, plarge = gr.pSL(10)

def FsAll(n, p):
    global seed, type
    G, graph, GA = mg.gph(n, p, seed, type)
    ccs, accs = mtcs.CCs(G)
    points, bridges = mtcs.pointsBridges(G)
    degree = mtcs.nodeDegree(G)
    return ccs, accs, points, bridges, degree, graph

def FsCCs(n, p):
    global seed, type
    G, graph, GA = mg.gph(n, p, seed, type)
    ccs, accs = mtcs.CCs(G)
    return ccs

def FsACCs(n, p):
    global seed, type
    G, graph, GA = mg.gph(n, p, seed, type)
    ccs, accs = mtcs.CCs(G)
    return accs

def FsBridges(n, p):
    global seed, type
    G, graph, GA = mg.gph(n, p, seed, type)
    points, bridges = mtcs.pointsBridges(G)
    return bridges

def FsPoints(n, p):
    global seed, type
    G, graph, GA = mg.gph(n, p, seed, type)
    points, bridges = mtcs.pointsBridges(G)
    return points

def FsTT(n, p):
    global seed, type
    G, graph, GA = mg.gph(n, p, seed, type)
    triangles, triplets = mtcs.figure(G, 3), mtcs.triplets(G)
    return triangles, triplets, graph

def Fps(n, qg, psmall, plarge):
    global seed
    meansf, meansfa = [0]*7, [[] for n in range(7)]
    seeds = []
    for p in tqdm(psmall):
        for s in range(qg):
            seed = random.randint(1, 100000)
            seeds.append(seed)
            result = FsAll(n, p)
            for r in range(len(result)-1): meansf[r] += result[r]
            triangles, triplets, gga = FsTT(20, p)
            meansf[5] += triangles; meansf[6] += triplets
        for m in range(7):
            meansfa[m].append(meansf[m]/qg)
            meansf[m] = 0

    for p in tqdm(plarge):
        for s in range(qg):
            seed = random.randint(1, 100000)
            seeds.append(seed)
            ccs = FsCCs(n, p)
            meansf[0] += ccs
            triangles, triplets, gga = FsTT(20, p)
            meansf[5] += triangles; meansf[6] += triplets
        meansfa[0].append(meansf[0]/qg); meansfa[5].append(meansf[5]/qg); meansfa[6].append(meansf[6]/qg)
        meansf[0] = 0; meansf[5] = 0; meansf[6] = 0
    return meansfa, seeds


def FspBridges(n, qg, p):
    global seed
    bridges = 0
    for s in range(qg):
        seed = random.randint(1, 100000)
        bridges += FsBridges(n, p);
    return bridges/qg

def FspPoints(n, qg, p):
    global seed
    points = 0
    for s in range(qg):
        seed = random.randint(1, 100000)
        points += FsPoints(n, p);
    return points/qg

def FspACCs(n, qg, p):
    global seed
    accs = 0
    for s in range(qg):
        seed = random.randint(1, 100000)
        accs += FsACCs(n, p);
    return accs/qg


def maximizar(edges, psmall, metric):
    higher = max(edges)
    tmp = edges.index(higher)
    l, r = tmp-1 if tmp else 0, tmp+1 if tmp < len(edges) else len(edges)-1
    l, r = psmall[l], psmall[r]
    for n in tqdm(range(1000)):
        middle = l + ((r-l)/2)
        if metric: fp = FspBridges(100, 200, middle)
        else: fp = FspPoints(100, 200, middle)
        if fp >= higher:
            higher = fp
            l = middle
        else:
            r = middle
    return middle, higher


def derivate(xs, ys, grade):
    if grade:
        dx = []
        for s in range(len(xs)-1):
            x1, x2 = xs[s], xs[s+1]
            y1, y2 = ys[s], ys[s+1]
            dx.append((y2-y1)/(x2-x1))
        result = derivate(xs[:-1], dx, grade-1)
    else:
        result = xs, ys
    return result


def inflexion(ins, xs):
    points = deque()
    positivo = True
    for n in range(len(ins)):
        tmp = True if ins[n] >= 0 else False
        if positivo != tmp:
            points.append(xs[n])
            positivo = tmp
    higher = (float("-inf"), 0)
    if len(points):
        point = points.popleft()
        higher = (FspACCs(15, 200, point), point)
    for p in tqdm(points):
        calculo = FspACCs(15, 200, p)
        higher = (calculo, p) if calculo > higher[0] else (higher[0], higher[1])
    return higher[1]


### Part 2_1
data = FsAll(15, 0.2)
tts = FsTT(15, 0.2)
data = (data[0], data[1], data[2], data[3], data[4], tts[0], tts[1], data[5])
text = ["Number of connected components: {}",
        "Average size of the connected components: {}",
        "Number of articulation points: {}",
        "Number of bridges: {}",
        "Average node degree: {}",
        "Number of triangles (u ↔ v ↔ w with u ↔ w): {}",
        "Number of triplets (u ↔ v ↔ w): {}", ""]

for n in range(len(data)):
    print(text[n].format(data[n]))
nx.draw_circular(data[len(data)-1], with_labels=True)
plt.show()
nx.draw_circular(tts[2], with_labels=True)
plt.show()


### Part 2_2
data = Fps(100, 200, psmall, plarge)
plt.title("Parte 2_2")
dataleft = [[] for n in range(4)]
names = [("CCs", "Number of CCs: {}"), ("%CCs", "Promedio de tamaño de CCs: {}"),
        ("Points", "Numero puntos de articulacion: {}"), ("Bridges", "Numero de puentes: {}"), ("Deegres", "Numero de degree de los nodos: {}"),
        ("Triangles", "Numero de triangulos: {}"), ("Triplets", "Numero de tripletas: {}")]
names2 = [("CCs", "Number of CCs: {}"), ("Triangles", "Numero de triangulos: {}"), ("Triplets", "Numero de tripletas: {}")]
data[0][0], dataleft[0] = data[0][0][0:len(psmall)], data[0][0][len(psmall):len(data[0][0])]
data[0][5], dataleft[1] = data[0][5][0:len(psmall)], data[0][5][len(psmall):len(data[0][5])]
data[0][6], dataleft[2] = data[0][6][0:len(psmall)], data[0][6][len(psmall):len(data[0][6])]
print("Psmall: ")
for n in range(len(data[0])):
    plt.plot(psmall, data[0][n], label=names[n][0])
    print(names[n][1].format(', '.join([str(s) for s in data[0][n]])))
plt.legend()
plt.show()
dataleft[3] = [data[0][5][n]/(data[0][6][n] if data[0][6][n] else 1) for n in range(len(psmall))]
dataleft[3] += [dataleft[1][n]/dataleft[2][n] for n in range(len(plarge))]
print("\nPlarge: ")
for n in range(3):
    plt.plot(plarge, dataleft[n], label=names2[n][0])
    print(names2[n][1].format(', '.join([str(s) for s in dataleft[n]])))
plt.legend()
plt.show()
plt.plot(psmall+plarge, dataleft[3], label="Triangles/Triplets")
plt.legend()
plt.show()


### Part 2_3
p1 = maximizar(data[0][3], psmall, 1)
p2 = maximizar(data[0][2], psmall, 0)
ins = derivate(psmall, data[0][1], 2)
print("Valor p1 que maximiza numero de puentes: {}\nValor p2 que maximiza numero de puntos de articulacion: {}".format(p1[0], p2[0]))
print("Punto de inflexion de tamaño promedio de CCs: {}".format(str(inflexion(ins[1], ins[0]))))
