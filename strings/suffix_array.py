# =============================================================================
# SuffixArray / LCP array (SA-IS)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# 参考: https://github.com/atcoder/ac-library/blob/master/atcoder/string.hpp
# 参考: https://speakerdeck.com/flare/sa-is?slide=61
# =============================================================================
#
# 使い方
#   sa  = suffix_array(s)      # s: 文字列 または 整数リスト (upper を渡すと 0..upper の整数列として扱う)
#   lcp = lcp_array(s, sa)     # lcp[i] = LCP(s[sa[i]:], s[sa[i+1]:])  (長さ n-1)

"""
suffix array with SA_IS.

references:
https://github.com/atcoder/ac-library/blob/master/atcoder/string.hpp
https://speakerdeck.com/flare/sa-is?slide=61
"""

from functools import cmp_to_key


def sa_naive(s):
    n = len(s)
    sa = [i for i in range(n)]

    def cmp(l, r):
        if l == r:
            return 1
        while l < n and r < n:
            if s[l] != s[r]:
                return -1 if s[l] < s[r] else 1
            l += 1
            r += 1
        return -1 if l == n else 1

    sa.sort(key=cmp_to_key(cmp))
    return sa


def sa_doubling(s):
    n = len(s)
    sa = [i for i in range(n)]
    rnk = s.copy()
    tmp = [0] * n
    k = 1
    while k < n:

        def cmp(x, y):
            if rnk[x] != rnk[y]:
                return -1 if rnk[x] < rnk[y] else 1

            rx = rnk[x + k] if x + k < n else -1
            ry = rnk[y + k] if y + k < n else -1
            return -1 if rx < ry else 1

        sa.sort(key=cmp_to_key(cmp))
        tmp[sa[0]] = 0
        for i in range(1, n):
            tmp[sa[i]] = tmp[sa[i - 1]] + (cmp(sa[i - 1], sa[i]) == -1)
        tmp, rnk = rnk, tmp
        k *= 2
    return sa


def sa_is(s, upper):
    THRESHOLD_NAIVE = 10
    THRESHOLD_DOUBLING = 40
    n = len(s)
    if n == 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        if s[0] < s[1]:
            return [0, 1]
        else:
            return [1, 0]

    if n < THRESHOLD_NAIVE:
        return sa_naive(s)
    if n < THRESHOLD_DOUBLING:
        return sa_doubling(s)

    sa = [0] * n
    ls = [False] * n  # if s[i] == S -> ls[i] = True
    for i in range(n - 2, -1, -1):
        ls[i] = ls[i + 1] if s[i] == s[i + 1] else (s[i] < s[i + 1])
    sum_l = [0] * (upper + 1)
    sum_s = [0] * (upper + 1)
    for i in range(n):
        if not ls[i]:
            sum_s[s[i]] += 1
        else:
            sum_l[s[i] + 1] += 1
    for i in range(upper + 1):
        sum_s[i] += sum_l[i]
        if i < upper:
            sum_l[i + 1] += sum_s[i]

    def induce(lms):
        nonlocal sa
        for i in range(n):
            sa[i] = -1
        buf = sum_s[:]
        for d in lms:
            if d == n:
                continue
            sa[buf[s[d]]] = d
            buf[s[d]] += 1
        buf = sum_l[:]
        sa[buf[s[n - 1]]] = n - 1
        buf[s[n - 1]] += 1
        for i in range(n):
            v = sa[i]
            if v >= 1 and not ls[v - 1]:
                sa[buf[s[v - 1]]] = v - 1
                buf[s[v - 1]] += 1
        buf = sum_l[:]
        for i in range(n - 1, -1, -1):
            v = sa[i]
            if v >= 1 and ls[v - 1]:
                buf[s[v - 1] + 1] -= 1
                sa[buf[s[v - 1] + 1]] = v - 1

    lms_map = [-1] * (n + 1)
    m = 0
    for i in range(1, n):
        if not ls[i - 1] and ls[i]:
            lms_map[i] = m
            m += 1
    lms = []
    for i in range(1, n):
        if not ls[i - 1] and ls[i]:
            lms.append(i)

    induce(lms)

    if m:
        sorted_lms = []
        for v in sa:
            if lms_map[v] != -1:
                sorted_lms.append(v)
        rec_s = [0] * m
        rec_upper = 0
        rec_s[lms_map[sorted_lms[0]]] = 0
        for i in range(1, m):
            l, r = sorted_lms[i - 1], sorted_lms[i]
            end_l = lms[lms_map[l] + 1] if lms_map[l] + 1 < m else n
            end_r = lms[lms_map[r] + 1] if lms_map[r] + 1 < m else n
            same = True
            if end_l - l != end_r - r:
                same = False
            else:
                while l < end_l:
                    if s[l] != s[r]:
                        break
                    l += 1
                    r += 1
                if l == n or s[l] != s[r]:
                    same = False

            if not same:
                rec_upper += 1
            rec_s[lms_map[sorted_lms[i]]] = rec_upper
        rec_sa = sa_is(rec_s, rec_upper)
        for i in range(m):
            sorted_lms[i] = lms[rec_sa[i]]
        induce(sorted_lms)
    return sa


def suffix_array(s, upper=None):
    if isinstance(s, str):
        return sa_is(list(map(ord, s)), 255)
    elif upper is None:
        n = len(s)
        idx = list(range(n))

        def cmp(left, right):
            return s[left] - s[right]

        idx.sort(key=cmp_to_key(cmp))
        s2 = [0] * n
        now = 0
        for i in range(n):
            if i and s[idx[i - 1]] != s[idx[i]]:
                now += 1
            s2[idx[i]] = now
        return sa_is(s2, now)
    else:
        assert 0 <= upper
        for d in s:
            assert 0 <= d <= upper
        return sa_is(s, upper)


def lcp_array(s, sa):

    if isinstance(s, str):
        s = [ord(c) for c in s]
    n = len(s)
    assert n >= 1

    rnk = [0] * n
    for i in range(n):
        rnk[sa[i]] = i

    lcp = [0] * (n - 1)
    h = 0
    for i in range(n):
        if h > 0:
            h -= 1
        if rnk[i] == 0:
            continue
        j = sa[rnk[i] - 1]
        while j + h < n and i + h < n:
            if s[j + h] != s[i + h]:
                break
            h += 1
        lcp[rnk[i] - 1] = h

    return lcp
