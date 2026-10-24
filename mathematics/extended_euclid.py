# =============================================================================
# 拡張ユークリッドの互除法 / 一次合同式 / 中国剰余定理
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   g, x, y = ext_gcd(a, b)      # a*x + b*y = g = gcd(a, b)  (g >= 0)
#                                # 一般解は (x + k*b//g, y - k*a//g)
#   inv_mod(a, mod)              # a の mod での逆元 (存在しなければ ValueError)
#   mod_solve(a, b, mod)         # a*x ≡ b (mod mod) の最小の非負解 x。解なしは -1
#   crt(R, M)                    # x ≡ R[i] (mod M[i]) を満たす (x, lcm)。解なしは (0, -1)
#                                # M は互いに素でなくてもよい。x は 0 <= x < lcm


def ext_gcd(a, b):
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    if a < 0:
        a, x0, y0 = -a, -x0, -y0
    return a, x0, y0


def inv_mod(a, mod):
    g, x, _ = ext_gcd(a % mod, mod)
    if g != 1:
        raise ValueError("inverse does not exist")
    return x % mod


def mod_solve(a, b, mod):
    g, x, _ = ext_gcd(a, mod)
    if b % g:
        return -1
    mod //= g
    return (x * (b // g)) % mod


def crt(R, M):
    r0, m0 = 0, 1
    for r, m in zip(R, M):
        g, p, _ = ext_gcd(m0, m)  # m0 * p ≡ g (mod m)
        if (r - r0) % g:
            return 0, -1
        lcm = m0 // g * m
        r0 += m0 * ((r - r0) // g * p % (m // g))
        r0 %= lcm
        m0 = lcm
    return r0, m0
