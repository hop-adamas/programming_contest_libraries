# =============================================================================
# SparseTable (冪等な演算の区間クエリ。構築 O(n log n), クエリ O(1))
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   st = SparseTable(arr, func=min)   # func は冪等 (func(x, x) = x) かつ結合的: min, max, gcd, and, or など
#   st.query(l, r)                    # func(arr[l], ..., arr[r-1])  (l < r)
# 更新は不可。更新がある場合は segment_tree.py を使う。


class SparseTable:
    def __init__(self, arr, func=min):
        self.func = func
        self.n = len(arr)
        self.table = [list(arr)]
        k = 1
        while 2 * k <= self.n:
            prev = self.table[-1]
            self.table.append([func(prev[i], prev[i + k]) for i in range(self.n - 2 * k + 1)])
            k *= 2

    def query(self, l, r):
        assert 0 <= l < r <= self.n
        k = (r - l).bit_length() - 1
        row = self.table[k]
        return self.func(row[l], row[r - (1 << k)])
