from collections import deque

def tarjan(g):
    global G, depth, low, parents, visited, scc, scctmp, num_components, sccindex, countscc
    G = g
    depth = [-1]*len(G)
    low = [-1]*len(G)
    visited = [0]*len(G)
    scc, scctmp, sccindex = [], deque(), [n for n in range(len(G))]
    countscc = 0
    num_components = 0
    for u in range(len(G)):
        if depth[u] == -1:
            dfs(u)
    return scc, sccindex

def dfs(u):
    global G, depth, low, parents, visited, scc, scctmp, num_components, sccindex, countscc
    depth[u] = low[u] = num_components
    num_components += 1
    visited[u] = 1
    scctmp.append(u)
    for v in G[u]:
        if depth[v] == -1:
            dfs(v)
            low[u] = min(low[u], low[v])
        elif visited[v]:
            low[u] = min(low[u], depth[v])
    if (low[u]==depth[u]):
        s = scctmp.pop()
        tmp = []
        while s != u:
            tmp.append(s)
            sccindex[s] = countscc
            s = scctmp.pop()
        tmp.append(s)
        sccindex[s] = countscc
        scc.append(tmp)
        countscc += 1


def averange(GA, scci):
    value = 0
    for u, v in GA:
        if scci[u] != scci[v]:
            value += 1
    return value