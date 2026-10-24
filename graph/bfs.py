# =============================================================================
# BFS / 0-1 BFS (辺のコストが 1、または 0 か 1 の最短路)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方 (頂点は 0-indexed)
#   adj = build_graph(n, edges, directed=False)   # edges: [(u, v)] か [(u, v, cost)]
#   dist, prev = bfs(adj, s)                      # 全ての辺のコストを 1 とみなす       O(n + m)
#   dist, prev = bfs01(adj, s)                    # コストが 0 か 1 の辺だけのとき       O(n + m)
#   dist[t]            # s から t への最短距離。到達不能なら INF
#   restore_path(prev, s, t)   # s から t への最短路の頂点列。到達不能なら []
from collections import deque

INF = float("inf")


def build_graph(n, edges, directed=False):
    adj = [[] for _ in range(n)]
    for e in edges:
        u, v = e[0], e[1]
        c = e[2] if len(e) > 2 else 1
        adj[u].append((v, c))
        if not directed:
            adj[v].append((u, c))
    return adj


def bfs(adj, s):
    dist = [INF] * len(adj)
    prev = [-1] * len(adj)
    dist[s] = 0
    q = deque([s])
    while q:
        v = q.popleft()
        for u, _ in adj[v]:
            if dist[u] == INF:
                dist[u] = dist[v] + 1
                prev[u] = v
                q.append(u)
    return dist, prev


def bfs01(adj, s):
    dist = [INF] * len(adj)
    prev = [-1] * len(adj)
    dist[s] = 0
    q = deque([s])
    while q:
        v = q.popleft()
        for u, c in adj[v]:
            if dist[v] + c < dist[u]:
                dist[u] = dist[v] + c
                prev[u] = v
                if c:
                    q.append(u)
                else:
                    q.appendleft(u)
    return dist, prev


def restore_path(prev, s, t):
    path = [t]
    while path[-1] != s:
        if prev[path[-1]] == -1:
            return []  # s から t へ到達できない
        path.append(prev[path[-1]])
    return path[::-1]
