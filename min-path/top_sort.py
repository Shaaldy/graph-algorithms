V = [6, 5, 4, 3, 2, 1]  # Вершины графа
E = [(1, 2, 4), (1, 4, 3), (1, 5, 10), (2, 3, 7), (4, 5, 5), (4, 6, -6), (5, 6, -6), (2, 5, -2)]  # Ребра (u, v, вес)

D = {v: float('inf') for v in V}  # Расстояния от источника
A = {v: {u: float('inf') for u in V} for v in V}  # Матрица смежности
prev = {v: [] for v in V}

n = len(V)
father = {v: None for v in V}  # Массив отцов

for u, v, weight in E:
    prev[v].append(u)
    A[u][v] = weight


def topological_sort():
    deg = {v: 0 for v in V}  # Инициализация степеней входа
    index = {v: 0 for v in V}  # Индексы для хранения порядка сортировки

    for v in V:
        for w in prev[v]:
            deg[v] = deg[w] + 1

    stk = []
    N = n
    for v in V:
        if deg[v] == 0:
            stk.append(v)
    while stk:
        v = stk.pop(0)
        index[v] = N
        N -= 1
        for w in prev[v]:
            deg[w] -= 1
            if deg[w] == 0:
                stk = [w] + stk
    return index


def distances(s):
    V = topological_sort()
    print(V)
    D[s] = 0  # Расстояние до источника равно 0
    for v in set(V) - {s}:
        D[v] = float('inf')

    for m in V:
        u = m  # Текущая вершина в порядке
        for v in prev[u]:  # Проходим по всем вершинам
            a = min(D[u], D[v] + A[v][u])
            D[u] = a  # Обновляем минимальное расстояние
    return D


print(distances(1))
