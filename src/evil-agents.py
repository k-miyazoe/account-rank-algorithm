import networkx as nx
import matplotlib.pyplot as plt
import random


# def create_agents_graph(node):
#     G = nx.DiGraph()
#     agents = [('エージェント{}'.format(i)) for i in range(1, node+1)]
#     G.add_nodes_from(agents)

#     # すべてのエージェントをつなぐ
#     # ランダムに繋ぐことがかのう
#     for i in range(1, node+1):
#         for j in range(1, node+1):
#             if i != j:
#                 G.add_edge('エージェント{}'.format(i), 'エージェント{}'.format(j))

#     # 悪意のあるエージェントを追加
#     malicious_agent = '悪意のあるエージェント'
#     G.add_node(malicious_agent)

#     # 悪意のあるエージェントと他のエージェントをつなぐ
#     for agent in agents:
#         if agent != malicious_agent:
#             G.add_edge(malicious_agent, agent)

#     return G

def create_scale_free_graph(node):
    agents = [('エージェント{}'.format(i)) for i in range(1, node+1)]
    low_rating_agent = '評価の低いエージェント'
    agents.append(low_rating_agent)
    
    G = nx.scale_free_graph(node+1, alpha=0.41)
    G.add_nodes_from(agents)
    return G

def set_agents_weight(node):
    random_agents = {'エージェント{}'.format(i): 1 for i in range(1, node+1)}
    # 評価スコアを低く設定
    random_agents['評価の低いエージェント'] = random.uniform(0, 0.2)
    return random_agents

def calculate_pagerank(graph, agents):
    return nx.pagerank(graph, alpha=0.85, personalization=agents)


def display_agent_scores(scores):
    for agent, score in scores.items():
        print('{} の評価スコア: {}'.format(agent, score))


def draw_graph(graph, agents, pagerank):
    pos = nx.spring_layout(graph)
    pagerank = pagerank
    plt.figure(figsize=(10, 10))
    nx.draw_networkx_nodes(graph, pos, node_size=[
                           5000*v for v in pagerank.values()])
    nx.draw_networkx_edges(graph, pos)
    plt.savefig("agents_graph.png")
    plt.axis('off')
    plt.show()


def main():
    node = int(input('ノード数を入力してください: '))
    scale_free_network = create_scale_free_graph(node)
    agents_weight = set_agents_weight(node)
    pagerank = calculate_pagerank(scale_free_network, agents_weight)
    display_agent_scores(pagerank)
    draw_graph(scale_free_network, agents_weight, pagerank)


if __name__ == "__main__":
    main()
