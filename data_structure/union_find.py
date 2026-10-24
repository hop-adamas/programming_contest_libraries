# =============================================================================
# UnionFind / WeightedUnionFind
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   uf = UnionFind(n)
#   uf.union(x, y)      # x, y を併合。併合したら True, 既に同じ集合なら False
#   uf.same(x, y)       # 同じ集合か
#   uf.leader(x)        # x の代表元
#   uf.size(x)          # x の属する集合の大きさ
#   uf.groups()         # 集合のリストのリスト
#
#   wuf = WeightedUnionFind(n)      # 重み付き UnionFind
#   wuf.union(a, b, d)              # value[b] - value[a] = d を追加。矛盾しなければ True, 矛盾すれば False
#   wuf.diff_of(a, b)               # value[b] - value[a]。不明 (別の集合) なら None
#   wuf.same(a, b), wuf.leader(a), wuf.size(a), wuf.groups()


class UnionFind:
    def __init__(self, n):
        # 負  : 根であることを示す。絶対値は木の要素数
        # 非負: 根でないことを示す。値は親を示す
        self.n = n
        self.table = [-1] * n

    def _root(self, x):
        stack = []
        tbl = self.table
        while tbl[x] >= 0:
            stack.append(x)
            x = tbl[x]
        for y in stack:
            tbl[y] = x
        return x

    leader = _root  # 代表元

    def same(self, x, y):
        return self._root(x) == self._root(y)

    def union(self, x, y):
        r1 = self._root(x)
        r2 = self._root(y)
        if r1 == r2:
            return False
        if self.table[r1] > self.table[r2]:
            r1, r2 = r2, r1
        self.table[r1] += self.table[r2]
        self.table[r2] = r1
        return True

    def size(self, x):
        return -self.table[self._root(x)]

    def groups(self):
        G = [[] for _ in range(self.n)]
        for i in range(self.n):
            G[self._root(i)].append(i)
        return [g for g in G if g]


class WeightedUnionFind:
    """各頂点に値 value[x] があるとして、「value[b] - value[a] = d」という情報だけを管理する"""

    def __init__(self, n):
        self.n = n
        self.parent = [-1] * n  # 負: 根 (絶対値は集合の大きさ), 非負: 親
        self.diff = [0] * n  # value[x] - value[parent[x]] (経路圧縮後は根との差)

    def leader(self, x):
        path = []
        while self.parent[x] >= 0:
            path.append(x)
            x = self.parent[x]
        acc = 0
        for y in reversed(path):  # 根に近い方から順に、根との差へ付け替える
            acc += self.diff[y]
            self.diff[y] = acc
            self.parent[y] = x
        return x

    def same(self, a, b):
        return self.leader(a) == self.leader(b)

    def diff_of(self, a, b):
        """value[b] - value[a]。異なる集合なら None"""
        if self.leader(a) != self.leader(b):
            return None
        return self.diff[b] - self.diff[a]

    def union(self, a, b, d):
        """
        value[b] - value[a] = d を追加する。
        新たに併合した、または既知の情報と矛盾しなければ True。矛盾すれば False。
        """
        ra, rb = self.leader(a), self.leader(b)
        if ra == rb:
            return self.diff[b] - self.diff[a] == d
        d_roots = d + self.diff[a] - self.diff[b]  # value[rb] - value[ra]
        if self.parent[ra] > self.parent[rb]:  # rb 側の方が大きい
            ra, rb, d_roots = rb, ra, -d_roots
        # rb を ra の下に付ける (value[rb] - value[ra] = d_roots)
        self.parent[ra] += self.parent[rb]
        self.parent[rb] = ra
        self.diff[rb] = d_roots
        return True

    def size(self, x):
        return -self.parent[self.leader(x)]

    def groups(self):
        res = {}
        for i in range(self.n):
            res.setdefault(self.leader(i), []).append(i)
        return list(res.values())
