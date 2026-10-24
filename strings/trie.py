# =============================================================================
# Trie 木
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   trie = Trie(sigma=26, base='a')   # 文字の種類数と、0 番目の文字。整数のリストも扱える (base=0)
#   trie.insert(word)                 # 追加 (同じ単語を何回でも追加できる)。単語の終端の頂点番号を返す
#   trie.search(word)                 # word が登録されているか
#   trie.count(word)                  # word が何回登録されたか
#   trie.count_prefix(prefix)         # prefix で始まる単語の個数 (重複込み)
#   trie.starts_with(prefix)          # prefix で始まる単語があるか
#   trie.find(word)                   # word に対応する頂点番号。無ければ -1 (根は 0)
#   trie.erase(word)                  # 1 回分削除。登録されていなければ False
#   trie.child[v][c]                  # 頂点 v の c 番目の文字の子 (無ければ -1)
#   len(trie)                         # 頂点数
# 計算量: 単語の長さに比例


class Trie:
    def __init__(self, sigma=26, base="a"):
        self.sigma = sigma
        self.base = ord(base) if isinstance(base, str) else base
        self.child = [[-1] * sigma]
        self.through = [0]  # その頂点を通る単語の数 (その頂点で終わるものも含む)
        self.ends = [0]  # その頂点で終わる単語の数

    def __len__(self):
        return len(self.child)

    def _code(self, ch):
        return (ord(ch) if isinstance(ch, str) else ch) - self.base

    def insert(self, word):
        v = 0
        self.through[0] += 1
        for ch in word:
            c = self._code(ch)
            if self.child[v][c] == -1:
                self.child[v][c] = len(self.child)
                self.child.append([-1] * self.sigma)
                self.through.append(0)
                self.ends.append(0)
            v = self.child[v][c]
            self.through[v] += 1
        self.ends[v] += 1
        return v

    def find(self, word):
        v = 0
        for ch in word:
            v = self.child[v][self._code(ch)]
            if v == -1:
                return -1
        return v

    def search(self, word):
        v = self.find(word)
        return v != -1 and self.ends[v] > 0

    def count(self, word):
        v = self.find(word)
        return 0 if v == -1 else self.ends[v]

    def count_prefix(self, prefix):
        v = self.find(prefix)
        return 0 if v == -1 else self.through[v]

    def starts_with(self, prefix):
        return self.count_prefix(prefix) > 0

    def erase(self, word):
        if not self.search(word):
            return False
        v = 0
        self.through[0] -= 1
        for ch in word:
            v = self.child[v][self._code(ch)]
            self.through[v] -= 1
        self.ends[v] -= 1
        return True
