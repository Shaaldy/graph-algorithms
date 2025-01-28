# Инициализация массива родительских элементов и рангов
def init_union_find(n: int) -> tuple[list[int], list[int]]:
    parent = list(range(n))
    rank = [1] * n
    return parent, rank


# Найти корень элемента с путевым сжатием
def find(parent: list[int], u: int) -> int:
    if parent[u] != u:
        parent[u] = find(parent, parent[u])
    return parent[u]


# Объединить два множества по рангу
def union(parent: list[int], rank: list[int], u: int, v: int) -> None:
    root_u = find(parent, u)
    root_v = find(parent, v)

    if root_u != root_v:
        if rank[root_u] > rank[root_v]:
            parent[root_v] = root_u
        elif rank[root_u] < rank[root_v]:
            parent[root_u] = root_v
        else:
            parent[root_v] = root_u
            rank[root_u] += 1


def diff(point1: tuple[int], point2: tuple[int]) -> int:
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


# Построение словаря расстояний между всеми парами точек
def make_dict_diff(points: dict[int, tuple[int, int]], n: int) -> dict[tuple[int, int], int]:
    dct_dif = {}
    for i in range(n):
        for j in range(i + 1, n):
            dct_dif[(i, j)] = diff(points[i], points[j])
    dct_dif = sorted(dct_dif.items(), key=lambda x: x[1])
    return dict(dct_dif)


# Функция Краскала для построения минимального остовного дерева
def kraskal_func(points_diff: dict[tuple, int], n: int) -> tuple[list[list[int]], int]:
    parent, rank = init_union_find(n)  # Инициализация Union-Find
    lst = [[] for _ in range(n)]
    res = 0
    edge_count = 0

    for (u, v) in points_diff.keys():
        if find(parent, u) != find(parent, v):  # Если вершины принадлежат разным компонентам
            union(parent, rank, u, v)  # Объединяем компоненты
            lst[u].append(v + 1)
            lst[v].append(u + 1)
            res += points_diff[(u, v)]
            edge_count += 1

        if edge_count == n - 1:
            break

    lst = [sorted(ls) + [0] for ls in lst]

    return lst, res

# Для проверки того что вершины принадлежат разным компонентам использую СНМ(система непересекающихся отрезков)
# Построение же происходит по алгоритму Краскала
if __name__ == '__main__':
    with open('in.txt', mode='r', encoding='UTF-8') as rf:
        n = int(rf.readline())
        points = {}

        for i in range(n):
            point = [int(x) for x in rf.readline().split()]
            points[i] = point

        res1, res2 = kraskal_func(make_dict_diff(points, n), n)

    with open('out.txt', mode='w', encoding='UTF-8') as wf:
        wf.write("\n".join(" ".join(map(str, row)) for row in res1) + "\n")
        wf.write(f"{res2}\n")
