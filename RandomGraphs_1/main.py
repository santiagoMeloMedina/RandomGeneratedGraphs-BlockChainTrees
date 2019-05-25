import makeGraph as mg
import sccGraph as sccg
import granularity as gr

import random
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import deque


seed = 672
type = 0
psmall, plarge = gr.pSL(10)

def Fs(n, p):
    global seed, type
    G, graph, GA = mg.gph(n, p, seed, type)
    scc, scci = sccg.tarjan(G)
    size = 0
    for s in scc: size += len(s)
    size /= len(scc)
    return len(scc), size, sccg.averange(GA, scci), graph

def Fps(n, qg, psmall):
    global seed
    meanf1, meanf2, meanf3 = 0, 0, 0
    seeds = []
    meanf1a, meanf2a, meanf3a = [], [], []
    for p in tqdm(psmall):
        for s in range(qg):
            seed = random.randint(1, 100000)
            seeds.append(seed)
            result = Fs(n, p)
            meanf1 += result[0]
            meanf2 += result[1]
            meanf3 += result[2]
        meanf1a.append(meanf1/qg)
        meanf2a.append(meanf2/qg)
        meanf3a.append(meanf3/qg)
        meanf1, meanf2, meanf3 = 0, 0, 0
    return meanf1a, meanf2a, meanf3a, seeds


def Fpsl(n, qg, p):
    global seed
    meanf3 = 0
    for s in range(qg):
        seed = random.randint(1, 100000)
        result = Fs(n, p)
        meanf3 += result[2]
    return meanf3/qg


def maximizar(edges, psmall):
    higher = max(edges)
    tmp = edges.index(higher)
    l, r = tmp-1 if tmp else 0, tmp+1 if tmp < len(edges) else len(edges)-1
    l, r = psmall[l], psmall[r]
    for n in tqdm(range(1000)):
        middle = l + ((r-l)/2)
        fp = Fpsl(100, 200, middle)
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
            points.append((xs[n], ins[n]))
            positivo = tmp
    higher = (float("-inf"), 0)
    if len(points):
        point = points.popleft()
        higher = (Fpsl(100, 200, point[0]), point[0])
    for p, pp in points:
        calculo = Fpsl(100, 200, p)
        higher = (calculo, p) if calculo > higher[0] else (higher[0], higher[1])
    return higher[1]


### Part 1_1
data = Fs(15, 0.2)
print("""Componentes fuertemente conectados ('SCC'): {} \nTamaño promedio de SCCs: {} \nNumero de aristas que conectan 2 SCCs: {}\n""".format(data[0], data[1], data[2]))
nx.draw_circular(data[3], with_labels=True)
plt.show()


### Part 1_2
data = Fps(100, 200, psmall)
print("Valores de promedio metricas en F(n,p):")
print("SCCs: " + ' '.join([ str(n) for n in data[0]]) + "\n")
print("Tamaño promedio SCCs: " + ' '.join([ str(n) for n in data[1]]) + "\n")
print("Aristas que conectan SCCs: " + ' '.join([ str(n) for n in data[2]]) + "\n")
print('')
plt.title("Parte 1_2")
plt.plot(psmall, data[0], label="SCCs")
plt.plot(psmall, data[1], label="% SCCs")
plt.plot(psmall, data[2], label="Aristas SCCs")
plt.legend()
plt.show()


### Part 1_3
p = maximizar(data[2], psmall)
ins = derivate(psmall, data[1], 2)
print("Valor p que maximiza numero de aristas entre 2 SCCs: {}".format(p[0]))
print("Punto de inflexion de tamaño promedio de SCCs: {}".format(str(inflexion(ins[1], ins[0]))))
