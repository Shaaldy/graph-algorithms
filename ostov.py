# Входные данные
V = [1, 2, 3, 4, 5, 6]  # Вершины графа
E = [(1, 2, 2), (1, 3, 3), (1, 4, 4), (2, 4, 3), (3, 4, 2), (3, 5, 4), (4, 6, 4), (3, 6, 5), (5, 6, 2)]  # Ребра (u, v, вес)

# Служебные массивы
d = {}  # Минимальные расстояния от леса до каждой вершины
near = {}  # Ближайшая вершина из леса
A = {}  # Матрица смежности
T = []  # Остовное дерево

# Построение матрицы смежности
def build_adjacency_matrix(V, E):
    A = {v: {u: float('inf') for u in V} for v in V}
    for u, v, weight in E:
        A[u][v] = weight
        A[v][u] = weight
    return A

# Функция для выбора вершины с минимальным расстоянием
def min_(F):
    return min(F, key=lambda v: d[v])

# Алгоритм Прима
def primo(V, E):
    global d, near, T

    # Построение матрицы смежности
    A = build_adjacency_matrix(V, E)

    # Начальная вершина
    w = V[0]
    F = set(V) - {w}  # Множество оставшихся вершин
    T = []

    # Инициализация расстояний
    for v in F:
        near[v] = w
        d[v] = A[w][v]

    print(f"Начальная вершина: {w}")
    print(f"Инициализированные расстояния: {d}")
    print(f"Инициализированные ближайшие вершины: {near}\n")

    # Поиск минимального остовного дерева
    while len(T) < len(V) - 1:
        # Выбор вершины с минимальным расстоянием
        v = min_(F)
        T.append((v, near[v]))
        print(f"Добавлено ребро: ({v}, {near[v]}) с весом {d[v]}")

        # Обновление леса
        F.remove(v)

        # Обновление расстояний
        for u in F:
            if d[u] > A[u][v]:
                d[u] = A[u][v]
                near[u] = v

        print(f"Обновленные расстояния: {d}")
        print(f"Обновленные ближайшие вершины: {near}\n")

    return T
    
# Запуск алгоритма
T = primo(V, E)

# Вывод результата
print("Минимальное остовное дерево:")
for edge in T:
    print(edge)
