from itertools import groupby

f = open("hamlet.txt", "r")
hamlet = f.read()
f.close()

frequencies = dict([(key, len(list(group))) for key, group in groupby(sorted(hamlet))])
Nin = sum([frequencies[a] for a in frequencies])
p = dict([(a,frequencies[a]/Nin) for a in frequencies])

f = [0.0]
for a in p:
    f.append(f[-1]+p[a])
f.pop()
f = dict([ (a, f[k]) for a, k in zip(p, range(len(p))) ])

lo, hi = 0.0, 1.0
n = 4
for k in range(n):
    a = hamlet[k]
    lohi_range = hi - lo
    hi = lo + lohi_range * (f[a] + p[a])
    lo = lo + lohi_range * f[a]

print('lo = {0}, hi = {1}, hi-lo = {2}'.format(lo, hi, hi - lo))