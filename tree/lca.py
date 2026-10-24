# =============================================================================
# LCA (ダブリングによる最小共通祖先)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方 (頂点は 0-indexed)
#   lca = LCA(adj, root=0)       # adj[v] = [隣接頂点, ...]。前計算 O(n log n)
#   lca.lca(u, v)                # 最小共通祖先            O(log n)
#   lca.dist(u, v)               # u-v 間の辺の本数
#   lca.kth_ancestor(v, k)       # v の k 個上の祖先 (根より上は -1)
#   lca.on_path(u, v, a)         # a が u-v 間の最短路上にあるか
#   lca.depth[v], lca.parent[v]  # 深さ / 親 (根は -1)
# 重み付き距離は、根からの距離 dist_from_root を別に持って
#   dist_from_root[u] + dist_from_root[v] - 2 * dist_from_root[lca.lca(u, v)]  で求める。
# HLD も使いたいときは tree.py の Tree を使う。


class LCA:
    def __init__(self, adj, root=0):
        n = len(adj)
        self.n = n
        self.parent = [-1] * n
        self.depth = [0] * n
        stack = [root]
        while stack:
            v = stack.pop()
            for u in adj[v]:
                if u != self.parent[v]:
                    self.parent[u] = v
                    self.depth[u] = self.depth[v] + 1
                    stack.append(u)
        self.log = max(1, max(self.depth).bit_length())
        # up[k][v] = v の 2^k 個上の祖先 (根を越えたら根の親に当たる番兵 n)
        up0 = [p if p >= 0 else n for p in self.parent] + [n]
        self.up = [up0]
        for _ in range(self.log - 1):
            prev = self.up[-1]
            self.up.append([prev[prev[v]] for v in range(n + 1)])

    def kth_ancestor(self, v, k):
        if k > self.depth[v]:
            return -1
        for i in range(k.bit_length()):
            if k >> i & 1:
                v = self.up[i][v]
        return v

    def lca(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        u = self.kth_ancestor(u, self.depth[u] - self.depth[v])
        if u == v:
            return u
        for i in range(self.log - 1, -1, -1):
            if self.up[i][u] != self.up[i][v]:
                u = self.up[i][u]
                v = self.up[i][v]
        return self.up[0][u]

    def dist(self, u, v):
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]

    def on_path(self, u, v, a):
        return self.dist(u, a) + self.dist(a, v) == self.dist(u, v)
