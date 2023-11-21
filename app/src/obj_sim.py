import networkx as nx
import random
import matplotlib.pyplot as plt
import datetime
import csv
import os


class Agent:
    def __init__(self, name, agent_type, msc=500, commission=0):
        self.name = name
        self.agent_type = agent_type
        self.msc = msc
        self.commission = commission


class AgentsGraph:
    def __init__(self):
        self.graph = nx.Graph()
    
    def add_agent(self, agent):
        self.graph.add_node(agent.name, agent_type=agent.agent_type, msc=agent.msc, commission=agent.commission)
    
    def add_edge(self, node_from, node_to):
        self.graph.add_edge(node_from, node_to)
    
    def set_node_color(self):
        agents_colors = {"A": "blue", "B": "green", "C": "red"}
        node_colors = [agents_colors.get(
            self.graph.nodes[n]['agent_type'], "gray") for n in self.graph.nodes]
        return node_colors
    
    def send_msc(self, node_from, node_to, commission=0):
        self.graph.nodes[node_from]['msc'] = self.graph.nodes[node_from]['msc'] - (1 + commission)
        self.graph.nodes[node_to]['msc'] = self.graph.nodes[node_to]['msc'] + (1 + commission)
    
    def set_agents_unified_score(self, num_agents):
        all_agents_score = {}
        for i in range(int(num_agents * 0.9)):
            all_agents_score[f'A{i + 1}'] = 10
        for j in range(int(num_agents * 0.07)):
            all_agents_score[f'B{j + 1}'] = 10
        for k in range(int(num_agents * 0.03)):
            all_agents_score[f'C{k + 1}'] = 10
        return all_agents_score
    
    #graphを返さなくていいか気になる
    def fee_payment(self, node_from, commission=0):
        if self.graph.nodes[node_from]['msc'] < commission + 1:
            return False
        else:
            self.graph.nodes[node_from]['msc'] = self.graph.nodes[node_from]['msc'] - commission
            return True

