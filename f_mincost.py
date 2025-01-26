from collections import defaultdict, deque
from math import inf

# Входные данные
n, m = 4, 5  # Размеры матриц
p = [[2, 3, 1, 4, 5],  # Матрица p (стоимость пути)
     [4, 1, 3, 2, 6],
     [5, 3, 2, 1, 4],
     [3, 4, 6, 2, 1]]
q = [[1, 2, 3, 1, 4],  # Матрица q (штраф за использование)
     [2, 3, 4, 1, 5],
     [1, 4, 2, 3, 6],
     [3, 2, 1, 4, 5]]
S = [10, 15, 20, 10]  # Стоимость истока -> источники
V = [15, 10, 10, 10]  # Пропускная способность источников
k = 5  # Желаемый поток

# Построение начальной сети
A = defaultdict(dict)
source = n + m  # Вершина s*
sink = n + m + 1  # Вершина t*

# Добавляем ребра от истока s* к источникам
for i in range(n):
    cost = S[i]  # Используем стоимость S[i]
    capacity = V[i]  # Пропускная способность V[i]
    A[source][i] = [cost, capacity]

# Добавляем ребра от источников к производству
for i in range(n):
    for j in range(m):
        cost = p[i][j] + q[i][j]  # Стоимость ребра
        capacity = 1  # Пропускная способность между вершинами i и j
        A[i][n + j] = [cost, capacity]

# Добавляем ребра от производства к стоку t
for j in range(m):
    cost = 0  # Стоимость 0
    capacity = 1e6  # Пропускная способность ограничена емкостью 1,000,000
    A[n + j][sink] = [cost, capacity]

# Инициализация потока
flow = defaultdict(lambda: defaultdict(int))

# Алгоритм Форда-Беллмана для поиска цепи минимальной стоимости
def ford_bellman(s, t):
    dist = {v: inf for v in A}
    parent = {v: None for v in A}
    dist[s] = 0

    for _ in range(len(A) - 1):  # |V| - 1 итераций
        for u in A:
            for v in A[u]:
                cost, capacity = A[u][v]
                residual_capacity = capacity - flow[u][v]
                if residual_capacity > 0 and dist[u] + cost < dist[v]:
                    dist[v] = dist[u] + cost
                    parent[v] = u

    # Восстановление пути
    if dist[t] == inf:
        return None  # Пути нет

    path = []
    current = t
    while current != s:
        path.append((parent[current], current))
        current = parent[current]
    path.reverse()
    return path

# Обновление потока вдоль найденной цепи
def augment_flow(path):
    # Определяем минимальную остаточную емкость на пути
    min_capacity = inf
    for u, v in path:
        _, capacity = A[u][v]
        min_capacity = min(min_capacity, capacity - flow[u][v])

    # Увеличиваем поток вдоль пути
    for u, v in path:
        flow[u][v] += min_capacity
        flow[v][u] -= min_capacity  # Обратное ребро

    return min_capacity

# Основной алгоритм
current_flow = 0
while current_flow < k:
    path = ford_bellman(source, sink)
    if not path:
        break  # Пути нет, завершаем

    augment_flow(path)
    current_flow += 1  # В данном случае шаг увеличения равен 1

# Результат
if current_flow == k:
    print("Найден поток величины k:")
    for u in flow:
        for v in flow[u]:
            if flow[u][v] > 0:
                print(f"{u} -> {v}: {flow[u][v]}")
else:
    print("Решение не существует")
