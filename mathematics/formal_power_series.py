# =============================================================================
# NTT 畳み込み / 形式的冪級数 (mod 998244353)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方 (多項式・冪級数は係数のリスト [a0, a1, ...] で表す)
#   convolve(a, b)         # 畳み込み (a * b の係数)                       O((n + m) log(n + m))
#   poly_inv(a, deg)       # 1 / a(x) の先頭 deg 項 (a[0] != 0。必ず deg 項返す)            O(deg log deg)
#   poly_mul_trunc(a, b, deg)  # a * b の先頭 deg 項
# 注意: 純 Python のため遅い。PyPy で長さ 2^17 程度までを目安にする。
# 他の mod の畳み込みが必要なときは、この mod の畳み込みを複数回使う方法 (Garner) などを別途用意する。

MOD = 998244353
_ROOT = 3  # 998244353 の原始根


def _ntt(a, inverse=False):
    """a (長さは 2 冪) をその場で NTT する。inverse=True なら逆変換 (1/n 倍まで行う)"""
    n = len(a)
    mod = MOD
    # ビット反転置換
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        w1 = pow(_ROOT, (mod - 1) // length, mod)
        if inverse:
            w1 = pow(w1, mod - 2, mod)
        half = length >> 1
        ws = [1] * half
        for k in range(1, half):
            ws[k] = ws[k - 1] * w1 % mod
        for i in range(0, n, length):
            for k in range(half):
                u = a[i + k]
                v = a[i + k + half] * ws[k] % mod
                a[i + k] = u + v if u + v < mod else u + v - mod
                a[i + k + half] = u - v if u >= v else u - v + mod
        length <<= 1
    if inverse:
        inv_n = pow(n, mod - 2, mod)
        for i in range(n):
            a[i] = a[i] * inv_n % mod


def convolve(a, b):
    if not a or not b:
        return []
    n_res = len(a) + len(b) - 1
    if min(len(a), len(b)) <= 16:  # 短いときは素直に計算した方が速い
        res = [0] * n_res
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    res[i + j] = (res[i + j] + x * y) % MOD
        return res
    n = 1 << (n_res - 1).bit_length()
    fa = a + [0] * (n - len(a))
    fb = b + [0] * (n - len(b))
    _ntt(fa)
    _ntt(fb)
    fa = [x * y % MOD for x, y in zip(fa, fb)]
    _ntt(fa, inverse=True)
    return fa[:n_res]


def poly_mul_trunc(a, b, deg):
    return convolve(a[:deg], b[:deg])[:deg]


def poly_inv(a, deg):
    assert a[0] % MOD != 0
    res = [pow(a[0], MOD - 2, MOD)]
    m = 1
    while m < deg:
        m <<= 1
        # res <- res * (2 - a * res) (mod x^m)
        ar = convolve(a[:m], res)[:m]
        ar += [0] * (m - len(ar))
        t = [(-x) % MOD for x in ar]
        t[0] = (t[0] + 2) % MOD
        res = convolve(res, t)[:m]
        res += [0] * (m - len(res))
    return res[:deg]
