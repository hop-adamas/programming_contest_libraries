# =============================================================================
# Trie 木
# Source: https://github.com/hop-adamas/programming_contest_libraries
# =============================================================================
#
# 使い方
#   trie = Trie(char_size=26, base='a')
#   trie.insert(word)          # 単語を追加
#   trie.search(word)          # 単語が登録されているか
#   trie.start_with(prefix)    # prefix で始まる単語があるか
#   trie.count() / trie.size() # 登録した単語数 / 頂点数

class Trie:
    char_size: int      # 文字の種類
    base: int           # 文字の0番目
    nodes: list         # Trie木本体
    root: int           # 根

    class Node:
        distance: int        # base からの間隔をint型で表現したもの
        common: int         # いくつの文字列がこの頂点を共有しているか
        next: list[int]     # 子の頂点番号を格納。存在しなければ-1
        accept: list[int]   # 末端がこの頂点になる文字列の str_id を保存

        def __init__(self, distance, char_size):
            self.distance = distance
            self.common = 0
            self.next = [-1] * char_size
            self.accept = []

    def __init__(self, char_size, base):
        self.char_size = char_size
        self.base = base
        self.root = 0
        self.nodes = [self.Node(self.root, char_size)]

    def insert_with_id(self, word, word_id):
        node_id = 0
        for i in range(len(word)):
            char_ord = ord(word[i]) - ord(self.base)
            next_id = self.nodes[node_id].next[char_ord]
            if next_id == -1:
                next_id = len(self.nodes)
                self.nodes[node_id].next[char_ord] = len(self.nodes)
                self.nodes.append(self.Node(char_ord, self.char_size))
            self.nodes[node_id].common += 1
            node_id = next_id
        
        self.nodes[node_id].common += 1
        self.nodes[node_id].accept.append(word_id)

    def insert(self, word):
        self.insert_with_id(word, self.nodes[0].common)

    def search(self, word, prefix=False):
        node_id = 0
        for i in range(len(word)):
            char_ord = ord(word[i]) - ord(self.base)
            next_id = self.nodes[node_id].next[char_ord]
            if next_id == -1:
                return False
            node_id = next_id
        
        if prefix:
            return True
        
        return len(self.nodes[node_id].accept) > 0
    
    def start_with(self, prefix):
        return self.search(prefix, prefix=True)
    
    def count(self):
        return self.nodes[0].common
    
    def size(self):
        return len(self.nodes)
