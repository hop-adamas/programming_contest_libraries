# =============================================================================
# Lowlink (橋・関節点, 非再帰)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   ll = Lowlink(n)
#   ll.add_edge(u, v)      # 無向辺 (多重辺・自己ループ可)
#   ll.build()
#   ll.bridges             # 橋のリスト [(u, v), ...] (u < v, ソート済み)
#   ll.articulation_points # 関節点のリスト (ソート済み)
#   ll.ord[v], ll.low[v]   # DFS 順序 / lowlink
# 計算量 O(n + m)


class Lowlink:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]  # (行き先, 辺番号)
        self.m = 0
        self.ord = [-1] * n
        self.low = [-1] * n
        self.bridges = []
        self.articulation_points = []

    def add_edge(self, u, v):
        self.graph[u].append((v, self.m))
        self.graph[v].append((u, self.m))
        self.m += 1

    def build(self):
        n, g = self.n, self.graph
        ord_, low = self.ord, self.low
        ptr = [0] * n
        parent_edge = [-1] * n
        is_art = [False] * n
        timer = 0
        bridges = []
        for root in range(n):
            if ord_[root] != -1:
                continue
            ord_[root] = low[root] = timer
            timer += 1
            root_children = 0
            call = [root]
            while call:
                v = call[-1]
                if ptr[v] < len(g[v]):
                    to, eid = g[v][ptr[v]]
                    ptr[v] += 1
                    if eid == parent_edge[v]:
                        continue
                    if ord_[to] == -1:
                        parent_edge[to] = eid
                        ord_[to] = low[to] = timer
                        timer += 1
                        call.append(to)
                    elif ord_[to] < low[v]:
                        low[v] = ord_[to]
                else:
                    call.pop()
                    if not call:
                        break
                    p = call[-1]
                    if low[v] < low[p]:
                        low[p] = low[v]
                    if low[v] > ord_[p]:
                        bridges.append((min(p, v), max(p, v)))
                    if p == root:
                        root_children += 1
                    elif low[v] >= ord_[p]:
                        is_art[p] = True
            if root_children > 1:
                is_art[root] = True
        bridges.sort()
        self.bridges = bridges
        self.articulation_points = [v for v in range(n) if is_art[v]]
