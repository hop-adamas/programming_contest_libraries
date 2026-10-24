# =============================================================================
# LazySegmentTree (遅延評価セグメント木, 非再帰)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# 参考: https://github.com/atcoder/ac-library/blob/master/atcoder/lazysegtree.hpp (CC0)
# =============================================================================
#
# 使い方
#   st = LazySegmentTree(op, e, mapping, composition, id_, n_or_list)
#     op(x, y)           : 値どうしの結合的な演算,  e: その単位元
#     mapping(f, x)      : 作用 f を値 x に適用した結果
#     composition(f, g)  : 作用 g の後に f を行うのと同じ作用 (f が後)
#     id_                : 恒等作用 (mapping(id_, x) = x)
#     n_or_list          : 要素数 n (全て e) か、初期値のリスト
#   st.set(p, x)         # a[p] = x                              O(log n)
#   st.get(p)            # a[p]                                  O(log n)
#   st.prod(l, r)        # op(a[l], ..., a[r-1])  (半開区間)        O(log n)
#   st.all_prod()        # 全体の積                               O(1)
#   st.apply(l, r, f)    # l <= i < r の a[i] に作用 f を適用          O(log n)
#   st.apply_point(p, f) # a[p] に作用 f を適用
#   st.max_right(l, g)   # g(op(a[l..r-1])) = True となる最大の r  (g(e) は True, g は単調)
#   st.min_left(r, g)    # g(op(a[l..r-1])) = True となる最小の l
#   st.to_list()         # 全要素のリスト
#
# 例 1: 区間加算・区間最小値
#   op = min; e = 10**18
#   mapping = lambda f, x: x + f; composition = lambda f, g: f + g; id_ = 0
#
# 例 2: 区間代入・区間最小値  (id_ は代入値として現れない値、None など)
#   op = min; e = 10**18
#   mapping = lambda f, x: x if f is None else f
#   composition = lambda f, g: g if f is None else f; id_ = None
#
# 例 3: 区間加算・区間和  (値を (和, 要素数) のペアで持つ。初期値は (a[i], 1))
#   op = lambda x, y: (x[0] + y[0], x[1] + y[1]); e = (0, 0)
#   mapping = lambda f, x: (x[0] + f * x[1], x[1]); composition = lambda f, g: f + g; id_ = 0


class LazySegmentTree:
    def __init__(self, op, e, mapping, composition, id_, v):
        self._op = op
        self._e = e
        self._mapping = mapping
        self._composition = composition
        self._id = id_
        if isinstance(v, int):
            v = [e] * v
        self._n = len(v)
        self._log = (self._n - 1).bit_length()
        self._size = 1 << self._log
        self._d = [e] * (2 * self._size)
        self._lz = [id_] * self._size
        for i in range(self._n):
            self._d[self._size + i] = v[i]
        for i in range(self._size - 1, 0, -1):
            self._update(i)

    def _update(self, k):
        self._d[k] = self._op(self._d[2 * k], self._d[2 * k + 1])

    def _apply_node(self, k, f):
        self._d[k] = self._mapping(f, self._d[k])
        if k < self._size:
            self._lz[k] = self._composition(f, self._lz[k])

    def _push(self, k):
        f = self._lz[k]
        self._apply_node(2 * k, f)
        self._apply_node(2 * k + 1, f)
        self._lz[k] = self._id

    def set(self, p, x):
        p += self._size
        for i in range(self._log, 0, -1):
            self._push(p >> i)
        self._d[p] = x
        for i in range(1, self._log + 1):
            self._update(p >> i)

    def get(self, p):
        p += self._size
        for i in range(self._log, 0, -1):
            self._push(p >> i)
        return self._d[p]

    def prod(self, l, r):
        if l >= r:
            return self._e
        l += self._size
        r += self._size
        for i in range(self._log, 0, -1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push((r - 1) >> i)
        sml = smr = self._e
        while l < r:
            if l & 1:
                sml = self._op(sml, self._d[l])
                l += 1
            if r & 1:
                r -= 1
                smr = self._op(self._d[r], smr)
            l >>= 1
            r >>= 1
        return self._op(sml, smr)

    def all_prod(self):
        return self._d[1]

    def apply_point(self, p, f):
        p += self._size
        for i in range(self._log, 0, -1):
            self._push(p >> i)
        self._d[p] = self._mapping(f, self._d[p])
        for i in range(1, self._log + 1):
            self._update(p >> i)

    def apply(self, l, r, f):
        if l >= r:
            return
        l += self._size
        r += self._size
        for i in range(self._log, 0, -1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push((r - 1) >> i)
        l2, r2 = l, r
        while l < r:
            if l & 1:
                self._apply_node(l, f)
                l += 1
            if r & 1:
                r -= 1
                self._apply_node(r, f)
            l >>= 1
            r >>= 1
        l, r = l2, r2
        for i in range(1, self._log + 1):
            if ((l >> i) << i) != l:
                self._update(l >> i)
            if ((r >> i) << i) != r:
                self._update((r - 1) >> i)

    def max_right(self, l, g):
        if l >= self._n:
            return self._n
        l += self._size
        for i in range(self._log, 0, -1):
            self._push(l >> i)
        sm = self._e
        while True:
            while l % 2 == 0:
                l >>= 1
            if not g(self._op(sm, self._d[l])):
                while l < self._size:
                    self._push(l)
                    l *= 2
                    if g(self._op(sm, self._d[l])):
                        sm = self._op(sm, self._d[l])
                        l += 1
                return l - self._size
            sm = self._op(sm, self._d[l])
            l += 1
            if (l & -l) == l:
                break
        return self._n

    def min_left(self, r, g):
        if r <= 0:
            return 0
        r += self._size
        for i in range(self._log, 0, -1):
            self._push((r - 1) >> i)
        sm = self._e
        while True:
            r -= 1
            while r > 1 and r % 2:
                r >>= 1
            if not g(self._op(self._d[r], sm)):
                while r < self._size:
                    self._push(r)
                    r = 2 * r + 1
                    if g(self._op(self._d[r], sm)):
                        sm = self._op(self._d[r], sm)
                        r -= 1
                return r + 1 - self._size
            sm = self._op(self._d[r], sm)
            if (r & -r) == r:
                break
        return 0

    def to_list(self):
        return [self.get(i) for i in range(self._n)]
