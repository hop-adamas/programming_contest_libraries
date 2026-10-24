# =============================================================================
# Mo's algorithm
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   mo = Mo(n)
#   for l, r in queries: mo.add_query(l, r)      # 半開区間 [l, r)
#   ans = mo.run(add_left, add_right, del_left, del_right, rem)
#     add_left(i)  : 区間の左に a[i] を加える      add_right(i) : 区間の右に a[i] を加える
#     del_left(i)  : 区間の左から a[i] を除く      del_right(i) : 区間の右から a[i] を除く
#     rem()        : 現在の区間に対する答えを返す
#     ans[k] = k 番目に追加したクエリの答え
#   add/del が左右で同じ処理なら add_left = add_right = add のように同じ関数を渡す。
#
# 例 (区間内の異なる値の個数)
#   cnt = [0] * (max(A) + 1); res = 0
#   def add(i):
#       nonlocal res
#       cnt[A[i]] += 1
#       if cnt[A[i]] == 1: res += 1
#   def delete(i):
#       nonlocal res
#       cnt[A[i]] -= 1
#       if cnt[A[i]] == 0: res -= 1
#   ans = mo.run(add, add, delete, delete, lambda: res)
# 計算量 O(n √q) 回の add/del
import math


class Mo:
    def __init__(self, n):
        self.n = n
        self.queries = []

    def add_query(self, l, r):
        self.queries.append((l, r))

    def run(self, add_left, add_right, del_left, del_right, rem):
        q = len(self.queries)
        if q == 0:
            return []
        block = max(1, int(self.n / math.sqrt(q)))
        # 偶数ブロックと奇数ブロックで r の向きを反転させる (定数倍高速化)
        order = sorted(
            range(q),
            key=lambda i: (
                self.queries[i][0] // block,
                self.queries[i][1] if (self.queries[i][0] // block) % 2 == 0 else -self.queries[i][1],
            ),
        )
        ans = [None] * q
        nl = nr = 0
        for idx in order:
            l, r = self.queries[idx]
            while nl > l:
                nl -= 1
                add_left(nl)
            while nr < r:
                add_right(nr)
                nr += 1
            while nl < l:
                del_left(nl)
                nl += 1
            while nr > r:
                nr -= 1
                del_right(nr)
            ans[idx] = rem()
        return ans
