# =============================================================================
# SccGraph (強連結成分分解, 非再帰 Tarjan)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# 参考: https://github.com/atcoder/ac-library/blob/master/atcoder/internal_scc.hpp
# =============================================================================
#
# 使い方
#   g = SccGraph(n)
#   g.add_edge(s, t)       # 有向辺 s -> t (0-indexed)
#   groups = g.scc()       # 強連結成分のリスト。トポロジカル順 (辺は前の成分から後ろの成分へ向かう)
#   group_num, ids = g.scc_ids()   # ids[v] = v の属する成分の番号 (scc() の添字と対応)
# 計算量 O(n + m)


class SccGraph:
    def __init__(self, n=0):
        self._n = n
        self._edges = []

    def __len__(self):
        return self._n

    def add_edge(self, s, t):
        assert 0 <= s < self._n and 0 <= t < self._n
        self._edges.append((s, t))

    def scc_ids(self):
        n = self._n
        g = [[] for _ in range(n)]
        for s, t in self._edges:
            g[s].append(t)

        order = [-1] * n
        low = [0] * n
        ids = [-1] * n
        ptr = [0] * n
        stack = []
        now = 0
        group_num = 0
        for root in range(n):
            if order[root] != -1:
                continue
            order[root] = low[root] = now
            now += 1
            stack.append(root)
            call = [root]
            while call:
                v = call[-1]
                if ptr[v] < len(g[v]):
                    t = g[v][ptr[v]]
                    ptr[v] += 1
                    if order[t] == -1:
                        order[t] = low[t] = now
                        now += 1
                        stack.append(t)
                        call.append(t)
                    elif order[t] < low[v]:
                        low[v] = order[t]
                else:
                    call.pop()
                    if call and low[v] < low[call[-1]]:
                        low[call[-1]] = low[v]
                    if low[v] == order[v]:
                        while True:
                            u = stack.pop()
                            order[u] = n  # 確定済みの印 (以後 low を下げない)
                            ids[u] = group_num
                            if u == v:
                                break
                        group_num += 1
        for i in range(n):
            ids[i] = group_num - 1 - ids[i]
        return group_num, ids

    def scc(self):
        group_num, ids = self.scc_ids()
        groups = [[] for _ in range(group_num)]
        for v in range(self._n):
            groups[ids[v]].append(v)
        return groups
