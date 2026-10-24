# =============================================================================
# 素因数分解 / 約数列挙 / 篩
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   prime_factorize(n)         # 試し割り O(√n)。{素数: 指数} の dict
#   divisors(n)                # n の約数のソート済みリスト       O(√n)
#   count_divisors(n)          # 約数の個数
#   sieve = PrimeSieve(N)      # 前処理 O(N log log N)
#   sieve.is_prime(n)          # n <= N が素数か
#   sieve.factorize(n)         # n <= N の素因数分解 {素数: 指数}   O(log n)
#   sieve.primes               # N 以下の素数のリスト
# 10^18 規模の素因数分解は pollard_rho.py を使う。
from math import isqrt


def prime_factorize(n):
    res = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            res[p] = res.get(p, 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        res[n] = res.get(n, 0) + 1
    return res


def divisors(n):
    small = []
    large = []
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            small.append(d)
            if d * d != n:
                large.append(n // d)
    return small + large[::-1]


def count_divisors(n):
    res = 1
    for e in prime_factorize(n).values():
        res *= e + 1
    return res


class PrimeSieve:
    def __init__(self, n):
        self.n = n
        self.spf = list(range(n + 1))  # 最小の素因数
        for i in range(2, isqrt(n) + 1):
            if self.spf[i] == i:
                for j in range(i * i, n + 1, i):
                    if self.spf[j] == j:
                        self.spf[j] = i
        self.primes = [i for i in range(2, n + 1) if self.spf[i] == i]

    def is_prime(self, n):
        return n >= 2 and self.spf[n] == n

    def factorize(self, n):
        res = {}
        while n > 1:
            p = self.spf[n]
            res[p] = res.get(p, 0) + 1
            n //= p
        return res
