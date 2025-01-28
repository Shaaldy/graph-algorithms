#include <iostream>
#include <fstream>
#include <vector>
#include <queue>
#include <cstring>

using namespace std;

const int INF = 1e9;
const int MAXN = 500;

int k, l;
vector<int> adj[MAXN];
int capacity[MAXN][MAXN];
int parent[MAXN];

bool bfs(int s, int t, int n) {
    memset(parent, -1, sizeof(parent));
    queue<int> q;
    q.push(s);
    parent[s] = s;

    while (!q.empty()) {
        int u = q.front();
        q.pop();

        for (int v = 0; v < n; ++v) {
            if (parent[v] == -1 && capacity[u][v] > 0) {
                parent[v] = u;
                if (v == t) return true;
                q.push(v);
            }
        }
    }
    return false;
}

int fordFulkerson(int s, int t, int n) {
    int maxFlow = 0;

    while (bfs(s, t, n)) {
        // Определяем минимальную пропускную способность на пути
        int flow = INF;
        for (int v = t; v != s; v = parent[v]) {
            int u = parent[v];
            flow = min(flow, capacity[u][v]);
        }

        // Обновляем остаточную сеть
        for (int v = t; v != s; v = parent[v]) {
            int u = parent[v];
            capacity[u][v] -= flow;
            capacity[v][u] += flow;
        }

        maxFlow += flow;
    }
    return maxFlow;
}

int main() {
    ifstream fin("in.txt"); // Открытие файла для чтения
    ofstream fout("out.txt"); // Открытие файла для записи

    if (!fin.is_open() || !fout.is_open()) {
        cerr << "Ошибка при открытии файла!" << endl;
        return 1;
    }

    fin >> k >> l;

    // Чтение списка смежности
    int s = 0, t = k + l + 1; // Исток и сток
    int n = t + 1; // Общее количество вершин

    memset(capacity, 0, sizeof(capacity));

    for (int i = 1; i <= k; ++i) {
        while (true) {
            int y; fin >> y;
            if (y == 0) break;

            adj[i].push_back(k + y); // Смежность X -> Y
            capacity[i][k + y] = 1; // Пропускная способность 1
        }
    }

    // Рёбра от истока к X и от Y к стоку
    for (int i = 1; i <= k; ++i) {
        adj[s].push_back(i);
        capacity[s][i] = 1;
    }

    for (int i = 1; i <= l; ++i) {
        adj[k + i].push_back(t);
        capacity[k + i][t] = 1;
    }

    // Нахождение максимального потока
    fordFulkerson(s, t, n);

    // Восстановление паросочетания
    vector<int> pairX(k + 1, 0);

    for (int i = 1; i <= k; ++i) {
        for (int j : adj[i]) {
            if (j > k && j <= k + l && capacity[j][i] > 0) {
                pairX[i] = j - k;
            }
        }
    }

    // Вывод результата в файл
    for (int i = 1; i <= k; ++i) {
        fout << pairX[i] << " ";
    }
    fout << endl;

    fin.close();
    fout.close();

    return 0;
}
