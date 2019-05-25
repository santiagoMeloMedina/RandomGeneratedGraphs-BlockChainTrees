import networkx as nx
import random

def erdosRenyi(V, p, s, d):     # adjacency lists
    """ V: # of nodes
        p: probability of generating an edge
        s: seed
        d: Undirected if True else Directed
    """
    G = [[] for n in range(V)]
    GA = []
    rdm = random
    rdm.seed(s)
    for u in range(V):
        for v in range(V):
            if u != v:
                odds = rdm.random()
                if odds <= p:
                    G[u].append(v)
                    GA.append((u,v))
                    if d:
                        G[v].append(u)
                        GA.append((v,u))
    return G, GA



def gph(V, p, s, d):        # adjacency lists & networks structure
    G, GA = erdosRenyi(V, p, s, d)
    if d: graph = nx.Graph()
    else: graph = nx.DiGraph()
    graph.add_nodes_from([n for n in range(len(G))])
    for u in range(len(G)):
        for v in G[u]:
            graph.add_edge(u,v)
    return (G, graph, GA)
