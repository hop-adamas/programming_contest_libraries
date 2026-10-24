# =============================================================================
# MaxFlow (Dinic 法, 非再帰)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# 参考: https://github.com/atcoder/ac-library/blob/master/atcoder/maxflow.hpp
#       https://ikatakos.com/pot/programming_algorithm/graph_theory/maximum_flow
# =============================================================================
#
# 使い方
#   mf = MaxFlow(n)
#   i = mf.add_edge(u, v, cap)       # 辺の番号 i を返す
#   f = mf.flow(s, t)                # s -> t の最大流量 (flow_limit を渡すとそこで打ち切り)
#   mf.get_edge(i)                   # (from, to, cap, flow)
#   mf.edges()                       # 全辺の get_edge
#   mf.min_cut(s)                    # flow 後に呼ぶ。s 側に残る頂点なら True のリスト
# 計算量 O(n^2 m) (実際はかなり速い)
from collections import deque


class MaxFlow:
    def __init__(self, n=0):
        self._n = n
        self._g = [[] for _ in range(n)]
        self._to = []
        self._cap = []  # 残余容量。辺 i は 2i (順方向) と 2i+1 (逆方向)

    def add_edge(self, u, v, cap):
        assert 0 <= u < self._n and 0 <= v < self._n and 0 <= cap
        m = len(self._to) // 2
        self._g[u].append(2 * m)
        self._g[v].append(2 * m + 1)
        self._to += [v, u]
        self._cap += [cap, 0]
        return m

    def get_edge(self, i):
        to, cap = self._to, self._cap
        return (to[2 * i + 1], to[2 * i], cap[2 * i] + cap[2 * i + 1], cap[2 * i + 1])

    def edges(self):
        return [self.get_edge(i) for i in range(len(self._to) // 2)]

    def change_edge(self, i, new_cap, new_flow):
        assert 0 <= new_flow <= new_cap
        self._cap[2 * i] = new_cap - new_flow
        self._cap[2 * i + 1] = new_flow

    def _bfs(self, s):
        level = [-1] * self._n
        level[s] = 0
        q = deque([s])
        g, to, cap = self._g, self._to, self._cap
        while q:
            v = q.popleft()
            for e in g[v]:
                if cap[e] > 0 and level[to[e]] < 0:
                    level[to[e]] = level[v] + 1
                    q.append(to[e])
        return level

    def flow(self, s, t, flow_limit=float("inf")):
        assert s != t
        g, to, cap = self._g, self._to, self._cap
        total = 0
        while total < flow_limit:
            level = self._bfs(s)
            if level[t] < 0:
                break
            it = [0] * self._n
            while total < flow_limit:
                # level graph 上で s -> t のパスを探す (current arc 方式)
                path = []
                v = s
                while v != t:
                    gv = g[v]
                    while it[v] < len(gv):
                        e = gv[it[v]]
                        if cap[e] > 0 and level[to[e]] == level[v] + 1:
                            break
                        it[v] += 1
                    if it[v] < len(gv):
                        e = gv[it[v]]
                        path.append(e)
                        v = to[e]
                    elif v == s:
                        break
                    else:
                        level[v] = -1  # 行き止まり
                        e = path.pop()
                        v = to[e ^ 1]
                        it[v] += 1
                if v != t:
                    break
                f = min(min(cap[e] for e in path), flow_limit - total)
                for e in path:
                    cap[e] -= f
                    cap[e ^ 1] += f
                total += f
        return total

    def min_cut(self, s):
        visited = [False] * self._n
        visited[s] = True
        stack = [s]
        g, to, cap = self._g, self._to, self._cap
        while stack:
            v = stack.pop()
            for e in g[v]:
                if cap[e] > 0 and not visited[to[e]]:
                    visited[to[e]] = True
                    stack.append(to[e])
        return visited
