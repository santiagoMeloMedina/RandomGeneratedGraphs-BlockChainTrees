from collections import deque

def depthAll(G, s, r):
    d = deque()
    visited = [0 for n in range(len(G))]
    d.append((s, 0, r[s]))
    depths = []
    while len(d):
        u, p, w = d.popleft()
        depths.append((w, p, u))
        visited[u] = 1
        for v in G[u]:
            if not visited[v]:
                d.append((v, p+1, r[v]))
    return sorted(depths)

def longestArm(G, s):
    d = deque()
    visited = [0 for n in range(len(G))]
    d.append((s, 0))
    depths = []
    while len(d):
        u, p = d.popleft()
        depths.append((p, u))
        visited[u] = 1
        for v in G[u]:
            if not visited[v]:
                d.append((v, p+1))
    return sorted(depths)
