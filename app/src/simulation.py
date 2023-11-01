import networkx as nx
import random
import matplotlib.pyplot as plt
import datetime
import csv

def create_record_email_file():
    now = str(datetime.datetime.now())
    with open('./output_email/' + now + '.txt', mode='w') as f:
        f.write('')

def create_agents_graph(num_agents,a_rate=0.9,b_rate=0.09,c_rate=0.01):
    G = nx.Graph()
    for i in range(int(num_agents * a_rate)):
        G.add_node(f'A{i + 1}', agent_type='A', msc=1000, commission=0)
    for i in range(int(num_agents * b_rate)):
        G.add_node(f'B{i + 1}', agent_type='B', msc=1000, commission=0)
    for i in range(int(num_agents * c_rate)):
        G.add_node(f'C{i + 1}', agent_type='C', msc=1000, commission=0)
    return G

def set_node_color(graph):
    agents_colors = {"A": "blue", "B": "green", "C": "red"}
    node_colors = [agents_colors.get(
        graph.nodes[n]['agent_type'], "gray") for n in graph.nodes]
    return node_colors

def send_msc(node_from,node_to,graph):
    graph.nodes[node_from]['msc'] = graph.nodes[node_from]['msc'] - 1
    graph.nodes[node_to]['msc'] = graph.nodes[node_to]['msc'] + 1
    return graph

def fee_payment(graph,node_from,commission=0):
    if graph.nodes[node_from]['msc'] < 0:
        return False,graph
    else:
        graph.nodes[node_from]['msc'] = graph.nodes[node_from]['msc'] - commission
        return True, graph

def record_email_sending_info(simulation_type,a_email_count,b_email_count,c_email_count):
    file_name = str(datetime.datetime.now()) + simulation_type
    with open('./output_email/' + file_name + '.txt', mode='w') as f:
        f.write("agentA:" + str(a_email_count) + '\n')
        f.write("agentB:" + str(b_email_count) + '\n')
        f.write("agentC:" + str(c_email_count) + '\n')

def add_a_relations(graph,a_agents,email_send_probability,refund_probability):
    target_a_relations = int(0.05 * a_agents)
    a_nodes = [node for node in graph.nodes if graph.nodes[node]['agent_type'] == 'A']
    a_email_count = 0
    for i in range(len(a_nodes)):
        for j in range(target_a_relations):
            if random.random() < email_send_probability:
                random_a_node = a_nodes[random.randint(0, len(a_nodes) - 1)]
                graph.add_edge(a_nodes[i], random_a_node)
                graph = send_msc(a_nodes[i], random_a_node, graph)
                a_email_count += 1
                if random.random() < refund_probability:
                    graph = send_msc(random_a_node, a_nodes[i], graph)
                    graph.add_edge(random_a_node, a_nodes[i])
    ave_a_email_count = a_email_count / len(a_nodes)
    return graph, ave_a_email_count

def add_b_relations(graph, a_agents,email_send_probability=0.9,refund_probability=0.7):
    target_b_relations = int(0.2 * a_agents)
    a_nodes = [node for node in graph.nodes if graph.nodes[node]['agent_type'] == 'A']
    b_nodes = [node for node in graph.nodes if graph.nodes[node]['agent_type'] == 'B']
    b_email_count = 0
    for i in range(len(b_nodes)):
        for j in range(target_b_relations):
            if random.random() < email_send_probability:
                send_msc_flag,graph = fee_payment(graph, b_nodes[i], graph.nodes[b_nodes[i]]['commission'])
                if send_msc_flag:
                    random_a_node = a_nodes[random.randint(0, len(a_nodes) - 1)]
                    graph = send_msc(b_nodes[i], random_a_node, graph)
                    graph.add_edge(b_nodes[i], random_a_node)
                    b_email_count += 1
                    if random.random() < refund_probability:
                        graph = send_msc(random_a_node, b_nodes[i], graph)
                        graph.add_edge(random_a_node, b_nodes[i])
    ave_b_email_count = b_email_count / len(b_nodes)
    return graph, ave_b_email_count

def add_c_relations(graph, a_agents,email_send_probability=0.9,refund_probability=0.1):
    target_c_relations = int(0.8 * a_agents)
    a_nodes = [node for node in graph.nodes if graph.nodes[node]['agent_type'] == 'A']
    c_nodes = [node for node in graph.nodes if graph.nodes[node]['agent_type'] == 'C']
    c_email_count = 0
    for i in range(len(c_nodes)):
        for j in range(target_c_relations):
            if random.random() < email_send_probability:
                send_msc_flag,graph = fee_payment(graph, c_nodes[i], graph.nodes[c_nodes[i]]['commission'])
                if send_msc_flag:
                    random_a_node = a_nodes[random.randint(0, len(a_nodes) - 1)]
                    graph = send_msc(c_nodes[i], random_a_node, graph)
                    graph.add_edge(c_nodes[i], random_a_node)
                    c_email_count += 1
                    if random.random() < refund_probability:
                        graph = send_msc(random_a_node, c_nodes[i], graph)
                        graph.add_edge(random_a_node, c_nodes[i])
    ave_c_email_count = c_email_count / len(c_nodes)
    return graph,ave_c_email_count

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

