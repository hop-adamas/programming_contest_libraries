# =============================================================================
# Bellman-Ford 法 (負の辺を含んでよい単一始点最短路, 負閉路の検出)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方 (頂点は 0-indexed)
#   dist, prev, has_negative_cycle = bellman_ford(n, edges, s, directed=True)   # O(nm)
#     edges: [(u, v, cost), ...]。directed=False なら無向辺 (負の辺があると負閉路になる)
#   dist[t]                   # s から t への最短距離。到達不能なら INF
#   has_negative_cycle        # s から到達できる負閉路があるか
#     あるとき、負閉路の影響を受ける頂点の dist は -INF (その頂点には最短路が存在しない)
#   restore_path(prev, s, t)  # s から t への最短路の頂点列。到達不能なら []
#                             #   負閉路がない (has_negative_cycle == False) ときだけ使う

INF = float("inf")


def bellman_ford(n, edges, s, directed=True):
    arcs = list(edges)
    if not directed:
        arcs += [(v, u, c) for u, v, c in edges]
    dist = [INF] * n
    prev = [-1] * n
    dist[s] = 0
    for _ in range(n):
        updated = False
        for u, v, c in arcs:
            if dist[u] != INF and dist[u] + c < dist[v]:
                dist[v] = dist[u] + c
                prev[v] = u
                updated = True
        if not updated:
            return dist, prev, False
    # 更新が止まらない: 負閉路から到達できる頂点を -INF にする
    for _ in range(n):
        for u, v, c in arcs:
            if dist[u] == -INF:
                dist[v] = -INF
            elif dist[u] != INF and dist[u] + c < dist[v]:
                dist[v] = -INF
    return dist, prev, True


def restore_path(prev, s, t):
    path = [t]
    while path[-1] != s:
        if prev[path[-1]] == -1:
            return []  # s から t へ到達できない
        path.append(prev[path[-1]])
    return path[::-1]
