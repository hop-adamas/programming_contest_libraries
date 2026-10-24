# =============================================================================
# HopcroftKarp (二部グラフの最大マッチング, 非再帰)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   hk = HopcroftKarp(left_size, right_size)
#   hk.add_edge(u, v)       # 左の頂点 u (0..left_size-1) と右の頂点 v (0..right_size-1)
#   k = hk.max_matching()   # 最大マッチングの大きさ
#   hk.match_u[u]           # u と組になった右の頂点 (無ければ -1)
#   hk.match_v[v]           # v と組になった左の頂点 (無ければ -1)
#   hk.matching()           # [(u, v), ...]
# 計算量 O(m √n)
from collections import deque


class HopcroftKarp:
    def __init__(self, u_size, v_size):
        self.u_size = u_size
        self.v_size = v_size
        self.graph = [[] for _ in range(u_size)]
        self.match_u = [-1] * u_size
        self.match_v = [-1] * v_size

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def _bfs(self):
        dist = [-1] * self.u_size
        queue = deque()
        for u in range(self.u_size):
            if self.match_u[u] == -1:
                dist[u] = 0
                queue.append(u)
        found = False
        while queue:
            u = queue.popleft()
            for v in self.graph[u]:
                w = self.match_v[v]
                if w == -1:
                    found = True
                elif dist[w] == -1:
                    dist[w] = dist[u] + 1
                    queue.append(w)
        return found, dist

    def max_matching(self):
        g, match_u, match_v = self.graph, self.match_u, self.match_v
        matching = sum(1 for x in match_u if x != -1)
        while True:
            found, dist = self._bfs()
            if not found:
                break
            ptr = [0] * self.u_size
            for root in range(self.u_size):
                if match_u[root] != -1:
                    continue
                stack = [root]
                while stack:
                    u = stack[-1]
                    if ptr[u] < len(g[u]):
                        v = g[u][ptr[u]]
                        ptr[u] += 1
                        w = match_v[v]
                        if w == -1:
                            # 増加路が見つかった: スタック上の各頂点が最後に見た v に付け替える
                            for x in reversed(stack):
                                y = g[x][ptr[x] - 1]
                                match_u[x] = y
                                match_v[y] = x
                            matching += 1
                            break
                        if dist[w] == dist[u] + 1:
                            stack.append(w)
                    else:
                        dist[u] = -1  # 行き止まり
                        stack.pop()
        return matching

    def matching(self):
        return [(u, v) for u, v in enumerate(self.match_u) if v != -1]
