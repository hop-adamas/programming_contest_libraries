# =============================================================================
# Warshall-Floyd 法 (全点対最短路)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方 (頂点は 0-indexed)
#   dist = warshall_floyd(n, edges, directed=False)   # O(n^3)
#     edges: [(u, v, cost), ...]  (負の辺があってもよいが、負閉路は扱わない)
#   dist[u][v]   # u から v への最短距離。到達不能なら INF。dist[v][v] = 0
#   多重辺は最小のコストが使われる。
#
# 経路復元が必要なら dist[u][v] == dist[u][w] + cost(w, v) を満たす w を辿る。

INF = float("inf")


def warshall_floyd(n, edges, directed=False):
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, c in edges:
        if c < dist[u][v]:
            dist[u][v] = c
        if not directed and c < dist[v][u]:
            dist[v][u] = c
    for k in range(n):
        dk = dist[k]
        for i in range(n):
            di = dist[i]
            dik = di[k]
            if dik == INF:
                continue
            for j in range(n):
                if dik + dk[j] < di[j]:
                    di[j] = dik + dk[j]
    return dist
