from math import *

def pSL(n):
    ps, pl = [], []
    v1, v2 = 0, 10
    for p in range(n*2):
        ps.append(v1/1000); pl.append(v2/100)
        v1 += 5; v2 += 5
    pl.pop()
    return ps, pl

def flotantes(f, s, grow):
	floats = []
	while f < s:
		floats.append(f)
		f += grow
	return floats