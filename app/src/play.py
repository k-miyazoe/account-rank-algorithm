import networkx as nx
import matplotlib.pyplot as plt

# 空の有向グラフを作成
G = nx.DiGraph()

# ノードの手動追加
G.add_node(1, rank_score=0.5)  # ノード1を追加し、ランクスコアを指定
G.add_node(2, rank_score=0.5)  # ノード2を追加し、ランクスコアを指定
G.add_node(3, rank_score=0.5)  # ノード3を追加し、ランクスコアを指定
G.add_node(4, rank_score=0.5)  # ノード1を追加し、ランクスコアを指定
G.add_node(5, rank_score=0.5)  # ノード2を追加し、ランクスコアを指定
G.add_node(6, rank_score=0.5)  # ノード3を追加し、ランクスコアを指定
G.add_node(7, rank_score=0.5)  # ノード1を追加し、ランクスコアを指定
G.add_node(8, rank_score=0.5)  # ノード2を追加し、ランクスコアを指定
G.add_node(9, rank_score=0.5)  # ノード3を追加し、ランクスコアを指定

# エッジの手動追加
G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(1, 4) 
G.add_edge(1, 5)
G.add_edge(1, 6)
G.add_edge(1, 7)  
G.add_edge(1, 8)
G.add_edge(1, 9)
G.add_edge(2, 3) 
G.add_edge(3, 4) 
G.add_edge(4, 5) 
G.add_edge(5, 6) 
G.add_edge(6, 7) 
G.add_edge(8, 9)
G.add_edge(9, 2)
G.add_edge(2, 9)

# ページランクの計算
pagerank = nx.pagerank(G)

# 結果の表示
# print("ページランク:")
# for node, rank in pagerank.items():
#     print(f"ノード {node}: {rank}")

print("ノードの隣接関係:", G.edges)
# グラフの描画
# pos = nx.spring_layout(G)  # グラフを描画するための座標を取得
# nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue')
# plt.show()
