from math import *

def pSL(n):
    ps = []
    v1 = 0
    for p in range(n*2+1):
        ps.append(v1/100)
        v1 += 5
    return ps

def flotantes(f, s, grow):
	floats = []
	while f < s:
		floats.append(f)
		f += grow
	return floats
