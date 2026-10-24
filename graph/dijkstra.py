# =============================================================================
# Dijkstra 法 (辺のコストが 0 以上の単一始点最短路)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方 (頂点は 0-indexed)
#   adj = build_graph(n, edges, directed=False)   # edges: [(u, v, cost), ...]
#   dist, prev = dijkstra(adj, s)                 # O((n + m) log n)
#   dist[t]                   # s から t への最短距離。到達不能なら INF
#   restore_path(prev, s, t)  # s から t への最短路の頂点列。到達不能なら []
# 辺のコストが全て 1 なら bfs.py、負の辺があるなら bellman_ford.py を使う。
import heapq

INF = float("inf")


def build_graph(n, edges, directed=False):
    adj = [[] for _ in range(n)]
    for u, v, c in edges:
        adj[u].append((v, c))
        if not directed:
            adj[v].append((u, c))
    return adj


def dijkstra(adj, s):
    dist = [INF] * len(adj)
    prev = [-1] * len(adj)
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, v = heapq.heappop(pq)
        if d > dist[v]:
            continue
        for u, c in adj[v]:
            nd = d + c
            if nd < dist[u]:
                dist[u] = nd
                prev[u] = v
                heapq.heappush(pq, (nd, u))
    return dist, prev


def restore_path(prev, s, t):
    path = [t]
    while path[-1] != s:
        if prev[path[-1]] == -1:
            return []  # s から t へ到達できない
        path.append(prev[path[-1]])
    return path[::-1]
