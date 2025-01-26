input_file = 'in.txt'
output_file = 'out.txt'
V = []  # узлы
E = []  # вершины



father = {v: None for v in V}  # Массив предков

d = {v: float('+inf') for v in V}  # Метка для алгоритма


def ford_bellman(s, C):
    D = {v: float('inf') for v in V}
    D[s] = 0

    # Первый цикл для начальной вершины
    for v in set(V) - {s}:
        D[v] = C[s][v]  # Обновление расстояний от s к соседям
        father[v] = s

    for k in range(2, len(V)):
        for v in set(V) - {s}:
            for w in set(V):
                if D[v] > D[w] + C[w][v]:
                    D[v] = D[w] + C[w][v]
                    father[v] = w
    return D


# путь по отцам
def get_path(t, s):
    path = []
    while t != s:
        path.append((father[t], t))
        t = father[t]
    path.reverse()
    return path


# остаточная сеть для двойственного алгоритма
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


# функия sign для направления дуги
def sign(v, w, path):
    if (v, w) in path:
        return 1
    elif (w, v) in path:
        return -1
    else:
        return 0


# инкремент потока
def h(path):
    h = float('+inf')
    for v, w in path:
        h = min(h, C[v][w] - F[v][w])
    return h


# двойственный алгоритм
def min_cost_flow():
    f = 0
    while True:
        new_E, new_C = make_graph()
        D = ford_bellman(s, new_C)
        path = get_path(t, s)
        d_temp = h(path)
        if len(path) > 2:
            f += d_temp
            for v, w, c, _ in E:
                F[v][w] += sign(v, w, path) * d_temp
        else:
            break
    return F


def write_flow_to_file(flow_matrix, n, m, output_file):
    with open(output_file, 'w') as f:
        for i in range(1, n + 1):
            row = []
            for j in range(n + 1, n + m + 1):
                if flow_matrix[i][j] > 0:
                    row.append(str(flow_matrix[i][j]))
                else:
                    row.append("0")
            f.write(" ".join(row) + "\n")


if __name__ == '__main__':
    with open(input_file, 'r') as f:
        n, m = map(int, f.readline().split())  # Размеры матриц
        p = [list(map(int, f.readline().split())) for _ in range(n)]  # Матрица p
        q = [list(map(int, f.readline().split())) for _ in range(n)]  # Матрица q
        s_i = list(map(int, f.readline().split()))  # Стоимость истока -> источники
        v_i = list(map(int, f.readline().split()))  # Пропускная способность от истока -> источники

    # Процесс заполнения всех множеств и списков
    for i in range(1, n + m + 1):
        V.append(i)

    for i in range(1, n + 1):
        for j in range(n + 1, n + m + 1):
            E.append((i, j, 1e6, p[i - 1][j - n - 1] + q[i - 1][j - n - 1]))
    s = 0
    V.append(s)
    for i in range(1, n + 1):
        E.append((s, i, v_i[i - 1], -s_i[i - 1]))
    t = n + m + 1
    V.append(t)
    for j in range(n + 1, n + m + 1):
        E.append((j, t, 1e6, 0))

    F = {v: {u: 0 for u in V} for v in V}  # Матрица потоков
    C = {v: {u: 0 for u in V} for v in V}  # Матрица пропускных способностей
    R = {v: {u: 0 for u in V} for v in V}  # Матрица стоимости

    # Заполняем матрицы C и R и списки смежности
    for u, v, weight, cost in E:
        C[u][v] = weight
        R[u][v] = cost

    flow_matrix = min_cost_flow()  # применение двойственного алгоритма
    write_flow_to_file(flow_matrix, n, m, output_file)  # запись в файл
