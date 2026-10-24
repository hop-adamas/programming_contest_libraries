# =============================================================================
# Miller-Rabin 素数判定 / Pollard の rho 法による素因数分解
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   is_prime(n)             # 素数判定 (n < 3.3 * 10^24 で決定的)             O(log n) 回の mod 乗算
#   factorize(n)            # n の素因数 (重複あり) のソート済みリスト。n <= 1 なら []
#                           #   n <= 10^18 程度で期待 O(n^(1/4))
#   factorize_dict(n)       # {素数: 指数}
import random
from math import gcd

_SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def is_prime(n):
    if n < 2:
        return False
    for p in _SMALL_PRIMES:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in _SMALL_PRIMES:
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _find_factor(n):
    # n は合成数で、小さい素因数を持たない
    while True:
        c = random.randrange(1, n)
        x = y = random.randrange(n)
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
        if d != n:
            return d


def factorize(n):
    res = []
    for p in _SMALL_PRIMES:
        while n % p == 0:
            res.append(p)
            n //= p
    stack = [n] if n > 1 else []
    while stack:
        m = stack.pop()
        if is_prime(m):
            res.append(m)
            continue
        d = _find_factor(m)
        stack.append(d)
        stack.append(m // d)
    return sorted(res)


def factorize_dict(n):
    res = {}
    for p in factorize(n):
        res[p] = res.get(p, 0) + 1
    return res
