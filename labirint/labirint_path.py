from collections import deque

# Поле лабиринта: 1 - стена, 0 - проходимая ячейка
p = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 1],
    [1, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1]
]

# Размерность поля
n = len(p)
m = len(p[0])

# Направления движения: вниз, вправо, вверх, влево
d = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def print_table():
    """Выводит таблицу маркировки."""
    print("Таблица p:")
    for row in p:
        print(" ".join(f"{cell:4}" for cell in row))
    print()


def mark_cells(v, w):
    """Алгоритм маркировки клеток лабиринта."""
    q2 = deque()
    q2.append(v)
    p[v[0]][v[1]] = 20
    k = 0
    while p[w[0]][w[1]] == 0 and len(q2) != 0:
        k += 1
        q1 = list(q2)
        q2.clear()
        for u in q1:
            for i in range(4):
                a = (u[0] + d[i][0], u[1] + d[i][1])
                while p[a[0]][a[1]] == 0 or (p[a[0]][a[1]] // 20) == k+1:
                    if p[a[0]][a[1]] == 0:
                        add = 20 * (k + 1) + 2 ** i
                        p[a[0]][a[1]] = add
                        q2.append(a)
                    else:
                        add = 2 ** i
                        p[a[0]][a[1]] += add
                    a = (a[0] + d[i][0], a[1] + d[i][1])
    print_table()


def has_direction_bit(i, x):
    """Проверяет, содержит ли число x бит, соответствующий направлению i."""
    return (x & (2 ** i)) != 0


def get_direction(x):
    """Извлекает направление движения из отметки x."""
    for i in range(4):
        if has_direction_bit(i, x):
            return i
    return -1


def find_path(v, w):
    """Находит обратный путь из точки w в точку v."""
    mark_cells(v, w)
    if p[w[0]][w[1]] != 0:
        stk = []
        stk.append(w)
        current = w
        while current != v:
            u = stk[-1]
            i = get_direction(p[u[0]][u[1]])
            a = (u[0] - d[i][0], u[1] - d[i][1])
            stk.append(a)
            current = a
        return stk[::-1]
    else:
        return None


# Начальная и конечная точки
start = (3, 1)
end = (1, 4)

# Поиск пути
path = find_path(start, end)

# Вывод результата
if path:
    print("Путь найден:")
    for step in path:
        print(step)
else:
    print("Путь не найден")
