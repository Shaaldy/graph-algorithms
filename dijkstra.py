V = [1, 2, 3, 4, 5, 6]  # Вершины графа
E = [(1, 2, 3), (1, 3, 10), (1, 4, 1), (2, 3, 4), (3, 4, 2), (4, 6, 2), (6, 3, 3), (3, 6, 12), (2, 5, 5)]  # Ребра (u, v, вес)

D = {v: float('inf') for v in V}  # Расстояния от источника
A = {v: {u: float('inf') for u in V} for v in V}  # Матрица смежности
n = len(V)
father = {v: None for v in V}  # Массив отцов

for u, v, weight in E:
    A[u][v] = weight


def min_(T):
    w = None
    min_dist = float('inf')
    for v in T:
        if D[v] < min_dist:
            min_dist = D[v]
            w = v
    return w

def dijkstra(s):
    D[s] = 0
    T = set(V) - {s}
    for v in T:
        D[v] = A[s][v]
        father[v] = s
    for _ in range(n):
        w = min_(T)
        T -= {w}
        for v in T:
            if D[v] > D[w] + A[w][v]:
                D[v] = D[w] + A[w][v]
                father[v] = w
    return D


def get_path(t, s):
    path = []
    while t != s:
        path.append(t)
        t = father[t]
    path.reverse()
    return [s] + path


# Запуск алгоритма
source = 1  # Начальная вершина
distances = dijkstra(source)
print(distances)
print(get_path(3, source))
