# =============================================================================
# 組み合わせ (mod p, p は素数)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   C = Combination(n_max, mod=998244353)   # 前処理 O(n_max)。n_max は使う n (重複組合せなら n + r - 1) の最大値
#   C.comb(n, r)         # nCr         (範囲外は 0)
#   C.perm(n, r)         # nPr
#   C.homo(n, r)         # nHr = (n+r-1)Cr  (n 種類から重複を許して r 個)
#   C.fact(n)            # n!
#   C.inv_fact(n)        # (n!)^-1
#   C.inv(n)             # n^-1   (1 <= n <= n_max)
#   C(n, r)              # comb(n, r) の別名
#
# nCr を 1 回だけ、n が大きく r が小さいとき:  comb_single(n, r, mod)  O(r)


class Combination:
    def __init__(self, n_max, mod=998244353):
        self.mod = mod
        self.n_max = n_max
        fact = [1] * (n_max + 1)
        for i in range(1, n_max + 1):
            fact[i] = fact[i - 1] * i % mod
        inv_fact = [1] * (n_max + 1)
        inv_fact[n_max] = pow(fact[n_max], mod - 2, mod)
        for i in range(n_max, 0, -1):
            inv_fact[i - 1] = inv_fact[i] * i % mod
        self._fact = fact
        self._inv_fact = inv_fact

    def fact(self, n):
        return self._fact[n]

    def inv_fact(self, n):
        return self._inv_fact[n]

    def inv(self, n):
        return self._inv_fact[n] * self._fact[n - 1] % self.mod

    def comb(self, n, r):
        if r < 0 or r > n:
            return 0
        return self._fact[n] * self._inv_fact[r] % self.mod * self._inv_fact[n - r] % self.mod

    __call__ = comb

    def perm(self, n, r):
        if r < 0 or r > n:
            return 0
        return self._fact[n] * self._inv_fact[n - r] % self.mod

    def homo(self, n, r):
        if n < 0 or r < 0:
            return 0
        if n == 0:
            return 1 if r == 0 else 0
        return self.comb(n + r - 1, r)


def comb_single(n, r, mod):
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)
    num = den = 1
    for i in range(r):
        num = num * ((n - i) % mod) % mod
        den = den * (i + 1) % mod
    return num * pow(den, mod - 2, mod) % mod
