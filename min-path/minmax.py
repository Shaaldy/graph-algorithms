V = [1, 2, 3, 4, 5]
E = [(1, 2, float('-inf')), (1, 3, 100), (2, 3, 100), (2, 4, 50), (3, 4, 90), (3, 5, 80), (4, 5, 80)]

A = {v: {u: float('+inf') for u in V} for v in V}
D = {v: float('+inf') for v in V}

n = len(V)
father = {v: None for v in V}
for u, v, e in E:
    A[u][v] = e
    if u != 1:
        A[v][u] = e


def min_(T):
    w = None
    min_res = float('+inf')
    for v in T:
        if D[v] < min_res:
            min_res = D[v]
            w = v
    return w

def modify_dijkstra(s, t):
    D[s] = float('-inf')
    father[s] = s
    S = {s}
    T = set(V) - {s}
    for v in T:
        D[v] = A[s][v]
        father[v] = s
    while t not in S:
        w = min_(T)
        T -= {w}
        S.add(w)
        for v in T:
            if D[v] > max(D[w], A[w][v]):
                D[v] = max(D[w], A[w][v])
                father[v] = w
    d = D[t]
    if d < float('+inf'):
        v = t
        path = []
        while v != s:
            path.append(v)
            v = father[v]
        path.reverse()
        return [s] + path

start = 1
print(modify_dijkstra(start, 5))