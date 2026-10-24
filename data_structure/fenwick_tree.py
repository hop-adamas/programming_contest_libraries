# =============================================================================
# FenwickTree (Binary Indexed Tree) / FenwickTree2D
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   ft = FenwickTree(n)              # 長さ n の配列 (全て 0) , 0-indexed
#   ft.add(i, x)             # a[i] += x                          O(log n)
#   ft.sum(i)                # a[0] + ... + a[i]  (i を含む)       O(log n)
#   ft.range_sum(l, r)       # a[l] + ... + a[r-1] (半開区間)      O(log n)
#   ft.lower_bound(w)        # a[0..x] の和 >= w となる最小の x    O(log n)
#   ft.upper_bound(w)        # a[0..x] の和 >  w となる最小の x    O(log n)
#     (lower/upper_bound は a[i] >= 0 が前提。無ければ n を返す)
#
#   ft2 = FenwickTree2D(h, w)
#   ft2.add(i, j, x)         # a[i][j] += x
#   ft2.query(i1, j1, i2, j2)  # [i1, i2) x [j1, j2) の和
#
# 転倒数の例: 値を座標圧縮して 0..n-1 にし、
#   for v in A: inv += ft.range_sum(v + 1, n); ft.add(v, 1)


class FenwickTree:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)  # 1-indexed

    def add(self, i, x):
        """a[i] += x"""
        i += 1
        n = self.n
        bit = self.bit
        while i <= n:
            bit[i] += x
            i += i & -i

    def sum(self, i):
        """a[0] + ... + a[i] (i を含む)。i < 0 なら 0"""
        i += 1
        res = 0
        bit = self.bit
        while i > 0:
            res += bit[i]
            i -= i & -i
        return res

    def range_sum(self, l, r):
        """a[l] + ... + a[r-1] (半開区間 [l, r))"""
        if r <= l:
            return 0
        return self.sum(r - 1) - self.sum(l - 1)

    def lower_bound(self, w):
        """
        a[0] + ... + a[x] >= w となる最小の x を返す。存在しなければ n。
        a[i] >= 0 が前提。
        """
        if w <= 0:
            return 0
        n = self.n
        x = 0
        k = 1 << n.bit_length()
        while k:
            if x + k <= n and self.bit[x + k] < w:
                w -= self.bit[x + k]
                x += k
            k >>= 1
        return x

    def upper_bound(self, w):
        """
        a[0] + ... + a[x] > w となる最小の x を返す。存在しなければ n。
        a[i] >= 0 が前提。
        """
        if w < 0:
            return 0
        n = self.n
        x = 0
        k = 1 << n.bit_length()
        while k:
            if x + k <= n and self.bit[x + k] <= w:
                w -= self.bit[x + k]
                x += k
            k >>= 1
        return x


class FenwickTree2D:
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.bit = [[0] * (w + 1) for _ in range(h + 1)]

    def add(self, i, j, x):
        """a[i][j] += x"""
        i += 1
        while i <= self.h:
            row = self.bit[i]
            k = j + 1
            while k <= self.w:
                row[k] += x
                k += k & -k
            i += i & -i

    def sum(self, i, j):
        """[0, i] x [0, j] の和 (i, j を含む)。i < 0 または j < 0 なら 0"""
        res = 0
        i += 1
        while i > 0:
            row = self.bit[i]
            k = j + 1
            while k > 0:
                res += row[k]
                k -= k & -k
            i -= i & -i
        return res

    def query(self, i1, j1, i2, j2):
        """[i1, i2) x [j1, j2) の和"""
        if i2 <= i1 or j2 <= j1:
            return 0
        return (
            self.sum(i2 - 1, j2 - 1)
            - self.sum(i2 - 1, j1 - 1)
            - self.sum(i1 - 1, j2 - 1)
            + self.sum(i1 - 1, j1 - 1)
        )
