# =============================================================================
# 二分探索
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   x = binary_search(ok, ng, test)
#     test(ok) == True, test(ng) == False を満たす ok, ng を渡す (ok < ng でも ok > ng でもよい)。
#     test の境目にある、test が True となる側の値 (ok 側の端) を返す。
#   例: 条件を満たす最大の x   -> binary_search(0, 10**18 + 1, test)
#       条件を満たす最小の x   -> binary_search(10**18, -1, test)  (test が単調増加な真偽)


def binary_search(ok, ng, test):
    while abs(ok - ng) > 1:
        mid = (ok + ng) // 2
        if test(mid):
            ok = mid
        else:
            ng = mid
    return ok
