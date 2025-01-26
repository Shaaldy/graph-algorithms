# Входные данные
V = [1, 2, 3, 4, 5]  # Вершины графа
E = [(1, 2, 1), (1, 3, 2), (3, 2, -3), (3, 5, -1), (2, 5, 6), (2, 4, 10), (4, 5, -2), (5, 4, 4)]  # Ребра (u, v, вес)

D = {v: float('inf') for v in V}  # Расстояния от источника
A = {v: {u: float('inf') for u in V} for v in V}  # Матрица смежности
father = {v: None for v in V}  # Массив отцов

for u, v, weight in E:
    A[u][v] = weight


# Алгоритм Форда-Беллмана с выводом
def ford_bellman(s):
    # Инициализация расстояний
    D[s] = 0
    print(f"Инициализация расстояний: {D}")

    # Первый цикл для начальной вершины
    for v in set(V) - {s}:
        D[v] = A[s][v]  # Обновление расстояний от s к соседям
        father[v] = s
    print(f"После обновления расстояний от стартовой вершины {s}: {D}")

    # Основной цикл
    for k in range(2, len(V)):  # |V| - 1 итерации
        for v in set(V) - {s}:
            for w in set(V):
                if D[v] > D[w] + A[w][v]:
                    D[v] = D[w] + A[w][v]
                    father[v] = w

        print(f"После итерации {k}, расстояния: {D}")

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
distances = ford_bellman(source)
print(get_path(4, source))