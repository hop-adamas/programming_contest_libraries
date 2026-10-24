# =============================================================================
# Stern-Brocot tree (正の既約分数 p/q の二分木。根は 1/1)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 分数は既約 (gcd(p, q) = 1) で p, q >= 1 とする。
# 根から p/q までの道のりを「連続する同じ向きの移動をまとめた」リスト [(向き, 回数), ...] で表す。
# 向きは 'L' (左の子 = 小さい方へ) か 'R' (右の子 = 大きい方へ)。根は空リスト。
#
# 使い方
#   SternBrocotTree.path(p, q)            # 根から p/q への道のり。O(log)
#   SternBrocotTree.node(path)            # 道のりが指す分数 (p, q)
#   SternBrocotTree.depth(p, q)           # 根からの深さ
#   SternBrocotTree.lca(p1, q1, p2, q2)   # 2 つの分数の最小共通祖先 (p, q)
#   SternBrocotTree.ancestor(p, q, k)     # k 個上の祖先 (p, q)。深さが足りなければ None
#   SternBrocotTree.bounds(p, q)          # p/q を根とする部分木に入る分数の範囲 (lp, lq, rp, rq):
#                                         #   lp/lq < x < rp/rq  (rq = 0 のときは右が +∞)


class SternBrocotTree:
    @staticmethod
    def path(p, q):
        # p/q の連分数展開 [a0; a1, a2, ...] は R^a0 L^a1 R^a2 ... の道のりに対応し、最後の 1 歩だけ余分
        runs = []
        right = True
        while q:
            a, r = divmod(p, q)
            if a:
                runs.append(['R' if right else 'L', a])
            p, q = q, r
            right = not right
        if runs:
            runs[-1][1] -= 1
            if runs[-1][1] == 0:
                runs.pop()
        return [(d, k) for d, k in runs]

    @staticmethod
    def _interval(path):
        # 左端 lp/lq と右端 rp/rq (開区間) を、道のりに沿って狭めていく
        lp, lq, rp, rq = 0, 1, 1, 0
        for d, k in path:
            if d == 'R':
                lp, lq = lp + k * rp, lq + k * rq
            else:
                rp, rq = rp + k * lp, rq + k * lq
        return lp, lq, rp, rq

    @classmethod
    def node(cls, path):
        lp, lq, rp, rq = cls._interval(path)
        return lp + rp, lq + rq

    @classmethod
    def bounds(cls, p, q):
        return cls._interval(cls.path(p, q))

    @classmethod
    def depth(cls, p, q):
        return sum(k for _, k in cls.path(p, q))

    @classmethod
    def lca(cls, p1, q1, p2, q2):
        common = []
        for (d1, k1), (d2, k2) in zip(cls.path(p1, q1), cls.path(p2, q2)):
            if d1 != d2:
                break
            common.append((d1, min(k1, k2)))
            if k1 != k2:
                break
        return cls.node(common)

    @classmethod
    def ancestor(cls, p, q, k):
        runs = cls.path(p, q)
        remain = sum(c for _, c in runs) - k
        if remain < 0:
            return None
        kept = []
        for d, c in runs:
            if remain == 0:
                break
            take = min(c, remain)
            kept.append((d, take))
            remain -= take
        return cls.node(kept)
