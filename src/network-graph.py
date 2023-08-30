import networkx as nx
import matplotlib.pyplot as plt
import random


def create_agents_graph(node):
    G = nx.DiGraph()
    agents = [('エージェント{}'.format(i))
              for i in range(1, node+1)]
    G.add_nodes_from(agents)
    # すべてのエージェントをつなぐ
    for i in range(1, node+1):
        for j in range(1, node+1):
            if i != j:
                G.add_edge('エージェント{}'.format(
                    i), 'エージェント{}'.format(j))
    return G


def set_agents_weight(node):
    random_agents = {'エージェント{}'.format(i): random.uniform(
        0, 1) for i in range(1, node+1)}
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
    nx.draw_networkx_nodes(graph, pos, node_color=list(
        pagerank.values()), cmap=plt.cm.Blues)
    nx.draw_networkx_edges(graph, pos)
    plt.savefig("agents_graph.png")
    plt.axis('off')
    plt.show()


def main():
    node = int(input('ノード数を入力してください: '))
    directed_graph = create_agents_graph(node)
    agents = set_agents_weight(node)
    pagerank = calculate_pagerank(directed_graph, agents)
    display_agent_scores(pagerank)
    draw_graph(directed_graph, agents, pagerank)


if __name__ == "__main__":
    main()
