# =============================================================================
# SegmentTree (非再帰, モノイド)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# 参考: https://github.com/atcoder/ac-library/blob/master/atcoder/segtree.hpp
# =============================================================================
#
# 使い方
#   st = SegmentTree(op, e, n_or_list)
#     op: 結合的な二項演算 op(a, b),  e: 単位元
#     n_or_list: 要素数 n (全て e) もしくは初期値のリスト
#   st.set(i, x)            # a[i] = x                    O(log n)
#   st.get(i)               # a[i]                         O(1)
#   st.prod(l, r)           # op(a[l], ..., a[r-1])  (半開区間) O(log n)
#   st.all_prod()           # op(a[0], ..., a[n-1])        O(1)
#   st.max_right(l, f)      # f(op(a[l..r-1])) が True となる最大の r  (f(e) は True)
#   st.min_left(r, f)       # f(op(a[l..r-1])) が True となる最小の l
#
# 例 (区間最小値)
#   st = SegmentTree(min, 10**18, A)
#   st.prod(l, r)
# 例 (区間和)
#   st = SegmentTree(lambda a, b: a + b, 0, A)
# 例 (区間 xor)
#   st = SegmentTree(lambda a, b: a ^ b, 0, A)


class SegmentTree:
    def __init__(self, op, e, v):
        self._op = op
        self._e = e
        if isinstance(v, int):
            v = [e] * v
        self._n = len(v)
        self._log = (self._n - 1).bit_length()
        self._size = 1 << self._log
        self._d = [e] * (2 * self._size)
        for i in range(self._n):
            self._d[self._size + i] = v[i]
        for i in range(self._size - 1, 0, -1):
            self._update(i)

    def _update(self, k):
        self._d[k] = self._op(self._d[2 * k], self._d[2 * k + 1])

    def set(self, p, x):
        """a[p] = x"""
        p += self._size
        self._d[p] = x
        for _ in range(self._log):
            p >>= 1
            self._update(p)

    def get(self, p):
        return self._d[p + self._size]

    def prod(self, l, r):
        """op(a[l], ..., a[r-1])。l >= r のとき単位元"""
        sml = self._e
        smr = self._e
        l += self._size
        r += self._size
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

    def max_right(self, l, f):
        """
        f(op(a[l], ..., a[r-1])) = True となる最大の r を返す。
        f は単調 (True の後に False) で f(e) = True であること。
        """
        if l == self._n:
            return self._n
        l += self._size
        sm = self._e
        while True:
            while l % 2 == 0:
                l >>= 1
            if not f(self._op(sm, self._d[l])):
                while l < self._size:
                    l *= 2
                    if f(self._op(sm, self._d[l])):
                        sm = self._op(sm, self._d[l])
                        l += 1
                return l - self._size
            sm = self._op(sm, self._d[l])
            l += 1
            if (l & -l) == l:
                break
        return self._n

    def min_left(self, r, f):
        """
        f(op(a[l], ..., a[r-1])) = True となる最小の l を返す。
        f は単調 (r から左へ伸ばすと True の後に False) で f(e) = True であること。
        """
        if r == 0:
            return 0
        r += self._size
        sm = self._e
        while True:
            r -= 1
            while r > 1 and r % 2:
                r >>= 1
            if not f(self._op(self._d[r], sm)):
                while r < self._size:
                    r = 2 * r + 1
                    if f(self._op(self._d[r], sm)):
                        sm = self._op(self._d[r], sm)
                        r -= 1
                return r + 1 - self._size
            sm = self._op(self._d[r], sm)
            if (r & -r) == r:
                break
        return 0
