
def CCs(graph):
	def connected():
		global G, visited, id, count
		G = graph
		visited = [0]*len(G)
		id = 0
		count = []
		for u in range(len(G)):
			if not visited[u]:
				id += 1
				count.append(0)
				dfs(u)
		return count

	def dfs(u):
		global G, visited, id, count
		visited[u] = id
		count[id-1] += 1
		for v in G[u]:
			if not visited[v]:
				dfs(v)

	def averange(res):
		size = 0
		for c in res:
			size += c
		return size/len(res)

	result = connected()
	return len(result), averange(result)



def pointsBridges(graph):
	def tarjan():
		global G, depth, low, parents, points, bridges
		G = graph
		depth = [-1]*len(G)
		low = [-1]*len(G)
		parents = [-1]*len(G)
		points, bridges = set(), set()
		for u in range(len(G)):
			if depth[u] == -1:
				depth[u] = low[u] = 0
				dfs(u)
		return len(points), len(bridges)

	def dfs(u):
		global G, depth, low, parents, points, bridges
		children = 0
		for v in G[u]:
			if depth[v] == -1:
				children += 1
				depth[v] = low[v] = depth[u]+1
				parents[v] = u
				dfs(v)
				low[u] = min(low[u], low[v])
				if (parents[u] == -1 and children > 1) or (parents[u] != -1 and depth[u] <= low[v]):
					points.add(u)
				if (depth[u] < low[v]):
					bridges.add((u,v))
			elif parents[u] != v:
				low[u] = min(low[u], depth[v])

	return tarjan()


def nodeDegree(graph):
	def degree():
		global G
		G = graph
		degrees = [0]*len(G)
		for u in range(len(G)):
			degrees[u] += len(G[u])
		#	for v in G[u]:
		#		degrees[v] += 1
		return degrees

	def count():
		size = 0
		degrees = degree()
		for d in degrees:
			size += d
		return size/len(degrees)

	return count()


def figure(graph, dm):
	def multiply(g, gg):
		G = [[0]*len(g) for n in range(len(g))]
		for u in range(len(g)):
			for v in range(len(g)):
				G[u][v] = 0
				for n in range(len(g)):
					G[u][v] += g[u][n]*gg[n][v]
		return G

	def diagonal(g):
		d = 0
		for n in range(len(g)):
			d += g[n][n]
		return d

	first = [[0]*len(graph) for n in range(len(graph))]
	result = first

	for u in range(len(graph)):
		for v in graph[u]:
			result[u][v] = 1

	for d in range(1, dm):
		result = multiply(first, result)

	return diagonal(result)/(dm*2)

def triplets(G):
	def combinations(vs):
		for n in range(len(vs)):
			math.log2()
	tris = set() ### Sin permutaciones
	for u in range(len(G)):
		for v in range(len(G[u])):
			for w in range(v, len(G[u])):
				if G[u][v] != G[u][w] != u:
					tris.add(tuple(sorted([u, G[u][v], G[u][w]])))
	return len(tris)
