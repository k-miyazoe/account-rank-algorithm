import itertools
import simulation
import csv
import datetime
import os


def main():
    mail_probabilities_A = [1]
    mail_probabilities_B = [1]
    mail_probabilities_C = [1]
    refund_probabilities_A = [0, 0.01, 0.2, 0.4, 0.6, 0.8, 0.99, 1]
    refund_probabilities_B = [0, 0.01, 0.2, 0.4, 0.6, 0.8, 0.99, 1]
    refund_probabilities_C = [0, 0.01, 0.2, 0.4, 0.6, 0.8, 0.99, 1]
    agent_ratios_A = [0.9]
    agent_ratios_B = [0.09]
    agent_ratios_C = [0.01]
    output_folder_path = create_output_directory()

    with open(output_folder_path + "params.txt", "w") as file:
        file.write("メール確率:\n")
        file.write(
            f"- タイプ A のメール確率: {', '.join(map(str, mail_probabilities_A))}\n")
        file.write(
            f"- タイプ B のメール確率: {', '.join(map(str, mail_probabilities_B))}\n")
        file.write(
            f"- タイプ C のメール確率: {', '.join(map(str, mail_probabilities_C))}\n\n")
        file.write("払い戻し確率:\n")
        file.write(
            f"- タイプ A の払い戻し確率: {', '.join(map(str, refund_probabilities_A))}\n")
        file.write(
            f"- タイプ B の払い戻し確率: {', '.join(map(str, refund_probabilities_B))}\n")
        file.write(
            f"- タイプ C の払い戻し確率: {', '.join(map(str, refund_probabilities_C))}\n\n")
        file.write("エージェント比率:\n")
        file.write(
            f"- タイプ A エージェント比率: {', '.join(map(str, agent_ratios_A))}\n")
        file.write(
            f"- タイプ B エージェント比率: {', '.join(map(str, agent_ratios_B))}\n")
        file.write(
            f"- タイプ C エージェント比率: {', '.join(map(str, agent_ratios_C))}\n")

    parameter_combinations = list(itertools.product(mail_probabilities_A, mail_probabilities_B, mail_probabilities_C,
                                                    refund_probabilities_A, refund_probabilities_B, refund_probabilities_C,
                                                    agent_ratios_A, agent_ratios_B, agent_ratios_C))

    total_combinations = len(parameter_combinations)
    print(f"Total combinations(試行回数): {total_combinations}")

    csv_header = ["返金確率A", "返金確率B", "返金確率C", "仮想通貨の平均所持量A", "仮想通貨の平均所持量B", "仮想通貨の平均所持量C", "前半の平均メール送信件数A",
                  "前半の平均メール送信件数B", "前半の平均メール送信件数C", "後半の平均メール送信件数A", "後半の平均メール送信件数B", "後半の平均メール送信件数C"]
    execution_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_file_name = f"output_{execution_time}.csv"
    with open(output_folder_path + output_file_name, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_header)

    num_agents = 100
    for combination in parameter_combinations:
        mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C, agent_ratio_A, agent_ratio_B, agent_ratio_C = combination
        simulation.main(num_agents, mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A,
                        refund_prob_B, refund_prob_C, agent_ratio_A, agent_ratio_B, agent_ratio_C, output_file_name, output_folder_path)


def create_output_directory():
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    folder_path = './output/' + now + '/'
    os.makedirs(folder_path, exist_ok=True)
    return folder_path


if __name__ == '__main__':
    main()
