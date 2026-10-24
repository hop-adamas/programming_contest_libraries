# =============================================================================
# SortedSet / SortedMultiSet (バケット分割による順序つき集合)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# 参考: https://github.com/tatyam-prime/SortedSet (ライセンス: The Unlicense)
# =============================================================================
#
# 使い方
#   s = SortedSet(iterable)
#   s.add(x) / s.discard(x)    # O(√n)。追加/削除できたら True
#   x in s; s[k]; len(s); s.index(x) (x 未満の個数); s.index_right(x) (x 以下の個数)
#   s.lt(x) / s.le(x) / s.gt(x) / s.ge(x)   # x 未満/以下/超/以上 の最近接要素 (無ければ None)
#   SortedMultiSet は同じ値を複数持てる (add は戻り値なし)。count(x) あり。

from bisect import bisect_left, bisect_right, insort
from math import ceil, sqrt


class _BucketList:
    """√ 分割したソート済みリスト。SortedSet / SortedMultiSet の共通部分"""

    BUCKET_RATIO = 50
    REBUILD_RATIO = 170

    def _build(self, a=None):
        if a is None:
            a = list(self)
        size = self.size = len(a)
        bucket_size = ceil(sqrt(size / self.BUCKET_RATIO))
        self.a = [a[size * i // bucket_size : size * (i + 1) // bucket_size] for i in range(bucket_size)]

    def __iter__(self):
        for bucket in self.a:
            yield from bucket

    def __reversed__(self):
        for bucket in reversed(self.a):
            yield from reversed(bucket)

    def __len__(self):
        return self.size

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, list(self))

    def __str__(self):
        return "{" + ", ".join(map(str, self)) + "}"

    def _find_bucket(self, x):
        # x が入るべきバケット (空でないときだけ呼ぶ)
        for bucket in self.a:
            if x <= bucket[-1]:
                return bucket
        return bucket

    def __contains__(self, x):
        if self.size == 0:
            return False
        bucket = self._find_bucket(x)
        i = bisect_left(bucket, x)
        return i != len(bucket) and bucket[i] == x

    def _after_insert(self, bucket):
        self.size += 1
        if len(bucket) > len(self.a) * self.REBUILD_RATIO:
            self._build()

    def discard(self, x):
        """x を 1 個削除して True。無ければ False。O(√n)"""
        if self.size == 0:
            return False
        bucket = self._find_bucket(x)
        i = bisect_left(bucket, x)
        if i == len(bucket) or bucket[i] != x:
            return False
        bucket.pop(i)
        self.size -= 1
        if len(bucket) == 0:
            self._build()
        return True

    def lt(self, x):
        """x より小さい最大の要素 (無ければ None)"""
        for bucket in reversed(self.a):
            if bucket[0] < x:
                return bucket[bisect_left(bucket, x) - 1]

    def le(self, x):
        """x 以下の最大の要素 (無ければ None)"""
        for bucket in reversed(self.a):
            if bucket[0] <= x:
                return bucket[bisect_right(bucket, x) - 1]

    def gt(self, x):
        """x より大きい最小の要素 (無ければ None)"""
        for bucket in self.a:
            if bucket[-1] > x:
                return bucket[bisect_right(bucket, x)]

    def ge(self, x):
        """x 以上の最小の要素 (無ければ None)"""
        for bucket in self.a:
            if bucket[-1] >= x:
                return bucket[bisect_left(bucket, x)]

    def __getitem__(self, k):
        """小さい方から k 番目 (0-indexed)。負の添字は後ろから"""
        if k < 0:
            k += self.size
        if k < 0:
            raise IndexError
        for bucket in self.a:
            if k < len(bucket):
                return bucket[k]
            k -= len(bucket)
        raise IndexError

    def index(self, x):
        """x 未満の要素の個数"""
        res = 0
        for bucket in self.a:
            if bucket[-1] >= x:
                return res + bisect_left(bucket, x)
            res += len(bucket)
        return res

    def index_right(self, x):
        """x 以下の要素の個数"""
        res = 0
        for bucket in self.a:
            if bucket[-1] > x:
                return res + bisect_right(bucket, x)
            res += len(bucket)
        return res


class SortedSet(_BucketList):
    def __init__(self, a=()):
        a = list(a)
        if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
            a = sorted(set(a))
        self._build(a)

    def add(self, x):
        """x を追加して True。既にあれば False。O(√n)"""
        if self.size == 0:
            self.a = [[x]]
            self.size = 1
            return True
        bucket = self._find_bucket(x)
        i = bisect_left(bucket, x)
        if i != len(bucket) and bucket[i] == x:
            return False
        bucket.insert(i, x)
        self._after_insert(bucket)
        return True


class SortedMultiSet(_BucketList):
    def __init__(self, a=()):
        a = list(a)
        if not all(a[i] <= a[i + 1] for i in range(len(a) - 1)):
            a = sorted(a)
        self._build(a)

    def add(self, x):
        """x を追加する (重複可)。O(√n)"""
        if self.size == 0:
            self.a = [[x]]
            self.size = 1
            return
        bucket = self._find_bucket(x)
        insort(bucket, x)
        self._after_insert(bucket)

    def count(self, x):
        return self.index_right(x) - self.index(x)
