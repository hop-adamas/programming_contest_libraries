# =============================================================================
# FastSet (0 <= x < n の整数集合。64 分木のビット演算で高速に前後検索)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   fs = FastSet(n)            # 空集合。値の範囲は 0 <= x < n
#   fs = FastSet(n, items)     # items で初期化
#   fs.insert(x)               # 追加 (既にあれば何もしない)         O(log_64 n)
#   fs.erase(x)                # 削除 (無ければ何もしない)
#   x in fs                    # 存在確認                         O(1)
#   fs.next(x)                 # x 以上の最小の要素 (無ければ None)
#   fs.prev(x)                 # x 以下の最大の要素 (無ければ None)
#   fs.min(), fs.max()         # 最小 / 最大 (空なら None)
#   fs.next(x + 1), fs.prev(x - 1) で「x より真に大きい / 小さい」要素が得られる。
# 順序統計量 (k 番目など) が必要なら sorted_set.py を使う。


class FastSet:
    def __init__(self, n, items=()):
        self.n = n
        self.levels = []  # levels[0] の bit x が要素 x の有無。上の階層は下の階層の語が非 0 かどうか
        m = n
        while True:
            m = (m + 63) >> 6
            self.levels.append([0] * m)
            if m <= 1:
                break
        for x in items:
            self.insert(x)

    def __contains__(self, x):
        return 0 <= x < self.n and self.levels[0][x >> 6] >> (x & 63) & 1 == 1

    def insert(self, x):
        assert 0 <= x < self.n
        for level in self.levels:
            level[x >> 6] |= 1 << (x & 63)
            x >>= 6

    def erase(self, x):
        if x not in self:
            return
        for level in self.levels:
            level[x >> 6] &= ~(1 << (x & 63))
            if level[x >> 6]:
                break
            x >>= 6

    def next(self, x):
        x = max(x, 0)
        if x >= self.n:
            return None
        levels = self.levels
        for h in range(len(levels)):
            if (x >> 6) >= len(levels[h]):
                break
            d = levels[h][x >> 6] >> (x & 63)
            if d == 0:
                x = (x >> 6) + 1
                continue
            x += (d & -d).bit_length() - 1
            for g in range(h - 1, -1, -1):
                w = levels[g][x]
                x = (x << 6) + (w & -w).bit_length() - 1
            return x
        return None

    def prev(self, x):
        x = min(x, self.n - 1)
        levels = self.levels
        for h in range(len(levels)):
            if x < 0:
                break
            d = levels[h][x >> 6] & ((2 << (x & 63)) - 1)
            if d == 0:
                x = (x >> 6) - 1
                continue
            x = ((x >> 6) << 6) + d.bit_length() - 1
            for g in range(h - 1, -1, -1):
                x = (x << 6) + levels[g][x].bit_length() - 1
            return x
        return None

    def min(self):
        return self.next(0)

    def max(self):
        return self.prev(self.n - 1)
