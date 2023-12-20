import networkx as nx
import matplotlib.pyplot as plt
import random
import datetime
import os
import csv


class Agent:
    def __init__(self, name, agent_type, msc=1000, commission=0):
        self.name = name
        self.agent_type = agent_type
        self.msc = msc
        self.commission = commission


class AgentsGraph:
    def __init__(self):
        # 空の有向グラフを作成
        self.graph = nx.DiGraph()

    def debug(self):
        print("debug agents graph class")

    def add_agent(self, agent):
        self.graph.add_node(agent.name, agent_type=agent.agent_type,
                            msc=agent.msc, commission=agent.commission)

    def add_edge(self, node_from, node_to):
        self.graph.add_edge(node_from, node_to)

    # ok
    def set_node_color(self):
        agents_colors = {"A": "blue", "C": "red"}
        node_colors = [agents_colors.get(
            self.graph.nodes[n]['agent_type'], "gray") for n in self.graph.nodes]
        return node_colors

    # ok
    def send_msc(self, node_from, node_to, commission=0):
        self.graph.nodes[node_from]['msc'] = self.graph.nodes[node_from]['msc'] - \
            (1 + commission)
        self.graph.nodes[node_to]['msc'] = self.graph.nodes[node_to]['msc'] + \
            (1 + commission)

    # 全エージェントの初期のランクスコアを設定(どんな値を取ろうが関係ない)
    def set_agents_unified_score(self, num_agents):
        all_agents_score = {}
        for i in range(int(num_agents * 0.99)):
            all_agents_score[f'A{i + 1}'] = 10
        for k in range(int(num_agents * 0.01)):
            all_agents_score[f'C{k + 1}'] = 10
        return all_agents_score


