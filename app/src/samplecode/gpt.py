import networkx as nx
import random
import matplotlib.pyplot as plt
import datetime

# グラフを作成
G = nx.Graph()

# エージェント数を設定
num_agents = 100

#エージェントAをエージェントの数の90%分追加する
for i in range(int(num_agents * 0.9)):
    G.add_node(f'A{i + 1}', agent_type='A')
for i in range(int(num_agents * 0.07)):
    G.add_node(f'B{i + 1}', agent_type='B')
for i in range(int(num_agents * 0.03)):
    G.add_node(f'C{i + 1}', agent_type='C')

print("ノード数:", len(G.nodes))
print("エッジ数:", len(G.edges))

num_a_relations = int(0.05 * num_agents)
a_relations = random.sample(range(1, num_agents), num_a_relations)
for node in a_relations:
    G.add_edge(random.choice([f'A{i + 1}' for i in range(int(num_agents * 0.9))]), f'A{node}')

# エージェントBの関係を追加
num_b_relations = int(0.15 * num_agents)
b_relations = random.sample(range(1, num_agents), num_b_relations)
for node in b_relations:
    if random.random() < 0.05:
        G.add_edge('B', f'A{node}')
    else:
        G.add_edge(f'A{node}', 'B')

# エージェントCの関係を追加
num_c_relations = int(0.5 * num_agents)
c_relations = random.sample(range(1, num_agents), num_c_relations)
for node in c_relations:
    if random.random() < 0.05:
        G.add_edge('C', f'A{node}')
    else:
        G.add_edge(f'A{node}', 'C')

# グラフの情報を表示
print("ノード数:", len(G.nodes))
print("エッジ数:", len(G.edges))

now = datetime.datetime.now()
graph_image_file = 'graph_' + now.strftime('%Y%m%d_%H%M%S') + '.png'

#need graph,pagerank
# pos = nx.spring_layout(graph)
# #指定されたサイズの新しい図が作成
# plt.figure(figsize=(100, 100))
# nx.draw_networkx_nodes(graph, pos, node_size=[
#                         5000*v for v in pagerank.values()])
# nx.draw_networkx_edges(graph, pos)
# graph_image = save_graph_image()
# plt.savefig(graph_image_file)
# plt.axis('off')
#グラフが表示されない問題
#エッジの繋ぎ方を完全に把握できてない