# =============================================================================
# 幾何 (複素数による 2 次元幾何)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   点は複素数 x + y*1j で表す。
#   dot(a, b), cross(a, b)         # 内積 / 外積
#   ccw(a, b, c)                   # 3 点の位置関係 (戻り値は関数の docstring を参照)
#   intersect(p1, p2, p3, p4)      # 線分 p1-p2 と p3-p4 が (端点を含めて) 交差するか
#   convex_hull(points)            # 凸包 (反時計回り)。同一直線上の点は含めない
#   polygon_area(poly)             # 多角形 (頂点を順に並べたリスト) の面積。反時計回りなら正

EPS = 1e-9


def dot(a, b):
    """内積"""
    return (a.conjugate() * b).real


def cross(a, b):
    """外積"""
    return (a.conjugate() * b).imag


def ccw(a, b, c):
    """
    3点 a, b, c の位置関係（Counter-Clockwise）
    1: a-b-c が反時計回り
    -1: a-b-c が時計回り
    2: c-a-b の順で一直線上
    -2: a-b-c の順で一直線上
    0: a-c-b の順で一直線上 (cが線分ab上)
    """
    b -= a
    c -= a
    if cross(b, c) > EPS:
        return 1
    if cross(b, c) < -EPS:
        return -1
    if dot(b, c) < -EPS:
        return 2
    if abs(b) < abs(c):
        return -2
    return 0


def intersect(p1, p2, p3, p4):
    """線分 p1-p2 と 線分 p3-p4 が交差しているか判定"""
    return (
        ccw(p1, p2, p3) * ccw(p1, p2, p4) <= 0
        and ccw(p3, p4, p1) * ccw(p3, p4, p2) <= 0
    )


def convex_hull(points):
    """
    凸包（Monotone Chain法）。O(N log N)
    points: complex型のリスト。戻り値は凸包を構成する頂点のリスト（反時計回り）
    """
    # 実部（x座標）、虚部（y座標）の順にソート (重複する点は 1 つにまとめる)
    points = sorted(set(points), key=lambda p: (p.real, p.imag))
    if len(points) <= 2:
        return points

    def build(pts):
        hull = []
        for p in pts:
            # 同一直線上の点を含めない場合は <= 0 とする
            while len(hull) >= 2 and cross(hull[-1] - hull[-2], p - hull[-1]) <= 0:
                hull.pop()
            hull.append(p)
        return hull

    lower = build(points)
    upper = build(points[::-1])
    # 始点と終点が重複するので除外して結合
    return lower[:-1] + upper[:-1]


def polygon_area(poly):
    """多角形の面積 (符号つき。反時計回りなら正)"""
    n = len(poly)
    return sum(cross(poly[i], poly[(i + 1) % n]) for i in range(n)) / 2
