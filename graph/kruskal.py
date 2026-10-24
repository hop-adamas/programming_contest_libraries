# =============================================================================
# Kruskal 法 (最小全域木)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   cost, used = kruskal(n, edges)
#     n: 頂点数, edges: (u, v, cost) のリスト (0-indexed)
#     cost: 最小全域森のコスト総和, used: 採用した辺の edges 内インデックス
#     グラフが非連結なら最小全域森になる (len(used) == n - 1 で連結かを判定)
#
# 単体でコピーして使えるよう、UnionFind をこのファイル内に持つ。


def kruskal(n, edges):
    parent = [-1] * n

    def find(x):
        r = x
        while parent[r] >= 0:
            r = parent[r]
        while parent[x] >= 0:
            parent[x], x = r, parent[x]
        return r

    total = 0
    used = []
    for i in sorted(range(len(edges)), key=lambda i: edges[i][2]):
        u, v, c = edges[i]
        ru, rv = find(u), find(v)
        if ru == rv:
            continue
        if parent[ru] > parent[rv]:
            ru, rv = rv, ru
        parent[ru] += parent[rv]
        parent[rv] = ru
        total += c
        used.append(i)
    return total, used
