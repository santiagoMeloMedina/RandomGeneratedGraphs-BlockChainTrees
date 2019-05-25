import search as sch
import random
from numpy.random import exponential as nre ## Debugging
import networkx as nx
import matplotlib.pyplot as plt
import visual as vs
from tqdm import tqdm
import granularity as gr
from sys import *
import math

class Block:
    def __init__(self, time, delay):
        self.time = time
        self.delay = delay

class Chain:
    def __init__(self):
        self.blocks = [Block(0,0)]
        self.tree = [[]]

    def times(self):
        return [t.time for t in self.blocks]

    def sumtimes(self): ## Reserved for debugging
        count = 0
        for t in self.blocks: count += t.time
        return count

    def subBlock(self, time, ordered):
        t = 1
        sub = [(0,0,0)]
        while t < len(ordered) and time >= ordered[t][0]:
            sub.append(ordered[t])
            t += 1
        return sub

    def depthest(self, sub):
        depth = []
        for t, d, u in sub:
            depth.append((d, t, u))
        depth = sorted(depth)
        return depth[len(depth)-1][2]

    def delays(self):
        return [d.delay for d in self.blocks]

    def longestArm(self):
        whole = sch.longestArm(self.tree, 0)
        return whole[len(whole)-1][0], len(self.blocks)-whole[len(whole)-1][0]-1

    def TorD(self, p):
        return (-1)*(p)*math.log(1-random.random())

    def addBlock(self, prob):
        t, delay = self.TorD(1), self.TorD(prob)
        time = self.blocks[len(self.blocks)-1].time+t
        block = Block(time, delay)
        longest = sch.depthAll(self.tree, 0, self.times())
        sub = self.subBlock(time-delay, longest)
        u = self.depthest(sub)
        self.tree[u].append(len(self.blocks))
        self.tree.append([])
        self.blocks.append(block)

    def reset(self):
        self.blocks = [Block(0,0)]
        self.tree = [[]]


def treeShow(p, nodes):
    c = Chain()
    for n in range(nodes):
        c.addBlock(p)
    nx.draw(vs.transform(c.tree, c.blocks), with_labels=True)
    plt.show()

def main(simulations, B):
    c = Chain()
    ps = gr.pSL(20)
    data = [[0,0] for n in range(len(ps))]
    longest, blocks = [], []
    for s in tqdm(range(simulations)):
        tmp = []
        for p in ps:
            for n in range(B):
                c.addBlock(p)
            tmp.append(c.longestArm())
            c.reset()
        for n in range(len(ps)):
            data[n][0] += tmp[n][0]
            data[n][1] += tmp[n][1]
    for d in range(len(data)):
        rama = data[d][0] / simulations
        bloques = data[d][1] / simulations
        data[d] = (rama, bloques)
        longest.append(rama)
        blocks.append(bloques)

    plt.title("Longest/Lost")
    plt.plot(ps, longest, label="Longest branch")
    plt.plot(ps, blocks, label="Blocks lost")
    plt.xlabel("p")
    plt.ylabel("Nodes (n)")
    plt.legend()
    plt.show()
    print(data)

main(int(argv[1]), int(argv[2]))
# treeShow(float(argv[1]), int(argv[2]))
