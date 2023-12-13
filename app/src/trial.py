from obj_sim import Simulation
import datetime
import os
import csv
import itertools


def main():
    # 100以下にするとエラーが出る
    num_agents = 1000
    mail_probabilities_A = [1]
    mail_probabilities_C = [1]
    refund_probabilities_A = [0, 0.01, 0.2, 0.4, 0.6, 0.8, 0.99, 1]
    refund_probabilities_C = [0, 0.01, 0.2, 0.4, 0.6, 0.8, 0.99, 1]
    # refund_probabilities_A = [0.6]
    # refund_probabilities_C = [0.4]
    agent_ratios_A = [0.99]
    agent_ratios_C = [0.01]

    output_folder_path = create_output_directory()
    create_params_file(num_agents, output_folder_path, mail_probabilities_A, mail_probabilities_C,
                       refund_probabilities_A,  refund_probabilities_C, agent_ratios_A, agent_ratios_C)

    parameter_combinations = list(itertools.product(mail_probabilities_A, mail_probabilities_C,
                                                    refund_probabilities_A, refund_probabilities_C,
                                                    agent_ratios_A, agent_ratios_C))

    total_combinations = len(parameter_combinations)
    print(f"Total combinations(試行回数): {total_combinations}")
    csv_file_name = create_output_csv(output_folder_path)
    ten_days_simulation = 10
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    accont_rank_csv = now + "account_rank.csv"

    for combination in parameter_combinations:
        mail_prob_A,  mail_prob_C, refund_prob_A, refund_prob_C, agent_ratio_A, agent_ratio_C = combination
        simulation = Simulation(
            num_agents, output_folder_path, agent_ratio_A, agent_ratio_C)

        simulation.create_agents_graph()
        init_graph, account_rank = simulation.run_init_simulation(
            mail_prob_A, mail_prob_C, refund_prob_A, refund_prob_C, accont_rank_csv)

        simulation.set_graph_account_rank(init_graph)
        simulation.set_graph_normal(init_graph)

        graph_rank = init_graph
        graph_normal = init_graph

        ten_days_simulation_result = [refund_prob_A,refund_prob_C,0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for j in range(1):
            graph_rank = init_graph
            graph_normal = init_graph
            sum_confi_msc_rank = 0
            sum_confi_msc_normal = 0
            
            for i in range(ten_days_simulation):
                graph_rank, ave_a_email_count_a, ave_c_email_count_a, sum_confiscation_msc_rank_c = simulation.run_simulation_with_account_rank(
                    graph_rank, account_rank, mail_prob_A, mail_prob_C, refund_prob_A, refund_prob_C)
                
                graph_normal, ave_a_email_count_n, ave_c_email_count_n, sum_confiscation_msc_normal_c = simulation.run_simulation_normal(
                    graph_normal, mail_prob_A, mail_prob_C, refund_prob_A, refund_prob_C)
                
                a_msc_rank, c_msc_rank = average_msc(graph_rank)
                a_msc, c_msc = average_msc(graph_normal)
                
                sum_confi_msc_rank += sum_confiscation_msc_rank_c
                sum_confi_msc_normal += sum_confiscation_msc_normal_c
                #noramlの没収金額が異様に大きい問題
                #print("debug noraml", sum_confi_msc_normal)
            
                ten_days_simulation_result = add_simulation_result(ten_days_simulation_result, a_msc_rank, c_msc_rank,a_msc, 
                                                                c_msc,ave_a_email_count_a, ave_c_email_count_a,
                                                                ave_a_email_count_n, ave_c_email_count_n,
                                                                sum_confi_msc_rank, sum_confi_msc_normal)
            
        ave_simulation_result = divide_simulation_result(ten_days_simulation_result, 10)

        with open(output_folder_path + csv_file_name, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(ave_simulation_result)


def create_output_directory():
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    folder_path = './output/' + now + '/'
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


def create_params_file(num_agents, dir_path, mail_probabilities_A, mail_probabilities_C, refund_probabilities_A, refund_probabilities_C, agent_ratios_A, agent_ratios_C):
    with open(dir_path + "params.txt", "w") as file:
        num_agents_text = "エージェントの数："+str(num_agents)+"\n"
        file.write(num_agents_text)
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


def create_output_csv(dir_path):
    csv_header = ["返金確率A", "返金確率C",
                  "仮想通貨の平均所持量A(rank)", "仮想通貨の平均所持量C(rank)",
                  "仮想通貨の平均所持量A(normal)", "仮想通貨の平均所持量C(normal)",
                  "平均メール送信件数A(rank)", "平均メール送信件数C(rank)",
                  "平均メール送信件数A(normal)", "平均メール送信件数C(normal)",
                  "没収されたCのmscの合計(rank)", "没収されたCのmscの合計(normal)"]
    execution_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    output_file_name = f"output_{execution_time}.csv"
    with open(dir_path + output_file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_header)
    print(f"Output file name: {output_file_name}")
    return output_file_name


def average_msc(graph):
    ave_A = 0
    ave_C = 0
    a_nodes = 0
    c_nodes = 0
    if len(graph.nodes) > 0:
        for key, value in graph.nodes.items():
            if value['agent_type'] == 'A':
                ave_A += value['msc']
                a_nodes += 1
            elif value['agent_type'] == 'C':
                ave_C += value['msc']
                c_nodes += 1
        ave_A = ave_A / a_nodes
        ave_C = ave_C / c_nodes
    else:
        print("Error: The length of graph.nodes is zero.")
        pass

    return ave_A, ave_C


def add_simulation_result(pre_result, a_msc_rank, c_msc_rank,a_msc, c_msc,ave_a_email_count_a, ave_c_email_count_a,ave_a_email_count_n, ave_c_email_count_n, sum_confiscation_msc_rank_c, sum_confiscation_msc_normal_c):
    pre_result[2] = pre_result[2] + a_msc_rank
    pre_result[3] = pre_result[3] + c_msc_rank
    pre_result[4] = pre_result[4] + a_msc
    pre_result[5] = pre_result[5] + c_msc
    pre_result[6] = pre_result[6] + ave_a_email_count_a
    pre_result[7] = pre_result[7] + ave_c_email_count_a
    pre_result[8] = pre_result[8] + ave_a_email_count_n
    pre_result[9] = pre_result[9] + ave_c_email_count_n
    pre_result[10] = pre_result[10] + sum_confiscation_msc_rank_c
    pre_result[11] = pre_result[11] + sum_confiscation_msc_normal_c
    return pre_result


def divide_simulation_result(result, num):  
    result[2] = round(result[2] / num, 2)
    result[3] = round(result[3] / num, 2)
    result[4] = round(result[4] / num, 2)
    result[5] = round(result[5] / num, 2)
    result[6] = result[6] / num
    result[7] = result[7] / num
    result[8] = result[8] / num
    result[9] = result[9] / num
    result[10] = result[10] / num
    result[11] = result[11] / num
    return result

if __name__ == "__main__":
    main()
