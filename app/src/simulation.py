import networkx as nx
import random
import matplotlib.pyplot as plt
import datetime
import csv
import os


def create_agents_graph(num_agents, a_rate=0.9, b_rate=0.09, c_rate=0.01):
    G = nx.Graph()
    for i in range(int(num_agents * a_rate)):
        G.add_node(f'A{i + 1}', agent_type='A', msc=500, commission=0)
    for i in range(int(num_agents * b_rate)):
        G.add_node(f'B{i + 1}', agent_type='B', msc=500, commission=0)
    for i in range(int(num_agents * c_rate)):
        G.add_node(f'C{i + 1}', agent_type='C', msc=500, commission=0)
    return G


def set_node_color(graph):
    agents_colors = {"A": "blue", "B": "green", "C": "red"}
    node_colors = [agents_colors.get(
        graph.nodes[n]['agent_type'], "gray") for n in graph.nodes]
    return node_colors


def send_msc(node_from, node_to, graph, commission=0):
    graph.nodes[node_from]['msc'] = graph.nodes[node_from]['msc'] - (1 + commission)
    graph.nodes[node_to]['msc'] = graph.nodes[node_to]['msc'] + (1 + commission)
    return graph


def fee_payment(graph, node_from, commission=0):
    if graph.nodes[node_from]['msc'] < commission + 1:
        return False, graph
    else:
        graph.nodes[node_from]['msc'] = graph.nodes[node_from]['msc'] - commission
        return True, graph


def add_relations(graph, agent_type, a_agents, email_send_probability, refund_probability):
    target_relations = {
        'A': 0.05,
        'B': 0.2,
        'C': 0.8
    }
    
    a_nodes = [node for node in graph.nodes if graph.nodes[node]['agent_type'] == 'A']
    agent_nodes = [node for node in graph.nodes if graph.nodes[node]['agent_type'] == agent_type]
    
    email_count = 0
    
    for i in range(len(agent_nodes)):
        target_count = int(target_relations[agent_type] * a_agents)
        
        for j in range(target_count):
            if random.random() < email_send_probability:
                send_msc_flag, graph = fee_payment(graph, agent_nodes[i], graph.nodes[agent_nodes[i]]['commission'])
                
                if send_msc_flag:
                    random_a_node = a_nodes[random.randint(0, len(a_nodes) - 1)]
                    graph = send_msc(agent_nodes[i], random_a_node, graph, graph.nodes[agent_nodes[i]]['commission'])
                    graph.add_edge(agent_nodes[i], random_a_node)
                    email_count += 1
                    
                    if random.random() < refund_probability:
                        graph = send_msc(random_a_node, agent_nodes[i], graph, graph.nodes[agent_nodes[i]]['commission'])
                        graph.add_edge(random_a_node, agent_nodes[i])
    
    ave_email_count = int(email_count / len(agent_nodes))
    return graph, ave_email_count


def display_graph_info(graph):
    print("ノード数:", len(graph.nodes))
    print("エッジ数:", len(graph.edges))


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


def save_graph_image(agents_graph, account_rank, output_folder_path, simulation_type):
    pos = nx.spring_layout(agents_graph)
    plt.figure(figsize=(5, 5))
    colors = set_node_color(agents_graph)
    nx.draw_networkx_nodes(agents_graph, pos, node_color=colors, node_size=[
                           100*v for v in account_rank.values()])
    nx.draw_networkx_edges(agents_graph, pos, width=0.01)
    graph_folder = output_folder_path + 'output_graph/'
    os.makedirs(graph_folder, exist_ok=True)
    now = datetime.datetime.now()
    # graphを出力するディレクトリ作成
    graph_image_file = graph_folder + \
        now.strftime('%Y%m%d_%H%M%S') + simulation_type + '.png'
    plt.savefig(graph_image_file)
    plt.axis('off')
    # 追加 メモリを大量に消費するので閉じる
    plt.close()

#改良の余地あり
def calculating_email_remittance_fees(rank, max_fee=10):
   #return min(max_fee, max(1, max_fee // rank))
    return int(1/(1/rank))


def commission_settings_for_each_agent(graph, account_rank):
    rank_score_data = sorted(account_rank.items(),
                             key=lambda x: x[1], reverse=True)
    rank_data = {}
    rank = 1
    for i in range(len(rank_score_data)):
        rank_data[rank_score_data[i][0]] = rank
        rank += 1
    new_graph = nx.Graph()
    # graphをコピー
    for key, value in graph.nodes.items():
        new_graph.add_node(
            key, agent_type=value['agent_type'], msc=value['msc'], commission=value['commission'])
    for key, value in rank_data.items():
        new_graph.nodes[key]['commission'] = calculating_email_remittance_fees(value)
    return new_graph


