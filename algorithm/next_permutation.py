# =============================================================================
# next_permutation (C++ の std::next_permutation 相当)
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   while True:
#       ...a を使う...
#       if not next_permutation(a): break   # a[l:r] を辞書順で次の順列にする。最後なら昇順に戻して False

def next_permutation(a: list, l: int = 0, r: int = None) -> bool:
    # a[l:r] を辞書順で次の順列に更新する。次があれば True
    if r is None:
        r = len(a)
    for i in range(r - 2, l - 1, -1):
        if a[i] < a[i + 1]:
            for j in range(r - 1, i, -1):
                if a[i] < a[j]:
                    a[i], a[j] = a[j], a[i]
                    p, q = i + 1, r - 1
                    while p < q:
                        a[p], a[q] = a[q], a[p]
                        p += 1
                        q -= 1
                    return True
    a[l:r] = a[l:r][::-1]  # 最後の順列だったので昇順に戻す (C++ と同じ挙動)
    return False
