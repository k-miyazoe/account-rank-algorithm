import itertools
import simulation
import os
import datetime

def main():
    #create_output_directory()
    mail_probabilities_A = [1]
    mail_probabilities_B = [1]
    mail_probabilities_C = [1]
    refund_probabilities_A = [0, 0.01, 0.2, 0.4, 0.6, 0.8, 0.99, 1]
    refund_probabilities_B = [0, 0.01, 0.2, 0.4, 0.6, 0.8, 0.99, 1]
    refund_probabilities_C = [0, 0.01, 0.2, 0.4, 0.6, 0.8, 0.99, 1]
    agent_ratios_A = [0.9]
    agent_ratios_B = [0.09]
    agent_ratios_C = [0.01]
    
    
    with open("params.txt", "w") as file:
        file.write("メール確率:\n")
        file.write(f"- タイプ A のメール確率: {', '.join(map(str, mail_probabilities_A))}\n")
        file.write(f"- タイプ B のメール確率: {', '.join(map(str, mail_probabilities_B))}\n")
        file.write(f"- タイプ C のメール確率: {', '.join(map(str, mail_probabilities_C))}\n\n")
        file.write("払い戻し確率:\n")
        file.write(f"- タイプ A の払い戻し確率: {', '.join(map(str, refund_probabilities_A))}\n")
        file.write(f"- タイプ B の払い戻し確率: {', '.join(map(str, refund_probabilities_B))}\n")
        file.write(f"- タイプ C の払い戻し確率: {', '.join(map(str, refund_probabilities_C))}\n\n")
        file.write("エージェント比率:\n")
        file.write(f"- タイプ A エージェント比率: {', '.join(map(str, agent_ratios_A))}\n")
        file.write(f"- タイプ B エージェント比率: {', '.join(map(str, agent_ratios_B))}\n")
        file.write(f"- タイプ C エージェント比率: {', '.join(map(str, agent_ratios_C))}\n")

    parameter_combinations = list(itertools.product(mail_probabilities_A, mail_probabilities_B, mail_probabilities_C,
                                                    refund_probabilities_A, refund_probabilities_B, refund_probabilities_C,
                                                    agent_ratios_A, agent_ratios_B, agent_ratios_C))

    total_combinations = len(parameter_combinations)
    print(f"Total combinations(試行回数): {total_combinations}")

    num_agents = 100
    for combination in parameter_combinations:
        mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C, agent_ratio_A, agent_ratio_B, agent_ratio_C = combination
        simulation.main(num_agents,mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C, agent_ratio_A, agent_ratio_B, agent_ratio_C)
        #結果を一行ずつcsvファイルに書き込む()-
        #前半でも手数料を1消費するようにする[一旦無視する]
        #返金確率A，返金確率B，返金確率C，仮想通貨の平均所持量A，平均所持量B，平均所持量C，前半の平均メール送信件数A，送信件数B，送信件数C，後半の平均メール送信件数A，送信件数B，送信件数C
        #1,1,1,900.0,90.0,10.0,4.0,18.0,72.0
        #refund_prob_A, refund_prob_B, refund_prob_C ,first_sim_a_agents_ave_msc,first_sim_b_agents_ave_msc,first_sim_c_agents_ave_msc,second_ave_a_email_count,second_ave_b_email_count,second_ave_c_email_count
   
#未完成
def create_output_directory():
    now = str(datetime.datetime.now())
    folder_path = './output/' + now + '/'
    os.makedirs(folder_path, exist_ok=True)
    with open(folder_path + now + '.txt', 'w') as file:
        file.write(now + 'シミュレーション結果\n')

if __name__ == '__main__':
    main()