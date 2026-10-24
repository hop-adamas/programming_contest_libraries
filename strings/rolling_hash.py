# =============================================================================
# RollingHash (mod 2^61 - 1, 基数はランダム)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   rh = RollingHash(s)            # s: 文字列 または 整数リスト。前計算 O(n)
#   rh.get(l, r)                   # s[l:r] のハッシュ値 (整数)
#   rh.get(l1, r1) == rh.get(l2, r2)  で部分列の一致判定 (衝突確率は 長さ / 2^61 程度)
#   rh.combine(h1, h2, len2)       # ハッシュ h1 の列の後ろにハッシュ h2 (長さ len2) の列を連結したハッシュ
# 2 つの文字列を比べるときは同じ基数を使う:  RollingHash(t, base=rh.base)
#   rh.lcp(i, other, j)            # s[i:] と other[j:] の最長共通接頭辞の長さ (二分探索, O(log n))
import random

MOD = (1 << 61) - 1


class RollingHash:
    def __init__(self, s, base=None):
        self.n = len(s)
        self.base = base or random.randrange(1 << 20, MOD - 1)
        n, b = self.n, self.base
        self.hash = [0] * (n + 1)
        self.pow = [1] * (n + 1)
        for i, ch in enumerate(s):
            val = ord(ch) if isinstance(ch, str) else ch + 1
            self.hash[i + 1] = (self.hash[i] * b + val) % MOD
            self.pow[i + 1] = self.pow[i] * b % MOD

    def get(self, l, r):
        return (self.hash[r] - self.hash[l] * self.pow[r - l]) % MOD

    def combine(self, h1, h2, len2):
        return (h1 * pow(self.base, len2, MOD) + h2) % MOD

    def lcp(self, i, other, j):
        assert self.base == other.base
        lo, hi = 0, min(self.n - i, other.n - j) + 1  # lo: 一致する, hi: 一致しない (または範囲外)
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if self.get(i, i + mid) == other.get(j, j + mid):
                lo = mid
            else:
                hi = mid
        return lo
