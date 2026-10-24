# =============================================================================
# LiChaoTree (直線の追加 + 点での最小値クエリ)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   lc = LiChaoTree(xs)       # クエリで使う x 座標のリスト (重複可)
#   lc.add_line(a, b)         # 直線 y = a*x + b を追加          O(log n)
#   lc.query(x)               # x での最小値 (x は xs に含まれること)  O(log n)
# 最大値が欲しいときは (-a, -b) を追加して答えの符号を反転する。
# 直線が 1 本も無いときの query は INF (10**18) を返す。
import bisect


class LiChaoTree:
    INF = 10**18

    def __init__(self, xs):
        self.x_list = sorted(set(xs))
        self.n = 1 << (len(self.x_list) - 1).bit_length()
        self.x_list += [self.x_list[-1]] * (self.n - len(self.x_list))
        self.lines = [(0, self.INF)] * (2 * self.n)

    @staticmethod
    def _f(line, x):
        return line[0] * x + line[1]

    def add_line(self, a, b):
        line = (a, b)
        idx = 1
        l, r = 0, self.n
        xs, f = self.x_list, self._f
        while True:
            m = (l + r) >> 1
            cur = self.lines[idx]
            left_better = f(line, xs[l]) < f(cur, xs[l])
            mid_better = f(line, xs[m]) < f(cur, xs[m])
            if mid_better:
                self.lines[idx], line = line, cur
            if r - l == 1:
                break
            if left_better != mid_better:
                idx = 2 * idx
                r = m
            else:
                idx = 2 * idx + 1
                l = m

    def query(self, x):
        node = bisect.bisect_left(self.x_list, x) + self.n
        res = self.INF
        while node > 0:
            v = self._f(self.lines[node], x)
            if v < res:
                res = v
            node >>= 1
        return res