class Simulation:
    def __init__(self, num_agents, output_file_name, output_folder_path,a_rate=0.9, b_rate=0.09, c_rate=0.01):
        self.num_agents = num_agents
        self.output_file_name = output_file_name
        self.output_folder_path = output_folder_path
        self.agents_graph = AgentsGraph()
        self.a_agents = int(self.num_agents * a_rate)
        self.b_agents = int(self.num_agents * b_rate)
        self.c_agents = int(self.num_agents * c_rate)
    
    #first simulationのみ
    def create_agents_graph(self):
        for i in range(self.a_agents):
            agent = Agent(f'A{i + 1}', 'A', msc=500, commission=0)
            self.agents_graph.add_agent(agent)
        for i in range(int(self.b_agents)):
            agent = Agent(f'B{i + 1}', 'B', msc=500, commission=0)
            self.agents_graph.add_agent(agent)
        for i in range(int(self.c_agents)):
            agent = Agent(f'C{i + 1}', 'C', msc=500, commission=0)
            self.agents_graph.add_agent(agent)
    
    #重要関数
    def add_relations(self, graph, agent_type, mail_prob, refund_prob):
        target_relations = {
            'A': 0.05,
            'B': 0.2,
            'C': 0.8
        }
        a_nodes = [node for node in self.agents_graph.graph.nodes if self.agents_graph.graph.nodes[node]['agent_type'] == 'A']
        agent_nodes = [node for node in self.agents_graph.graph.nodes if self.agents_graph.graph.nodes[node]['agent_type'] == agent_type]
        email_count = 0
        for i in range(len(agent_nodes)):
            target_count = int(target_relations[agent_type] * self.a_agents)
            for j in range(target_count):
                if random.random() < mail_prob:
                    #この行がうまくいくか気になる
                    send_msc_flag = self.agents_graph.fee_payment(agent_nodes[i], self.agents_graph.graph.nodes[agent_nodes[i]]['commission'])
                    if send_msc_flag:
                        random_a_node = a_nodes[random.randint(0, len(a_nodes) - 1)]
                        self.agents_graph.send_msc(agent_nodes[i], random_a_node, self.agents_graph.graph.nodes[agent_nodes[i]]['commission'])
                        self.agents_graph.add_edge(agent_nodes[i], random_a_node)
                        email_count += 1
                        if random.random() < refund_prob:
                            self.agents_graph.send_msc(random_a_node, agent_nodes[i], self.agents_graph.graph.nodes[agent_nodes[i]]['commission'])
                            self.agents_graph.add_edge(random_a_node, agent_nodes[i])
        ave_email_count = int(email_count / len(agent_nodes))
        return graph, ave_email_count
    
    #ok
    def display_graph_info(self):
        print("ノード数:", len(self.agents_graph.graph.nodes))
        print("エッジ数:", len(self.agents_graph.graph.edges))
    
    #この関数は1回回すか、複数回回すか
    def apply_account_rank(self, account_rank):
        #rank score順にソート
        rank_score_data = sorted(account_rank.items(), key=lambda x: x[1], reverse=True)
        rank_data = {}
        rank = 1

        for i in range(len(rank_score_data)):
            rank_data[rank_score_data[i][0]] = rank
            rank += 1

        new_graph = nx.Graph()
        
        for key, value in self.agents_graph.graph.nodes.items():
            new_graph.add_node(key, agent_type=value['agent_type'], msc=value['msc'], commission=value['commission'])
            
        for key, value in rank_data.items():
            if key in new_graph.nodes:
                new_graph.nodes[key]['commission'] = self.calculate_email_remittance_fees(value)
        return new_graph
    
    def calculate_accountrank(self,graph, all_agents_score):
        return nx.pagerank(graph, alpha=0.85, personalization=all_agents_score)

    #ok
    def calculate_email_remittance_fees(self, rank):
        return int(1 / (1 / rank))
    
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
                new_graph.nodes[key]['commission'] = self.calculate_email_remittance_fees(value)
        return new_graph

    def copy_graph_only_nodes(self, graph):
        new_graph = nx.Graph()
        for key, value in graph.nodes.items():
            new_graph.add_node(key, agent_type=value['agent_type'], msc=value['msc'], commission=value['commission'])
        return new_graph
    
    #ok
    def save_graph_image(self, agents_graph,  output_folder_path, simulation_type):
        pos = nx.spring_layout(agents_graph)
        plt.figure(figsize=(5, 5))
        colors = self.agents_graph.set_node_color()
        nx.draw_networkx_nodes(agents_graph, pos, node_color=colors, node_size=100)
        nx.draw_networkx_edges(agents_graph, pos, width=0.01)
        graph_folder = self.output_folder_path + 'output_graph/'
        os.makedirs(graph_folder, exist_ok=True)
        now = datetime.datetime.now()
        graph_image_file = graph_folder + \
            now.strftime('%Y%m%d_%H%M%S') + simulation_type + '.png'
        plt.savefig(graph_image_file)
        plt.axis('off')
        plt.close()
    
    def run_init_simulation(self, mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C):
        self.create_agents_graph()
        init_graph = self.agents_graph.graph
        init_graph,ave_a_email_count = self.add_relations(init_graph,'A',mail_prob_A,refund_prob_A)
        init_graph,ave_b_email_count = self.add_relations(init_graph,'B',mail_prob_B,refund_prob_B)
        inti_graph,ave_c_email_count = self.add_relations(init_graph,'C',mail_prob_C,refund_prob_C)
        
        set_socre_agents = self.agents_graph.set_agents_unified_score(self.num_agents)
        account_rank_graph = self.apply_account_rank(set_socre_agents)
        account_rank = self.calculate_accountrank(account_rank_graph, set_socre_agents)
        #email_countは返した方がいいか検討すること
        #init_graphがaccout_rank_graphになるか検討すること,引数のgraph情報はaccount_rank_graph or init_graph
        return account_rank_graph, account_rank
    
    def run_simulation_with_account_rank(self, graph, account_rank, mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C):
        account_rank_graph = self.commission_settings_for_each_agent(graph, account_rank)
        account_rank_graph, ave_a_email_count = self.add_relations(account_rank_graph, 'A', mail_prob_A, refund_prob_A)
        account_rank_graph, ave_b_email_count = self.add_relations(account_rank_graph, 'B', mail_prob_B, refund_prob_B)
        account_rank_graph, ave_c_email_count = self.add_relations(account_rank_graph, 'C', mail_prob_C, refund_prob_C)
        self.save_graph_image(account_rank_graph, self.output_folder_path, 'account_rank')
        return account_rank_graph, ave_a_email_count, ave_b_email_count, ave_c_email_count
        
    def run_simulation_normal(self, graph, mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C):
        normal_graph = self.copy_graph_only_nodes(graph)
        normal_graph, ave_a_email_count = self.add_relations(normal_graph, 'A', mail_prob_A, refund_prob_A)
        normal_graph, ave_b_email_count = self.add_relations(normal_graph, 'B', mail_prob_B, refund_prob_B)
        normal_graph, ave_c_email_count = self.add_relations(normal_graph, 'C', mail_prob_C, refund_prob_C)
        self.save_graph_image(normal_graph, self.output_folder_path, 'normal')
        return normal_graph, ave_a_email_count, ave_b_email_count, ave_c_email_count