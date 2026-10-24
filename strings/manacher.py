# =============================================================================
# Manacher (回文の半径)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   m = Manacher(s)              # s: 文字列 / リスト。O(n)
#   m.is_palindrome(l, r)        # s[l:r] が回文か (l < r)
#   m.R[c]                       # 中心 c (c = l + r, 区間 [l, r) の中心) での最長回文の長さ + 1
#   m.longest(c)                 # 中心 c の最長回文の長さ (= R[c] - 1)
#     c が偶数なら偶数長回文 (文字 c/2-1 と c/2 の間), 奇数なら奇数長回文 (文字 (c-1)/2 が中心)


class Manacher:
    def __init__(self, s):
        self.n = len(s)
        # 偶数長回文に対応するため間にダミー (None) を挿入
        t = [None] * (2 * self.n + 1)
        t[1::2] = s
        self.t = t
        m = len(t)
        R = [0] * m
        i = j = 0
        while i < m:
            while i - j >= 0 and i + j < m and t[i - j] == t[i + j]:
                j += 1
            R[i] = j
            k = 1
            while i - k >= 0 and k + R[i - k] < j:
                R[i + k] = R[i - k]
                k += 1
            i += k
            j -= k
        self.R = R

    def longest(self, c):
        return self.R[c] - 1

    def is_palindrome(self, l, r):
        return self.R[l + r] - 1 >= r - l
