V = [1, 2, 3, 4]  # Вершины графа
E = [(1, 3, 3, 1), (1, 4, 3, 2), (2, 3, 4, 3), (2, 4, 4, 10)]  # Ребра (u, v, вес, стоимость)

k = 7

# Добавляем фиктивные источники и стоки
s = 0  # Источник
V.append(s)
t = len(V)  # Сток
V.append(t)

# Добавляем ребра от источника и к стоку
E.extend([
    (s, 1, 3, 0),
    (s, 2, 4, 0),
    (3, t, 2, 0),
    (4, t, 5, 0),
])

s_ = -1
V.append(s_)
E.append((s_, s, k, 0))

# Инициализация матриц и массивов
F = {v: {u: 0 for u in V} for v in V}  # Матрица потоков
R = {v: {u: 0 for u in V} for v in V}  # Матрица стоимости
C = {v: {u: float('+inf') for u in V} for v in V}  # Матрица пропускных способностей

father = {v: None for v in V}  # Массив предков

d = {v: float('+inf') for v in V}  # Метка для алгоритма

# Заполняем матрицы C и R и списки смежности
for u, v, weight, cost in E:
    C[u][v] = weight
    R[u][v] = cost


# Вывод результата
def printF():
    print("Матрица потоков:")
    for u in V:
        for v in V:
            if F[u][v] > 0:
                print(f"Поток из {u} в {v}: {F[u][v]}")


def ford_bellman(s, C):
    D = {v: float('inf') for v in V}  # Расстояния от источника
    D[s] = 0
    # print(f"Инициализация расстояний: {D}")

    # Первый цикл для начальной вершины
    for v in set(V) - {s}:
        D[v] = C[s][v]  # Обновление расстояний от s к соседям
        father[v] = s
    # print(f"После обновления расстояний от стартовой вершины {s}: {D}")

    # Основной цикл
    for k in range(2, len(V)):
        for v in set(V) - {s}:
            for w in set(V):
                if D[v] > D[w] + C[w][v]:
                    D[v] = D[w] + C[w][v]
                    father[v] = w

        # print(f"После итерации {k}, расстояния: {D}")


def get_path(t, s):
    path = []
    while t != s:
        path.append((father[t], t))  # Добавляем ребро (откуда -> куда)
        t = father[t]
    path.reverse()  # Инвертируем порядок, чтобы путь шел от s к t
    return path


def make_graph():
    new_E = []
    new_C = {q: {u: float('+inf') for u in V} for q in V}
    for v, w, c, r in E:
        if F[v][w] < C[v][w]:
            new_E.append((v, w, r))
            new_C[v][w] = r
        if F[v][w] > 0:
            new_E.append((w, v, -r))
            new_C[w][v] = -r
    return new_E, new_C


def sign(v, w, path):
    if (v, w) in path:
        return 1
    elif (w, v) in path:
        return -1
    else:
        return 0


def h(path):
    h = float('+inf')
    for v, w in path:  # path уже представлен как список ребер
        h = min(h, C[v][w] - F[v][w])
    return h


def min_cost_flow(k):
    f = 0
    while True:
        new_E, new_C = make_graph()

        ford_bellman(s_, new_C)
        path = get_path(t, s_)
        d_temp = h(path)
        if len(path) > 2:
            f += d_temp
            for v, w, c, _ in E:
                a = sign(v, w, path)
                F[v][w] += a * d_temp

        else:
            break
        printF()
    if f == k:
        return F
    else:
        print("Решения не существует")

def calculate_flow_cost():
    """
    Вычисляет суммарную стоимость потока в графе.
    :param C: матрица пропускных способностей (dict of dict)
    :param F: матрица потоков (dict of dict)
    :param R: матрица стоимости рёбер (dict of dict)
    :return: суммарная стоимость потока
    """
    total_cost = 0
    for v in F:  # Перебираем вершины-истоки
        for w in F[v]:  # Перебираем вершины-назначения
            if F[v][w] > 0:  # Если через ребро идет поток
                total_cost += F[v][w] * R[v][w]  # f(e) * r(e)
    return total_cost

def printF_MATRIX():
    print("Матрица потоков (без учета истока и стока):")
    for u in V:
        if u != s and u != t and u!= s_:  # Пропускаем источник и сток
            row = []
            for v in V:
                if v != s and v != t and v != s_:
                    if F[u][v] > 0:# Пропускаем источник и сток
                        row.append(F[u][v])  # Собираем значения потока в строку
                    else:
                        row.append(0)
            print(row)  # Печатаем строку потока для вершины u

# Вычисление максимального потока
flow_matrix = min_cost_flow(k)
printF_MATRIX()
print("\nМаксимальный поток:", k)

print(calculate_flow_cost())