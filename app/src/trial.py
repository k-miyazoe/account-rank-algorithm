import itertools
import simulation

def main():
    mail_probabilities_A = [0.9]
    mail_probabilities_B = [0.99]
    mail_probabilities_C = [0.99]
    refund_probabilities_A = [0.8, 0.85, 0.9, 0.99]
    refund_probabilities_B = [0.6, 0.7, 0.8, 0.9, 0.99]
    refund_probabilities_C = [0.01, 0.05, 0.1, 0.15]
    agent_ratios_A = [0.9]
    agent_ratios_B = [0.07]
    agent_ratios_C = [0.03]

    parameter_combinations = list(itertools.product(mail_probabilities_A, mail_probabilities_B, mail_probabilities_C,
                                                    refund_probabilities_A, refund_probabilities_B, refund_probabilities_C,
                                                    agent_ratios_A, agent_ratios_B, agent_ratios_C))

    total_combinations = len(parameter_combinations)
    print(f"Total combinations(試行回数): {total_combinations}")

    num_agents = 1000
    for combination in parameter_combinations:
        mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C, agent_ratio_A, agent_ratio_B, agent_ratio_C = combination
        simulation.main(num_agents,mail_prob_A, mail_prob_B, mail_prob_C, refund_prob_A, refund_prob_B, refund_prob_C, agent_ratio_A, agent_ratio_B, agent_ratio_C)
        
if __name__ == '__main__':
    main()