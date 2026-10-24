# programming_contest_libraries
This repository is the libaries of algorithm for programming contest such as AtCoder and also includes several memos of the solutions.

These codes are written in python.

## 構成

ジャンルごとのディレクトリに分けています。各ファイルは単体でコピーして使えるように作ってあり、先頭のコメントに使い方・計算量・参考にした URL を書いています。
頂点番号・添字は特記が無い限り 0-indexed、区間は半開区間 `[l, r)` です。

| ディレクトリ | 内容 |
| --- | --- |
| data_structure/ | fenwick_tree, segment_tree, lazy_segment_tree, sparse_table, union_find, sorted_set, multiset, balancing_tree, trie, li_chao_tree |
| graph/ | bfs, dijkstra, bellman_ford, warshall_floyd, scc, lowlink, topological_sort, kruskal, max_flow, min_cost_flow, hopcroft_karp, eulerian_trail |
| tree/ | tree (HLD, 全方位木 DP など), lca |
| strings/ | suffix_array, z_algorithm, manacher, rolling_hash |
| mathematics/ | matrix, vector, combination_mod, extended_euclid, prime_factorization, pollard_rho, formal_power_series, stern_brocot_tree |
| geometry/ | plane (複素数による 2 次元幾何) |
| algorithm/ | binary_search, mo_algorithm, next_permutation |

## AtCoder のコンテスト中にコピーして使うとき

ライブラリのコードを提出に含めるときは、提出コードの先頭にこのリポジトリの URL を書いてください。

```
# https://github.com/hop-adamas/programming_contest_libraries
```
