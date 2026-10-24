# =============================================================================
# DAG (トポロジカルソート)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   order = topological_sort(graph)
#     graph: 有向グラフの隣接リスト (0-indexed)。graph[v] = [行き先, ...]
#     トポロジカル順に並べた頂点のリストを返す。閉路があれば None を返す。
from collections import deque


def topological_sort(graph):
    n = len(graph)
    indeg = [0] * n
    for v in range(n):
        for u in graph[v]:
            indeg[u] += 1
    queue = deque(v for v in range(n) if indeg[v] == 0)
    order = []
    while queue:
        v = queue.popleft()
        order.append(v)
        for u in graph[v]:
            indeg[u] -= 1
            if indeg[u] == 0:
                queue.append(u)
    return order if len(order) == n else None
