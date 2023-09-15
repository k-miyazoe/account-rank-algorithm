import networkx as nx
import matplotlib.pyplot as plt
import random
import sys
import datetime

def create_scale_free_graph(node):
    agents = [('エージェント{}'.format(i)) for i in range(1, node+1)]
    low_score_agent = '評価の低いエージェント'
    agents.append(low_score_agent)
    G = nx.scale_free_graph(node+1, alpha=0.41)
    G.add_nodes_from(agents)
    return G

def set_agents_score(node):
    random_agents = {'エージェント{}'.format(i): 1 for i in range(1, node+1)}
    random_agents['評価の低いエージェント'] = random.uniform(0, 0.2)
    return random_agents

def calculate_pagerank(graph, agents):
    return nx.pagerank(graph, alpha=0.85, personalization=agents)

def display_agent_scores(scores):
    for agent, score in scores.items():
        print(f'{agent} の評価スコア: {score}')

def save_graph_image():
    now = datetime.datetime.now()
    graph_image_file = './output/graph_' + now.strftime('%Y%m%d_%H%M%S') + '.png'
    return graph_image_file

def draw_graph(graph, pagerank):
    pos = nx.spring_layout(graph)
    #指定されたサイズの新しい図が作成
    plt.figure(figsize=(100, 100))
    nx.draw_networkx_nodes(graph, pos, node_size=[
                           5000*v for v in pagerank.values()])
    nx.draw_networkx_edges(graph, pos)
    graph_image = save_graph_image()
    #図をファイルに保存
    plt.savefig(graph_image)
    #グラフの軸を非表示に設定
    plt.axis('off')

def main():
    num_agents = int(input('エージェントの数を入力してください: '))
    scale_free_network = create_scale_free_graph(num_agents)
    all_agents_score = set_agents_score(num_agents)
    pagerank = calculate_pagerank(scale_free_network, all_agents_score)
    display_agent_scores(pagerank)
    draw_graph(scale_free_network, pagerank)

if __name__ == "__main__":
    main()