def save_graph_image(agents_graph, account_rank, simulation_type):
    pos = nx.spring_layout(agents_graph)
    plt.figure(figsize=(5, 5))
    colors = set_node_color(agents_graph)
    nx.draw_networkx_nodes(agents_graph, pos, node_color=colors, node_size=[
                           100*v for v in account_rank.values()])
    nx.draw_networkx_edges(agents_graph, pos, width=0.01)
    now = datetime.datetime.now()
    graph_image_file = './output_graph/' + \
        now.strftime('%Y%m%d_%H%M%S') + simulation_type +'.png'
    plt.savefig(graph_image_file)
    plt.axis('off')
    #追加 メモリを大量に消費するので閉じる
    plt.close()

def calculating_email_remittance_fees(num_agents,rank):
    return int(1 / (1 / rank))

def commission_settings_for_each_agent(graph,account_rank):
    rank_score_data = sorted(account_rank.items(), key=lambda x: x[1], reverse=True)
    rank_data = {}
    rank = 1
    for i in range(len(rank_score_data)):
        rank_data[rank_score_data[i][0]] = rank
        rank += 1
    new_graph = nx.Graph()
    #graphをコピー
    for key,value in graph.nodes.items():
        new_graph.add_node(key,agent_type=value['agent_type'],msc=value['msc'],commission=value['commission'])
    for key,value in rank_data.items():
        new_graph.nodes[key]['commission'] = calculating_email_remittance_fees(len(graph.nodes),value)
    return new_graph

def average_msc(graph):
    ave_A = 0
    ave_B = 0
    ave_C = 0
    for key,value in graph.nodes.items():
        if value['agent_type'] == 'A':
            ave_A += value['msc']
        elif value['agent_type'] == 'B':
            ave_B += value['msc']
        elif value['agent_type'] == 'C':
            ave_C += value['msc']
    ave_A = ave_A / len(graph.nodes)
    ave_B = ave_B / len(graph.nodes)
    ave_C = ave_C / len(graph.nodes)
    return ave_A,ave_B,ave_C

def first_simulation(num_agents,mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C, agent_ratio_A, agent_ratio_B, agent_ratio_C):
    agents_graph = create_agents_graph(num_agents, agent_ratio_A, agent_ratio_B, agent_ratio_C)
    a_agents = num_agents * agent_ratio_A
    agents_graph,ave_a_email_count = add_a_relations(agents_graph, a_agents, mail_prob_A, refund_prob_A)
    agents_graph,ave_b_email_count = add_b_relations(agents_graph, a_agents, mail_prob_B, refund_prob_B)
    agents_garph,ave_c_email_count = add_c_relations(agents_graph, a_agents, mail_prob_C, refund_prob_C)
    #メール送信件数を記録ではなく、csvでまとめて出力するように変更する、平均メール送信件数を返り値にする
    #record_email_sending_info("first",a_email_count,b_email_count,c_email_count)
    all_agents_score = set_agents_unified_score(num_agents)
    account_rank = calculate_accountrank(agents_graph, all_agents_score)
    
    display_graph_info(agents_graph)
    save_graph_image(agents_graph, account_rank, simulation_type='first')
    return agents_graph,account_rank,ave_a_email_count,ave_b_email_count,ave_c_email_count

def second_simulation(previous_agents_graph, account_rank, num_agents, mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C, agent_ratio_A):
    a_agents = num_agents * agent_ratio_A
    commission_agents_graph = commission_settings_for_each_agent(previous_agents_graph,account_rank)
    commission_agents_graph,ave_a_email_count = add_a_relations(commission_agents_graph, a_agents, mail_prob_A, refund_prob_A)
    commission_agents_graph,ave_b_email_count = add_b_relations(commission_agents_graph, a_agents, mail_prob_B, refund_prob_B)
    commission_agents_graph,ave_c_email_count = add_c_relations(commission_agents_graph, a_agents, mail_prob_C, refund_prob_C)
    #record_email_sending_info("second",a_email_count,b_email_count,c_email_count)
    display_graph_info(commission_agents_graph)
    save_graph_image(commission_agents_graph, account_rank, simulation_type='second')
    return ave_a_email_count,ave_b_email_count,ave_c_email_count

def main(num_agents,mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C, agent_ratio_A, agent_ratio_B, agent_ratio_C):
    previous_agents_graph,account_rank,first_ave_a_email_count,first_ave_b_email_count,first_ave_c_email_count = first_simulation(num_agents,mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C, agent_ratio_A, agent_ratio_B, agent_ratio_C)
    first_sim_a_agents_ave_msc,first_sim_b_agents_ave_msc,first_sim_c_agents_ave_msc = average_msc(previous_agents_graph)
    second_ave_a_email_count,second_ave_b_email_count,second_ave_c_email_count = second_simulation(previous_agents_graph,account_rank,num_agents,mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C, agent_ratio_A)
    simulation_result = []
    data = [refund_prob_A, refund_prob_B, refund_prob_C ,first_sim_a_agents_ave_msc,first_sim_b_agents_ave_msc,first_sim_c_agents_ave_msc,second_ave_a_email_count,second_ave_b_email_count,second_ave_c_email_count]
    #simulation_result.append(data)
    #一行しか書き込まれない
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)

if __name__ == "__main__":
    main()