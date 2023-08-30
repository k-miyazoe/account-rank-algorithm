import networkx as nx
import matplotlib.pyplot as plt
import random


def create_graph(node):
    G = nx.DiGraph()
    agents = [('エージェント{}'.format(i), {"weight": 2})
              for i in range(1, node+1)]
    G.add_nodes_from(agents)

    # すべてのエージェントをつなぐ
    for i in range(1, node+1):
        for j in range(1, node+1):
            if i != j:
                G.add_edge('エージェント{}'.format(
                    i), 'エージェント{}'.format(j))
    return G, agents


def display_node_edg(graph):
    print('ノードの数:', nx.number_of_nodes(graph))
    print('エッジの数:', nx.number_of_edges(graph))


def calculate_pagerank(graph):
    return nx.pagerank(graph, alpha=0.85)


def display_node_edg(graph):
    print('ノードの数:', nx.number_of_nodes(graph))
    print('エッジの数:', nx.number_of_edges(graph))


def display_agent_scores(scores):
    for agent, score in scores.items():
        print('{} の評価スコア: {}'.format(agent, score))


def draw_graph(graph, agents):
    # 有向グラフを生成
    G = nx.DiGraph()
    # ページランクの計算
    pagerank = nx.pagerank(G, alpha=0.85, personalization=agents)

    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 10))
    nx.draw_networkx_nodes(graph, pos, node_color=list(
        pagerank.values()), cmap=plt.cm.Reds)
    nx.draw_networkx_edges(graph, pos)
    plt.savefig("agents_graph.png")
    plt.axis('off')
    plt.show()


def main():
    graph = create_graph(20)

    display_node_edg(graph)
    pagerank_scores = calculate_pagerank(graph)
    display_agent_scores(pagerank_scores)
    draw_graph(graph, agents)


if __name__ == "__main__":
    main()