def average_msc(graph):
    ave_A = 0
    ave_B = 0
    ave_C = 0
    for key, value in graph.nodes.items():
        if value['agent_type'] == 'A':
            ave_A += value['msc']
        elif value['agent_type'] == 'B':
            ave_B += value['msc']
        elif value['agent_type'] == 'C':
            ave_C += value['msc']
    ave_A = ave_A / len(graph.nodes)
    ave_B = ave_B / len(graph.nodes)
    ave_C = ave_C / len(graph.nodes)
    return ave_A, ave_B, ave_C


def first_simulation(num_agents, mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C, agent_ratio_A, agent_ratio_B, agent_ratio_C, output_folder_path):
    agents_graph = create_agents_graph(
        num_agents, agent_ratio_A, agent_ratio_B, agent_ratio_C)
    a_agents = num_agents * agent_ratio_A
    
    agents_graph, ave_a_email_count = add_relations(agents_graph, 'A', a_agents, mail_prob_A, refund_prob_A)
    agents_graph, ave_b_email_count = add_relations(agents_graph, 'B', a_agents, mail_prob_B, refund_prob_B)
    agents_graph, ave_c_email_count = add_relations(agents_graph, 'C', a_agents, mail_prob_C, refund_prob_C)
    
    all_agents_score = set_agents_unified_score(num_agents)
    account_rank = calculate_accountrank(agents_graph, all_agents_score)

    display_graph_info(agents_graph)
    save_graph_image(agents_graph, account_rank,
                     output_folder_path, simulation_type='first')
    return agents_graph, account_rank, ave_a_email_count, ave_b_email_count, ave_c_email_count


def second_simulation(previous_agents_graph, account_rank, num_agents, mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C, agent_ratio_A, output_folder_path):
    a_agents = num_agents * agent_ratio_A
    
    # アカウントランクあり
    commission_agents_graph = commission_settings_for_each_agent(
        previous_agents_graph, account_rank)
    
    commission_agents_graph, ave_a_email_count = add_relations(
        commission_agents_graph, 'A', a_agents, mail_prob_A, refund_prob_A)
    commission_agents_graph, ave_b_email_count = add_relations(
        commission_agents_graph, 'B', a_agents, mail_prob_B, refund_prob_B)
    commission_agents_graph, ave_c_email_count = add_relations(
        commission_agents_graph, 'C', a_agents, mail_prob_C, refund_prob_C)
    # アカウントランクなし
    no_account_rank_graph = previous_agents_graph
    no_account_rank_graph, ave_a_email_count_ = add_relations(
        no_account_rank_graph, 'A', a_agents, mail_prob_A, refund_prob_A)
    no_account_rank_graph, ave_b_email_count_ = add_relations(
        no_account_rank_graph, 'B', a_agents, mail_prob_B, refund_prob_B)
    no_account_rank_graph, ave_c_email_count_ = add_relations(
        no_account_rank_graph, 'C', a_agents, mail_prob_C, refund_prob_C)
    
    
    display_graph_info(commission_agents_graph)
    save_graph_image(commission_agents_graph, account_rank,
                     output_folder_path, simulation_type='second')
    return commission_agents_graph,ave_a_email_count, ave_b_email_count, ave_c_email_count, ave_a_email_count_, ave_b_email_count_, ave_c_email_count_


def main(num_agents, mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C, agent_ratio_A, agent_ratio_B, agent_ratio_C, output_file_name, output_folder_path):
    previous_agents_graph, account_rank, first_ave_a_email_count, first_ave_b_email_count, first_ave_c_email_count = first_simulation(
        num_agents, mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C, agent_ratio_A, agent_ratio_B, agent_ratio_C, output_folder_path)
    
    second_agents_graph,second_ave_a_email_count, second_ave_b_email_count, second_ave_c_email_count, second_ave_a_email_count_, second_ave_b_email_count_, second_ave_c_email_count_ = second_simulation(
        previous_agents_graph, account_rank, num_agents, mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C, agent_ratio_A, output_folder_path)
    
    second_sim_a_agents_ave_msc, second_sim_b_agents_ave_msc, second_sim_c_agents_ave_msc = average_msc(
        second_agents_graph)
    
    simulation_result = [refund_prob_A, refund_prob_B, refund_prob_C, second_sim_a_agents_ave_msc, second_sim_b_agents_ave_msc,
            second_sim_c_agents_ave_msc, first_ave_a_email_count,first_ave_b_email_count, first_ave_c_email_count,second_ave_a_email_count, second_ave_b_email_count, second_ave_c_email_count, second_ave_a_email_count_, second_ave_b_email_count_, second_ave_c_email_count_]
    
    with open(output_folder_path + output_file_name, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(simulation_result)


if __name__ == "__main__":
    main()
