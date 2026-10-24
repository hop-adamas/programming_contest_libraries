# =============================================================================
# Multiset (最小値を O(1) で取れる多重集合。ヒープ 2 本による遅延削除)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   ms = Multiset([3, 1, 4])
#   ms.add(x)           # 追加                         O(log n)
#   ms.remove(x)        # 1 個削除 (無ければ KeyError)    O(log n)
#   ms.min()            # 最小値 (空なら IndexError)       O(1)
#   ms.pop_min()        # 最小値を取り出して削除            O(log n)
#   ms.count(x), x in ms, len(ms)
# 最大値が欲しいときは -x を入れる。
# lower_bound など順序つきの検索が必要なら sorted_set.py の SortedMultiSet を使う。
import heapq


class Multiset:
    def __init__(self, items=()):
        self._alive = []  # 追加された値 (削除済みを含みうる)
        self._dead = []  # 削除された値 (まだ _alive から消えていないもの)
        self._cnt = {}
        self._len = 0
        for x in items:
            self.add(x)

    def add(self, x):
        heapq.heappush(self._alive, x)
        self._cnt[x] = self._cnt.get(x, 0) + 1
        self._len += 1

    def remove(self, x):
        if self._cnt.get(x, 0) == 0:
            raise KeyError(x)
        self._cnt[x] -= 1
        self._len -= 1
        heapq.heappush(self._dead, x)
        self._settle()

    def _settle(self):
        # 先頭が削除済みの値である間、両方のヒープから取り除く
        alive, dead = self._alive, self._dead
        while dead and alive[0] == dead[0]:
            heapq.heappop(alive)
            heapq.heappop(dead)

    def min(self):
        if not self._len:
            raise IndexError("min of empty Multiset")
        return self._alive[0]

    def pop_min(self):
        x = self.min()
        self.remove(x)
        return x

    def count(self, x):
        return self._cnt.get(x, 0)

    def __contains__(self, x):
        return self._cnt.get(x, 0) > 0

    def __len__(self):
        return self._len
