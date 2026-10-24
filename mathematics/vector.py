# =============================================================================
# Vector (数のベクトル)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   v = Vector([1, 2, 3])            # mod を渡すと全ての演算結果を mod で割った余りにする
#   v = Vector([1, 2, 3], mod=998244353)
#   v + w, v - w, -v                 # 成分ごとの和・差
#   v * c, c * v                     # スカラー倍
#   v.dot(w)                         # 内積
#   v // c, v % c
#   v[i], v[i] = x, len(v), list(v), v.tolist(), v == w


class Vector:
    def __init__(self, values, mod=None):
        self.mod = mod
        self.a = [x % mod for x in values] if mod else list(values)

    def _new(self, values):
        return Vector(values, self.mod)

    def __getitem__(self, i):
        return self.a[i]

    def __setitem__(self, i, x):
        self.a[i] = x % self.mod if self.mod else x

    def __len__(self):
        return len(self.a)

    def __iter__(self):
        return iter(self.a)

    def __repr__(self):
        return "Vector(%r)" % (self.a,)

    def __eq__(self, other):
        return isinstance(other, Vector) and self.a == other.a

    def tolist(self):
        return list(self.a)

    def __neg__(self):
        return self._new([-x for x in self.a])

    def __add__(self, other):
        assert len(self) == len(other)
        return self._new([x + y for x, y in zip(self.a, other)])

    def __sub__(self, other):
        assert len(self) == len(other)
        return self._new([x - y for x, y in zip(self.a, other)])

    def __mul__(self, c):
        return self._new([x * c for x in self.a])

    __rmul__ = __mul__

    def __floordiv__(self, c):
        return self._new([x // c for x in self.a])

    def __mod__(self, c):
        return self._new([x % c for x in self.a])

    def dot(self, other):
        assert len(self) == len(other)
        res = sum(x * y for x, y in zip(self.a, other))
        return res % self.mod if self.mod else res
