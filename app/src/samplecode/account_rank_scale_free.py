import networkx as nx
import matplotlib.pyplot as plt
import random
import sys
import datetime
import numpy as np


def create_scale_free_graph(node):
    # 各エージェントの割合を設定
    agent_ratios = [0.9, 0.07, 0.03]
    # 各エージェントの数を計算
    total_agents = node
    agent_counts = [int(total_agents * ratio) for ratio in agent_ratios]
    # エージェントリストを生成
    agents = []
    for i, count in enumerate(agent_counts):
        agents.extend(['エージェント{}'.format(i+1)] * count)
    random.shuffle(agents)
    G = nx.scale_free_graph(node, alpha=0.41)
    G.add_nodes_from(agents)
    return G

def set_agents_score(node):
    random_agents = {'エージェント{}'.format(i): random.randint(1, 10) for i in range(1, node)}
    #random_agents['評価の低いエージェント'] = random.uniform(0, 0.2)
    random_agents['評価の低いエージェント'] = 0.1
    return random_agents

def calculate_pagerank(graph, agents):
    return nx.pagerank(graph, alpha=0.85, personalization=agents)

def write_agent_scores_to_file(scores, filename):
    with open(filename, 'w') as file:
        for agent, score in scores.items():
            file.write(f'{agent} の評価スコア: {score}\n')

def display_agent_scores(scores):
    for agent, score in scores.items():
        write_agent_scores_to_file(scores, 'scores.txt')

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
