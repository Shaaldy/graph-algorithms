V = [1, 2, 3, 4]  # Вершины графа
E = [(1, 2, 1), (1, 4, -2), (2, 3, 2), (2, 1, 6), (3, 4, 3), (3, 1, -1), (4, 2, 7), (4, 1, 4)]  # Ребра (u, v, вес)

D = {v: {u: float('inf') for u in V} for v in V}  # Расстояния от источника
A = {v: {u: float('inf') for u in V} for v in V}  # Матрица смежности
n = len(V)
father = {v: None for v in V}  # Массив отцов
prev = {v: {u: None for u in V} for v in V}

for u, v, weight in E:
    A[u][v] = weight

for v in V:
    A[v][v] = 0

def floyd():
    for i in V:
        for j in V:
            D[i][j] = A[i][j]
            prev[i][j] = i
    for m in V:
        for i in V:
            for j in V:
                if D[i][j] > D[i][m] + D[m][j]:
                    D[i][j] = D[i][m] + D[m][j]
                    prev[i][j] = prev[m][j]

    return D, prev

result_D, result_prev = floyd()
print("Матрица расстояний:")
for i in V:
    print(f"{i}: {result_D[i]}")

print("\nМассив отцов:")
for i in V:
    print(f"{i}: {result_prev[i]}")