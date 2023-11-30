from obj_sim import Simulation
import datetime
import os
import csv
import itertools


def main():
    num_agents = 500
    mail_probabilities_A = [1]
    mail_probabilities_C = [1]
    # refund_probabilities_A = [0, 0.01, 0.2, 0.4, 0.6, 0.8, 0.99, 1]
    # refund_probabilities_B = [0, 0.01, 0.2, 0.4, 0.6, 0.8, 0.99, 1]
    # refund_probabilities_C = [0, 0.01, 0.2, 0.4, 0.6, 0.8, 0.99, 1]
    refund_probabilities_A = [0.9]
    refund_probabilities_C = [0.1]
    agent_ratios_A = [0.99]
    agent_ratios_C = [0.01]

    output_folder_path = create_output_directory()
    create_params_file(output_folder_path, mail_probabilities_A, mail_probabilities_C,
                       refund_probabilities_A,  refund_probabilities_C, agent_ratios_A, agent_ratios_C)

    parameter_combinations = list(itertools.product(mail_probabilities_A, mail_probabilities_C,
                                                    refund_probabilities_A, refund_probabilities_C,
                                                    agent_ratios_A, agent_ratios_C))

    total_combinations = len(parameter_combinations)
    print(f"Total combinations(試行回数): {total_combinations}")

    for combination in parameter_combinations:
        csv_folder_index = 1
        csv_index = csv_folder_index
        csv_file_name = create_output_csv(output_folder_path, csv_index)

        mail_prob_A,  mail_prob_C, refund_prob_A, refund_prob_C, agent_ratio_A, agent_ratio_C = combination
        simulation = Simulation(num_agents, csv_file_name, output_folder_path,
                                agent_ratio_A, agent_ratio_C)
        # 1回のみ
        simulation.create_agents_graph()
        init_graph, account_rank = simulation.run_init_simulation(
            mail_prob_A, mail_prob_C, refund_prob_A, refund_prob_C)

        simulation.set_graph_account_rank(init_graph)
        simulation.set_graph_normal(init_graph)

        graph_rank = init_graph
        graph_normal = init_graph

        # forで本シミュレーションが収束するまで回す(要検討) @high
        for i in range(10):
            graph_rank, ave_a_email_count_a, ave_c_email_count_a = simulation.run_simulation_with_account_rank(
                graph_rank, account_rank, mail_prob_A, mail_prob_C, refund_prob_A, refund_prob_C)
            graph_normal, ave_a_email_count_n, ave_c_email_count_n = simulation.run_simulation_normal(
                graph_normal, mail_prob_A, mail_prob_C, refund_prob_A, refund_prob_C)
            a_msc_rank, c_msc_rank = average_msc(graph_rank)
            a_msc, c_msc = average_msc(graph_normal)
            simulation_result = [refund_prob_A,  refund_prob_C,
                                 a_msc_rank, c_msc_rank,
                                 a_msc, c_msc,
                                 ave_a_email_count_a, ave_c_email_count_a,
                                 ave_a_email_count_n, ave_c_email_count_n]

            with open(output_folder_path + csv_file_name, 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(simulation_result)

        csv_folder_index += 1


def create_output_directory():
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    folder_path = './output/' + now + '/'
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def create_params_file(dir_path, mail_probabilities_A, mail_probabilities_C, refund_probabilities_A, refund_probabilities_C, agent_ratios_A, agent_ratios_C):
    with open(dir_path + "params.txt", "w") as file:
        file.write("メール確率:\n")
        file.write(
            f"- タイプ A のメール確率: {', '.join(map(str, mail_probabilities_A))}\n")
        file.write(
            f"- タイプ C のメール確率: {', '.join(map(str, mail_probabilities_C))}\n\n")
        file.write("払い戻し確率:\n")
        file.write(
            f"- タイプ A の払い戻し確率: {', '.join(map(str, refund_probabilities_A))}\n")
        file.write(
            f"- タイプ C の払い戻し確率: {', '.join(map(str, refund_probabilities_C))}\n\n")
        file.write("エージェント比率:\n")
        file.write(
            f"- タイプ A エージェント比率: {', '.join(map(str, agent_ratios_A))}\n")
        file.write(
            f"- タイプ C エージェント比率: {', '.join(map(str, agent_ratios_C))}\n")


def create_output_csv(dir_path, csv_index):
    csv_header = ["返金確率A", "返金確率C",
                  "仮想通貨の平均所持量A(rank)", "仮想通貨の平均所持量C(rank)",
                  "仮想通貨の平均所持量A(normal)", "仮想通貨の平均所持量C(normal)",
                  "平均メール送信件数A(rank)", "平均メール送信件数C(rank)",
                  "平均メール送信件数A(normal)", "平均メール送信件数C(normal)"]
    execution_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    output_file_name = f"output_{execution_time + str(csv_index)}.csv"
    with open(dir_path + output_file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_header)
    print(f"Output file name: {output_file_name}")
    return output_file_name


def average_msc(graph):
    ave_A = 0
    ave_C = 0
    if len(graph.nodes) > 0:
        for key, value in graph.nodes.items():
            if value['agent_type'] == 'A':
                ave_A += value['msc']
            elif value['agent_type'] == 'C':
                ave_C += value['msc']
        ave_A = ave_A / len(graph.nodes)
        ave_C = ave_C / len(graph.nodes)
    else:
        print("Error: The length of graph.nodes is zero.")
        pass

    return ave_A, ave_C


if __name__ == "__main__":
    main()
