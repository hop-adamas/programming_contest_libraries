# =============================================================================
# Z algorithm
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   z = z_algorithm(s)       # s: 文字列 / リスト。z[i] = LCP(s, s[i:])、z[0] = len(s)。O(n)
# パターン検索: z_algorithm(pattern + '#' + text) で z[i] == len(pattern) となる位置。


def z_algorithm(s):
    n = len(s)
    z = [0] * n
    if n == 0:
        return z
    z[0] = n
    l = r = 0  # [l, r) は既に分かっている s の接頭辞と一致する最も右の区間
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z