class Simulation:
    def __init__(self, num_agents, output_folder_path, a_rate=0.99, c_rate=0.01):
        self.num_agents = num_agents
        self.output_folder_path = output_folder_path

        self.agents_graph = AgentsGraph()
        self.agents_graph_account_rank = AgentsGraph()
        self.agents_graph_normal = AgentsGraph()

        self.a_agents = int(self.num_agents * a_rate)
        self.c_agents = int(self.num_agents * c_rate)

    def create_agents_graph(self):
        for i in range(self.a_agents):
            agent = Agent(f'A{i + 1}', 'A', msc=1000, commission=0)
            self.agents_graph.add_agent(agent)
        for i in range(int(self.c_agents)):
            agent = Agent(f'C{i + 1}', 'C', msc=1000, commission=0)
            self.agents_graph.add_agent(agent)

    def fee_payment(self, graph, node_from, commission=0):
        if graph.nodes[node_from]['msc'] - (commission + 1) < 0:
            return False
        else:
            return True

    def number_of_emails_sent(self,agent_type):
        if (agent_type == 'A'):
            return 15
        #スパマーが1日にどれくらいメールするかわからない
        elif (agent_type == 'C'):
            return min(100,self.num_agents * 0.8)

    def add_relations(self, agent_type, mail_prob, refund_prob):
        a_nodes = [
            node for node in self.agents_graph.graph.nodes if self.agents_graph.graph.nodes[node]['agent_type'] == 'A']
        agent_nodes = [
            node for node in self.agents_graph.graph.nodes if self.agents_graph.graph.nodes[node]['agent_type'] == agent_type]
        email_count = 0
        for i in range(len(agent_nodes)):
            target_count = self.number_of_emails_sent(agent_type)
            for j in range(target_count):
                if random.random() < mail_prob:
                    send_msc_flag = self.fee_payment(
                        self.agents_graph.graph, agent_nodes[i], self.agents_graph.graph.nodes[agent_nodes[i]]['commission'])
                    if send_msc_flag:
                        random_a_node = a_nodes[random.randint(
                            0, len(a_nodes) - 1)]
                        self.agents_graph.send_msc(
                            agent_nodes[i], random_a_node, self.agents_graph.graph.nodes[agent_nodes[i]]['commission'])
                        self.agents_graph.add_edge(
                            agent_nodes[i], random_a_node)
                        email_count += 1
                        if random.random() < refund_prob:
                            self.agents_graph.send_msc(
                                random_a_node, agent_nodes[i], self.agents_graph.graph.nodes[agent_nodes[i]]['commission'])
                            self.agents_graph.add_edge(
                                random_a_node, agent_nodes[i])

    def add_relations_account_rank(self, agent_type, mail_prob, refund_prob):
        a_nodes = [node for node in self.agents_graph_account_rank.graph.nodes if self.agents_graph_account_rank.graph.nodes[node]['agent_type'] == 'A']
        agent_nodes = [
            node for node in self.agents_graph_account_rank.graph.nodes if self.agents_graph_account_rank.graph.nodes[node]['agent_type'] == agent_type]
        email_count = 0
        sum_confiscation_msc = 0
        for i in range(len(agent_nodes)):
            target_count = self.number_of_emails_sent(agent_type)
            for j in range(target_count):
                if random.random() < mail_prob:
                    send_msc_flag = self.fee_payment(
                        self.agents_graph_account_rank.graph, agent_nodes[i], self.agents_graph_account_rank.graph.nodes[agent_nodes[i]]['commission'])
                    if send_msc_flag:
                        random_a_node = a_nodes[random.randint(
                            0, len(a_nodes) - 1)]
                        self.agents_graph_account_rank.send_msc(
                            agent_nodes[i], random_a_node, self.agents_graph_account_rank.graph.nodes[agent_nodes[i]]['commission'])
                        self.agents_graph_account_rank.add_edge(
                            agent_nodes[i], random_a_node)
                        email_count += 1
                        if random.random() < refund_prob:
                            self.agents_graph_account_rank.send_msc(
                                random_a_node, agent_nodes[i], self.agents_graph_account_rank.graph.nodes[agent_nodes[i]]['commission'])
                            self.agents_graph_account_rank.add_edge(
                                random_a_node, agent_nodes[i])
                        elif agent_type == 'C':
                            sum_confiscation_msc += self.agents_graph_account_rank.graph.nodes[agent_nodes[i]]['commission']
                            
        ave_email_count = int(email_count / len(agent_nodes))
        return ave_email_count, sum_confiscation_msc

    def add_relations_normal(self, agent_type, mail_prob, refund_prob):
        a_nodes = [
            node for node in self.agents_graph_normal.graph.nodes if self.agents_graph_normal.graph.nodes[node]['agent_type'] == 'A']
        agent_nodes = [
            node for node in self.agents_graph_normal.graph.nodes if self.agents_graph_normal.graph.nodes[node]['agent_type'] == agent_type]
        email_count = 0
        sum_confiscation_msc = 0
        for i in range(len(agent_nodes)):
            target_count = self.number_of_emails_sent(agent_type)
            for j in range(target_count):
                if random.random() < mail_prob:
                    send_msc_flag = self.fee_payment(
                        self.agents_graph_normal.graph, agent_nodes[i], 0)
                    # メール送信の通貨送金
                    if send_msc_flag:
                        random_a_node = a_nodes[random.randint(
                            0, len(a_nodes) - 1)]
                        self.agents_graph_normal.send_msc(
                            agent_nodes[i], random_a_node, 0)
                        self.agents_graph_normal.add_edge(
                            agent_nodes[i], random_a_node)
                        email_count += 1
                        # 通貨返金
                        if random.random() < refund_prob:
                            self.agents_graph_normal.send_msc(
                                random_a_node, agent_nodes[i], 0)
                            self.agents_graph_normal.add_edge(
                                random_a_node, agent_nodes[i])
                        #返金されないかつスパマーの場合
                        elif agent_type == 'C':
                            sum_confiscation_msc += self.agents_graph_normal.graph.nodes[agent_nodes[i]]['commission']
        ave_email_count = int(email_count / len(agent_nodes))
        return ave_email_count, sum_confiscation_msc

    def apply_account_rank(self, account_rank):
        # rank score順にソート
        rank_score_data = sorted(account_rank.items(),
                                 key=lambda x: x[1], reverse=True)
        rank_data = {}
        rank = 1

        for i in range(len(rank_score_data)):
            rank_data[rank_score_data[i][0]] = rank
            rank += 1

        new_graph = nx.Graph()
        for key, value in self.agents_graph.graph.nodes.items():
            new_graph.add_node(
                key, agent_type=value['agent_type'], msc=value['msc'], commission=value['commission'])
        for key, value in self.agents_graph.graph.edges.items():
            node_from = key[0]
            node_to = key[1]
            new_graph.add_edge(node_from, node_to)
        for key, value in rank_data.items():
            if key in new_graph.nodes:
                new_graph.nodes[key]['commission'] = self.calculate_email_remittance_fees(
                    value)
        return new_graph

    def calculate_account_rank(self, graph, all_agents_score):
        return nx.account_rank(graph, alpha=0.85, personalization=all_agents_score)

    # 手数料をここで設定
    def calculate_email_remittance_fees(self, rank):
        return min(100, rank)

    def commission_settings_for_each_agent(self, graph, account_rank):
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
            if key in new_graph.nodes:
                new_graph.nodes[key]['commission'] = self.calculate_email_remittance_fees(
                    value)
        return new_graph

    def copy_graph_only_nodes(self, graph):
        new_graph = nx.Graph()
        for key, value in graph.nodes.items():
            new_graph.add_node(
                key, agent_type=value['agent_type'], msc=value['msc'], commission=value['commission'])
        return new_graph

    def save_graph_image(self, agents_graph, simulation_type):
        pos = nx.spring_layout(agents_graph)
        plt.figure(figsize=(5, 5))
        # self.agents_graphの使用は危険
        colors = self.agents_graph.set_node_color()
        nx.draw_networkx_nodes(
            agents_graph, pos, node_color=colors, node_size=100)
        nx.draw_networkx_edges(agents_graph, pos, width=0.01)
        graph_folder = self.output_folder_path + 'output_graph/'
        os.makedirs(graph_folder, exist_ok=True)
        now = datetime.datetime.now()
        graph_image_file = graph_folder + \
            now.strftime('%Y%m%d_%H%M%S') + simulation_type + '.png'
        plt.savefig(graph_image_file)
        plt.axis('off')
        plt.close()

    def set_graph_account_rank(self, graph):
        self.agents_graph_account_rank.graph = graph

    def set_graph_normal(self, graph):
        self.agents_graph_normal.graph = graph

    def write_account_rank(self, account_rank, account_rank_csv):
        rank_index = 1
        with open(self.output_folder_path + account_rank_csv, "a") as csvfile:
            csv_writer = csv.writer(csvfile)
            for key, value in account_rank.items():
                csv_writer.writerow([rank_index, key, value])
                rank_index += 1
    
    def run_init_simulation(self, mail_prob_A, mail_prob_C, refund_prob_A, refund_prob_C, account_rank_csv):
        self.create_agents_graph()
        self.add_relations('A', mail_prob_A, refund_prob_A)
        self.add_relations('C', mail_prob_C, refund_prob_C)
        
        account_rank = nx.pagerank(self.agents_graph.graph, alpha=0.85)
        account_rank_graph = self.apply_account_rank(account_rank)
        self.write_account_rank(account_rank, account_rank_csv)
        return account_rank_graph, account_rank

    def run_simulation_with_account_rank(self, graph, account_rank, mail_prob_A, mail_prob_C, refund_prob_A, refund_prob_C):
        account_rank_graph = self.commission_settings_for_each_agent(
            graph, account_rank)
        self.agents_graph_account_rank.graph = account_rank_graph
        ave_a_email_count, sum_confiscation_msc_rank_a = self.add_relations_account_rank(
            'A', mail_prob_A, refund_prob_A)
        ave_c_email_count, sum_confiscation_msc_rank_c = self.add_relations_account_rank(
            'C', mail_prob_C, refund_prob_C)
        return self.agents_graph_account_rank.graph, ave_a_email_count, ave_c_email_count, sum_confiscation_msc_rank_c

    def run_simulation_normal(self, graph, mail_prob_A,  mail_prob_C, refund_prob_A, refund_prob_C):
        normal_graph = self.copy_graph_only_nodes(graph)
        self.agents_graph_normal.graph = normal_graph
        ave_a_email_count, sum_confiscation_msc_normal_a = self.add_relations_normal(
            'A', mail_prob_A, refund_prob_A)
        ave_c_email_count, sum_confiscation_msc_normal_c = self.add_relations_normal(
            'C', mail_prob_C, refund_prob_C)
        return self.agents_graph_normal.graph, ave_a_email_count, ave_c_email_count, sum_confiscation_msc_normal_c
