import networkx as nx
import random
import matplotlib.pyplot as plt
import datetime
import uuid

def create_agents_graph(num_agents):
    G = nx.Graph()
    for i in range(int(num_agents * 0.9)):
        G.add_node(f'A{i + 1}', agent_type='A')
    for i in range(int(num_agents * 0.07)):
        G.add_node(f'B{i + 1}', agent_type='B')
    for i in range(int(num_agents * 0.03)):
        G.add_node(f'C{i + 1}', agent_type='C')
    return G

def set_node_color(graph):
    agents_colors = {"A": "blue", "B": "green", "C": "red"}
    node_colors = [agents_colors.get(graph.nodes[n]['agent_type'], "gray") for n in graph.nodes]
    return node_colors

def add_a_relations(graph, num_agents):
    target_a_relations = int(0.05 * num_agents)
    a_nodes = [node for node in graph.nodes if graph.nodes[node]['agent_type'] == 'A']
    #ノードaの数だけループ(90回)
    for i in range(len(a_nodes)):
        a_ege_add_probability = random.random()
        return_edge_add_probabili = random.random()
        #5回ループ
        for j in range(target_a_relations):
            #80%の確率でエッジ追加
            if a_ege_add_probability > 0.2:
                #ここはaのノード以外のランダム性を発生させる可能性あり
                random_a_node = a_nodes[random.randint(0, len(a_nodes) - 1)]
                graph.add_edge(a_nodes[i], random_a_node)
                #90%の確率で双方向にエッジを追加
                if return_edge_add_probabili > 0.1:
                    graph.add_edge(random_a_node, a_nodes[i])

def add_b_relations(graph, num_agents):
    target_b_relations = int(0.8 * num_agents)
    a_nodes = [node for node in graph.nodes if graph.nodes[node]['agent_type'] == 'A']
    b_nodes = [node for node in graph.nodes if graph.nodes[node]['agent_type'] == 'B']
    for i in range(len(b_nodes)):
        b_ege_add_probability = random.random()
        return_edge_add_probabili = random.random()
        for j in range(target_b_relations):
            if b_ege_add_probability > 0.1:
                random_a_node = a_nodes[random.randint(0, len(a_nodes) - 1)]
                graph.add_edge(b_nodes[i], random_a_node)
                if return_edge_add_probabili > 0.3:
                    graph.add_edge(random_a_node, b_nodes[i])

def add_c_relations(graph, num_agents):
    target_c_relations = int(0.7 * num_agents)
    a_nodes = [node for node in graph.nodes if graph.nodes[node]['agent_type'] == 'A']
    c_nodes = [node for node in graph.nodes if graph.nodes[node]['agent_type'] == 'C']
    for i in range(len(c_nodes)):
        c_ege_add_probability = random.random()
        return_edge_add_probabili = random.random()
        for j in range(target_c_relations):
            if c_ege_add_probability > 0.1:
                random_a_node = a_nodes[random.randint(0, len(a_nodes) - 1)]
                graph.add_edge(c_nodes[i], random_a_node)
                if return_edge_add_probabili < 0.1:
                    graph.add_edge(random_a_node, c_nodes[i])

def display_graph_info(graph):
    print("ノード数:", len(graph.nodes))
    print("エッジ数:", len(graph.edges))

def set_agents_random_score(num_agents):
    all_agents_score = {}
    for i in range(num_agents):
        if i < int(num_agents * 0.9):
            all_agents_score[f'A{i + 1}'] = random.randint(1, 10)
        elif i < int(num_agents * 0.97):
            all_agents_score[f'B{i + 1}'] = random.randint(1, 10)
        else:
            all_agents_score[f'C{i + 1}'] = random.randint(1, 10)
    return all_agents_score

def set_agents_unified_score(num_agents):
    all_agents_score = {}
    for i in range(num_agents):
        if i < int(num_agents * 0.9):
            all_agents_score[f'A{i + 1}'] = 10
        elif i < int(num_agents * 0.97):
            all_agents_score[f'B{i + 1}'] = 10
        else:
            all_agents_score[f'C{i + 1}'] = 10
    return all_agents_score

def calculate_accountrank(graph, all_agents_score):
    return nx.pagerank(graph, alpha=0.85, personalization=all_agents_score)

def save_graph_image(agents_graph, account_rank):
    pos = nx.spring_layout(agents_graph)
    plt.figure(figsize=(10, 10))
    colors = set_node_color(agents_graph)
    nx.draw_networkx_nodes(agents_graph, pos, node_color=colors, node_size=[
                           5000*v for v in account_rank.values()])
    nx.draw_networkx_edges(agents_graph, pos)
    
    now = datetime.datetime.now()
    graph_image_file = './output_graph/graph_' + now.strftime('%Y%m%d_%H%M%S') + '.png'
    plt.savefig(graph_image_file)
    plt.axis('off')

#できればスコア情報もファイルに書き込みたい
def write_to_text_accout_rank(account_rank):
    now = str(datetime.datetime.now())
    with open('./output_text/'+ now +'.txt', mode='w') as f:
        for account in account_rank:
            f.write(account + '\n')

def main():
    num_agents = 100
    agents_graph = create_agents_graph(num_agents)
    
    add_a_relations(agents_graph, num_agents)
    add_b_relations(agents_graph, num_agents)
    add_c_relations(agents_graph, num_agents)
    
    all_agents_score = set_agents_unified_score(num_agents)
    
    account_rank = calculate_accountrank(agents_graph, all_agents_score)
    account_rank_descending_order = sorted( account_rank, key=None, reverse=False)
    
    write_to_text_accout_rank(account_rank_descending_order)
    
    display_graph_info(agents_graph)
    
    save_graph_image(agents_graph, account_rank)

if __name__ == "__main__":
    main()
