import networkx as nx
import random

# グラフの生成
G = nx.gnm_random_graph(10, 20)

# ランクスコアを調整するために、ランダムに一つのノードを選択
low_rank_node = random.choice(list(G.nodes()))
print(f"ランクスコアを調整するノード: {low_rank_node}")

# ランクスコアが低くなるように、選択されたノードの入力エッジを一時的に保存
edges_to_remove = [(neighbor, low_rank_node) for neighbor in G.neighbors(low_rank_node)]

# 一時的に保存したエッジを削除
for edge in edges_to_remove:
    G.remove_edge(*edge)

# ページランクの計算
pagerank = nx.pagerank(G)

# ページランクが高い順にソート
sorted_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)

# 結果の表示
print("ページランク:")
for node, rank in sorted_pagerank:
    print(f"ノード {node}: {rank}")
