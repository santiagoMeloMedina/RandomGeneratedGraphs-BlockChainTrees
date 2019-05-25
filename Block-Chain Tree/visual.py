import networkx as nx

def transform(G, B):
    graph = nx.DiGraph()
    for u in range(len(G)):
        graph.add_node("{} {}".format(u, B[u].time))
    for u in range(len(G)):
        for v in G[u]:
            uu, vv = "{} {}".format(u, B[u].time), "{} {}".format(v, B[v].time)
            graph.add_edge(uu, vv)
    return graph
