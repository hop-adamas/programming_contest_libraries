# =============================================================================
# Tree (木: 親・深さ・部分木サイズ / HLD / LCA / 距離 / パス / 直径 / 全方位木 DP)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方 (頂点は 0-indexed)
#   t = Tree(n)
#   i = t.add_edge(u, v)       # 無向辺を追加 (辺の番号 i = 0, 1, ... を返す)
#   t.build(root=0)            # 根を決めて前計算 (O(n))。以下は build の後に使う
#
#   t.parent[v], t.depth[v], t.size[v]    # 親 (根は -1) / 深さ / 部分木の大きさ
#   t.order                               # 根が先頭の DFS 前順 (親は子より先)
#   t.tin[v]                              # HLD の番号。部分木は連続し、重い子が直後に並ぶ
#   t.lca(u, v), t.dist(u, v)             # LCA / 距離 (辺の本数)         O(log n)
#   t.path(u, v)                          # u から v への頂点列
#   t.subtree_range(v)                    # (tin[v], tin[v] + size[v]) 部分木に対応する半開区間
#   t.path_ranges(u, v, edge=False)       # u-v パスを覆う半開区間 (tin 上) のリスト O(log n)
#                                         #   edge=True なら「頂点 v ↔ 親との辺」を v に載せた辺クエリ用
#                                         #   (LCA は含まない)。可換な演算のときに使う
#   t.edge_vertex(i)                      # 辺 i の子側の頂点 (辺クエリでその辺を載せる頂点)
#   t.diameter()                          # (直径の長さ, 端点 a, 端点 b)
#   t.rerooting(e, merge, f)              # 全方位木 DP (下記)
#
# 全方位木 DP:  res = t.rerooting(e, merge, f)
#   頂点 v の値 res[v] は、v に隣接する各頂点 u から届く「メッセージ」を merge (可換, 単位元 e) で
#   まとめたもの。u から v へのメッセージは f(x, u, v) で、x は「v を親とみなしたときの u の値」
#   (= u に隣接する v 以外の頂点からのメッセージを merge したもの)。
#   例: 各頂点から最も遠い頂点までの距離
#       res = t.rerooting(0, max, lambda x, u, v: x + 1)
from collections import deque


class Tree:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.edges = []

    def add_edge(self, u, v):
        self.adj[u].append(v)
        self.adj[v].append(u)
        self.edges.append((u, v))
        return len(self.edges) - 1

    def build(self, root=0):
        n, adj = self.n, self.adj
        parent = [-1] * n
        order = []
        stack = [root]
        while stack:
            v = stack.pop()
            order.append(v)
            for u in adj[v]:
                if u != parent[v]:
                    parent[u] = v
                    stack.append(u)
        depth = [0] * n
        for v in order[1:]:
            depth[v] = depth[parent[v]] + 1
        size = [1] * n
        heavy = [-1] * n
        for v in reversed(order):
            p = parent[v]
            if p >= 0:
                size[p] += size[v]
        for v in order:
            best = 0
            for u in adj[v]:
                if u != parent[v] and size[u] > best:
                    best = size[u]
                    heavy[v] = u
        # 重い子を先に訪れる前順で番号を振る (部分木が連続し、重い鎖も連続する)
        tin = [0] * n
        head = [root] * n
        stack = [root]
        cnt = 0
        while stack:
            v = stack.pop()
            tin[v] = cnt
            cnt += 1
            for u in adj[v]:
                if u != parent[v] and u != heavy[v]:
                    head[u] = u
                    stack.append(u)
            if heavy[v] != -1:
                head[heavy[v]] = head[v]
                stack.append(heavy[v])
        self.root = root
        self.parent, self.order, self.depth, self.size = parent, order, depth, size
        self.heavy, self.head, self.tin = heavy, head, tin
        self.vertex_at = [0] * n  # tin の逆写像
        for v in range(n):
            self.vertex_at[tin[v]] = v

    def lca(self, u, v):
        head, parent, tin = self.head, self.parent, self.tin
        while head[u] != head[v]:
            if tin[head[u]] < tin[head[v]]:
                u, v = v, u
            u = parent[head[u]]
        return u if self.depth[u] < self.depth[v] else v

    def dist(self, u, v):
        return self.depth[u] + self.depth[v] - 2 * self.depth[self.lca(u, v)]

    def path(self, u, v):
        w = self.lca(u, v)
        left = []
        while u != w:
            left.append(u)
            u = self.parent[u]
        right = []
        while v != w:
            right.append(v)
            v = self.parent[v]
        return left + [w] + right[::-1]

    def subtree_range(self, v):
        return self.tin[v], self.tin[v] + self.size[v]

    def edge_vertex(self, i):
        u, v = self.edges[i]
        return v if self.parent[v] == u else u

    def path_ranges(self, u, v, edge=False):
        head, parent, tin, depth = self.head, self.parent, self.tin, self.depth
        res = []
        while head[u] != head[v]:
            if tin[head[u]] < tin[head[v]]:
                u, v = v, u
            res.append((tin[head[u]], tin[u] + 1))
            u = parent[head[u]]
        if tin[u] > tin[v]:
            u, v = v, u
        lo = tin[u] + 1 if edge else tin[u]
        if lo < tin[v] + 1:
            res.append((lo, tin[v] + 1))
        return res

    def _farthest(self, s):
        dist = [-1] * self.n
        dist[s] = 0
        q = deque([s])
        last = s
        while q:
            v = q.popleft()
            last = v
            for u in self.adj[v]:
                if dist[u] < 0:
                    dist[u] = dist[v] + 1
                    q.append(u)
        return last, dist[last]

    def diameter(self):
        a, _ = self._farthest(0)
        b, d = self._farthest(a)
        return d, a, b

    def rerooting(self, e, merge, f):
        n, parent, adj = self.n, self.parent, self.adj
        down = [e] * n  # 子の部分木だけから届くメッセージの合成
        for v in reversed(self.order):
            acc = e
            for u in adj[v]:
                if u != parent[v]:
                    acc = merge(acc, f(down[u], u, v))
            down[v] = acc
        up = [e] * n  # 親から v に届くメッセージ (根は e)
        for v in self.order:
            kids = [u for u in adj[v] if u != parent[v]]
            msgs = [f(down[u], u, v) for u in kids]
            suffix = [e] * (len(kids) + 1)
            for i in range(len(kids) - 1, -1, -1):
                suffix[i] = merge(msgs[i], suffix[i + 1])
            prefix = up[v]
            for i, u in enumerate(kids):
                up[u] = f(merge(prefix, suffix[i + 1]), v, u)
                prefix = merge(prefix, msgs[i])
        return [merge(up[v], down[v]) for v in range(n)]
