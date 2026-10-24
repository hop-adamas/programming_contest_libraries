# =============================================================================
# オイラー路 (一筆書き, Hierholzer 法, 非再帰)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方 (頂点は 0-indexed)
#   et = EulerianTrail(n, directed=False)
#   i = et.add_edge(u, v)     # 辺を追加。辺の番号 i = 0, 1, ... を返す (自己ループ・多重辺可)
#   res = et.build()          # 全ての辺をちょうど 1 回通る路 (閉路でもよい) があれば (頂点列, 辺番号列)、無ければ None
#                             #   頂点列の長さは m + 1、辺番号列の長さは m。辺が 0 本なら ([], [])。O(n + m)
#   頂点列 vs と辺番号列 es について、辺 es[i] は vs[i] と vs[i + 1] を結ぶ。


class EulerianTrail:
    def __init__(self, n, directed=False):
        self.n = n
        self.directed = directed
        self.adj = [[] for _ in range(n)]  # (行き先, 辺番号)
        self.m = 0
        self.deg = [0] * n  # 有向: 出次数 - 入次数 / 無向: 次数

    def add_edge(self, u, v):
        self.adj[u].append((v, self.m))
        if self.directed:
            self.deg[u] += 1
            self.deg[v] -= 1
        else:
            self.adj[v].append((u, self.m))
            self.deg[u] += 1
            self.deg[v] += 1
        self.m += 1
        return self.m - 1

    def _start(self):
        deg = self.deg
        if self.directed:
            starts = [v for v in range(self.n) if deg[v] == 1]
            ends = [v for v in range(self.n) if deg[v] == -1]
            if any(abs(d) > 1 for d in deg) or len(starts) != len(ends) or len(starts) > 1:
                return None
            if starts:
                return starts[0]
        else:
            odd = [v for v in range(self.n) if deg[v] % 2]
            if len(odd) not in (0, 2):
                return None
            if odd:
                return odd[0]
        for v in range(self.n):
            if self.adj[v]:
                return v
        return 0

    def build(self):
        if self.m == 0:
            return [], []
        start = self._start()
        if start is None:
            return None
        ptr = [0] * self.n
        used = [False] * self.m
        vs = []
        es = []
        stack = [(start, -1)]  # (頂点, そこへ来た辺)
        while stack:
            v, e = stack[-1]
            adj_v = self.adj[v]
            while ptr[v] < len(adj_v) and used[adj_v[ptr[v]][1]]:
                ptr[v] += 1
            if ptr[v] < len(adj_v):
                to, eid = adj_v[ptr[v]]
                ptr[v] += 1
                used[eid] = True
                stack.append((to, eid))
            else:
                stack.pop()
                vs.append(v)
                if e != -1:
                    es.append(e)
        if len(es) != self.m:
            return None  # 辺を持つ頂点が連結でない
        return vs[::-1], es[::-1]
