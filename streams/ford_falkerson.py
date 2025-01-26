# Инициализация графа
V = [1, 2, 3, 4]  # Вершины графа
E = [(2, 3, 1), (1, 3, 0.5), (1, 4, 1)]  # Ребра (u, v, вес)

# Добавляем фиктивные источники и стоки
s = 0  # Источник
V.append(s)
t = len(V)  # Сток
V.append(t)

# Добавляем ребра от источника и к стоку
E.extend([
    (s, 1, 1),
    (s, 2, 1),
    (3, t, 1),
    (4, t, 1)
])

# Инициализация матриц и массивов
F = {v: {u: 0 for u in V} for v in V}  # Матрица потоков
C = {v: {u: float('+inf') for u in V} for v in V}  # Матрица пропускных способностей
father = {v: None for v in V}  # Массив предков
method = {v: None for v in V}  # Массив способов достижения вершины

next_ = {v: [] for v in V}  # Список соседей, в которые можно перейти
prev = {v: [] for v in V}  # Список соседей, из которых можно прийти

d = {v: float('+inf') for v in V}  # Метка для алгоритма

# Заполняем матрицы C и списки смежности
for u, v, weight in E:
    C[u][v] = weight
    next_[u].append(v)
    prev[v].append(u)


# Функция для пометки пути
def mark(F):
    for v in V:
        d[v] = float('+inf')  # Сбрасываем метки
    q = [s]  # Очередь для обхода
    father[s] = None  # Источник не имеет предка

    while q and t not in q:  # Пока очередь не пуста и сток не найден
        w = q.pop(0)  # Удаляем вершину из очереди
        # Прямое ребро
        for v in next_[w]:
            if d[v] == float('+inf') and C[w][v] - F[w][v] > 0:
                d[v] = min(d[w], C[w][v] - F[w][v])
                father[v] = w
                q.append(v)
                method[v] = 1
        # Обратное ребро
        for v in prev[w]:
            if v != s and d[v] == float('+inf') and F[v][w] > 0:
                d[v] = min(d[w], F[v][w])
                father[v] = w
                q.append(v)
                method[v] = -1


# Реализация алгоритма Форда-Фалкерсона
def ford_falkerson():
    f = 0  # Максимальный поток
    while True:
        mark(F)  # Ищем аугментирующий путь
        if d[t] < float('+inf'):  # Если есть путь до стока
            f += d[t]
            v = t
            while v != s:  # Обновляем потоки вдоль пути
                w = father[v]
                if method[v] == 1:
                    F[w][v] += d[t]
                else:
                    F[v][w] -= d[t]
                v = w
        else:  # Если пути нет, выходим
            break
    return f, F


# Вычисление максимального потока
max_flow, flow_matrix = ford_falkerson()

# Вывод результата
print("Матрица потоков:")
for u in V:
    for v in V:
        if F[u][v] > 0:
            print(f"Поток из {u} в {v}: {F[u][v]}")

print("\nМаксимальный поток:", max_flow)
