# =============================================================================
# Matrix (数の行列)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   A = Matrix([[1, 1], [1, 0]])                  # mod を渡すと全ての演算結果を mod で割った余りにする
#   A = Matrix([[1, 1], [1, 0]], mod=10**9 + 7)
#   Matrix.identity(n, mod=None), Matrix.zeros(h, w, mod=None)
#   A + B, A - B, A * B (行列積), A * c / c * A (スカラー倍)
#   A * v                    # v: list / tuple / Vector (列ベクトル)。結果は list
#   A ** m                   # m 乗 (m >= 0, 正方行列)  O(n^3 log m)
#   A.T                      # 転置
#   A[i][j], A[i, j] = x, A.h, A.w, A.tolist()
#
# 例 (フィボナッチ数 F(n) mod p):  (Matrix([[1, 1], [1, 0]], mod=p) ** n)[0][1]


class Matrix:
    def __init__(self, rows, mod=None):
        self.mod = mod
        self.a = [[x % mod for x in row] for row in rows] if mod else [list(row) for row in rows]
        self.h = len(self.a)
        self.w = len(self.a[0]) if self.a else 0

    @classmethod
    def zeros(cls, h, w, mod=None):
        return cls([[0] * w for _ in range(h)], mod)

    @classmethod
    def identity(cls, n, mod=None):
        m = cls.zeros(n, n, mod)
        for i in range(n):
            m.a[i][i] = 1 % mod if mod else 1
        return m

    def __getitem__(self, idx):
        if isinstance(idx, tuple):
            return self.a[idx[0]][idx[1]]
        return self.a[idx]

    def __setitem__(self, idx, x):
        i, j = idx
        self.a[i][j] = x % self.mod if self.mod else x

    def __repr__(self):
        return "Matrix(%r)" % (self.a,)

    def __eq__(self, other):
        return isinstance(other, Matrix) and self.a == other.a

    def tolist(self):
        return [row[:] for row in self.a]

    @property
    def T(self):
        return Matrix(zip(*self.a), self.mod)

    def __add__(self, other):
        assert (self.h, self.w) == (other.h, other.w)
        return Matrix([[x + y for x, y in zip(r, s)] for r, s in zip(self.a, other.a)], self.mod)

    def __sub__(self, other):
        assert (self.h, self.w) == (other.h, other.w)
        return Matrix([[x - y for x, y in zip(r, s)] for r, s in zip(self.a, other.a)], self.mod)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            assert self.w == other.h
            cols = list(zip(*other.a))
            return Matrix([[sum(x * y for x, y in zip(r, c)) for c in cols] for r in self.a], self.mod)
        if isinstance(other, (list, tuple)) or hasattr(other, "tolist"):
            assert self.w == len(other)
            res = [sum(x * y for x, y in zip(r, other)) for r in self.a]
            return [x % self.mod for x in res] if self.mod else res
        return Matrix([[x * other for x in r] for r in self.a], self.mod)

    def __rmul__(self, c):
        return Matrix([[c * x for x in r] for r in self.a], self.mod)

    def __pow__(self, m):
        assert self.h == self.w and m >= 0
        res = Matrix.identity(self.h, self.mod)
        base = self
        while m:
            if m & 1:
                res = res * base
            base = base * base
            m >>= 1
        return res
