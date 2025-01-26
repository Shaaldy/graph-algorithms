V = [0, 1, 2, 3, 4, 5, 6, 7, 8]
E = [(0, 1, 4), (1, 2, 8), (2, 3, 2), (2, 4, 3), (2, 5, 4), (3, 6, 5), (4, 6, 5), (5, 7, 2), (6, 8, 0), (7, 8, 0)]  # Рёбра (u, v, вес)


A = {v: {u: float('-inf') for u in V} for v in V}

prev = {v: [] for v in V}

for u, v, weight in E:
    A[u][v] = weight
    prev[v].append(u)

# Планирование
def planning():
    # Ранние сроки начала и завершения
    rnach = {v: 0 for v in V}  # Ранние сроки начала
    rvip = {v: 0 for v in V}  # Ранние сроки завершения

    # Вычисление ранних сроков
    for u in V:
        for v in prev[u]:
            rnach[u] = max(rnach[u], rvip[v])  # Ранний срок начала задачи u
            rvip[u] = rnach[u] + A[v][u]  # Ранний срок завершения задачи u

    return {"Ранние сроки начала": rnach, "Ранние сроки завершения": rvip}

result = planning()
print("Ранние сроки начала:")
for v in V:
    print(f"Задача {v}: {result['Ранние сроки начала'][v]}")

print("\nРанние сроки завершения:")
for v in V:
    print(f"Задача {v}: {result['Ранние сроки завершения'][v]}")
