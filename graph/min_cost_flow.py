# =============================================================================
# MinCostFlow (主双対法 + ダイクストラ法)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# 参考: https://github.com/atcoder/ac-library/blob/master/atcoder/mincostflow.hpp
# =============================================================================
#
# 使い方
#   mcf = MinCostFlow(n)
#   i = mcf.add_edge(u, v, cap, cost)     # 辺の番号 i を返す
#   flow, cost = mcf.flow(s, t, f)        # s -> t へ高々 f 流す (流せるだけ流して最小コスト)
#   flow, cost = mcf.flow(s, t, 10**18)   # 最小費用最大流
#   mcf.get_edge(i)                       # (from, to, cap, flow, cost)
# 負のコストの辺があってもよい (負閉路が無いこと)。
# 流量ちょうど f を要求するなら返り値の flow == f を確認する。
import heapq


class MinCostFlow:
    def __init__(self, n):
        self._n = n
        self._g = [[] for _ in range(n)]
        self._to = []
        self._cap = []
        self._cost = []
        self._has_negative = False

    def add_edge(self, u, v, cap, cost):
        assert 0 <= u < self._n and 0 <= v < self._n and cap >= 0
        m = len(self._to) // 2
        self._g[u].append(2 * m)
        self._g[v].append(2 * m + 1)
        self._to += [v, u]
        self._cap += [cap, 0]
        self._cost += [cost, -cost]
        if cost < 0:
            self._has_negative = True
        return m

    def get_edge(self, i):
        to, cap = self._to, self._cap
        return (to[2 * i + 1], to[2 * i], cap[2 * i] + cap[2 * i + 1], cap[2 * i + 1], self._cost[2 * i])

    def flow(self, s, t, f):
        n, g, to, cap, cost = self._n, self._g, self._to, self._cap, self._cost
        INF = float("inf")
        h = [0] * n  # ポテンシャル
        if self._has_negative:
            # Bellman-Ford で初期ポテンシャルを求める
            h = [INF] * n
            h[s] = 0
            for _ in range(n):
                updated = False
                for v in range(n):
                    if h[v] == INF:
                        continue
                    for e in g[v]:
                        if cap[e] > 0 and h[v] + cost[e] < h[to[e]]:
                            h[to[e]] = h[v] + cost[e]
                            updated = True
                if not updated:
                    break
            h = [0 if x == INF else x for x in h]

        total_flow = 0
        total_cost = 0
        while total_flow < f:
            dist = [INF] * n
            dist[s] = 0
            prev_e = [-1] * n
            pq = [(0, s)]
            while pq:
                d, v = heapq.heappop(pq)
                if dist[v] < d:
                    continue
                for e in g[v]:
                    if cap[e] <= 0:
                        continue
                    u = to[e]
                    nd = d + cost[e] + h[v] - h[u]
                    if nd < dist[u]:
                        dist[u] = nd
                        prev_e[u] = e
                        heapq.heappush(pq, (nd, u))
            if dist[t] == INF:
                break
            for v in range(n):
                if dist[v] < INF:
                    h[v] += dist[v]
            d = f - total_flow
            v = t
            while v != s:
                e = prev_e[v]
                d = min(d, cap[e])
                v = to[e ^ 1]
            v = t
            while v != s:
                e = prev_e[v]
                cap[e] -= d
                cap[e ^ 1] += d
                v = to[e ^ 1]
            total_flow += d
            total_cost += d * (h[t] - h[s])
        return total_flow, total_cost
