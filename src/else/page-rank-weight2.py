import random


def main():
    # PageRank初期値
    PR = {'A': 1.0, 'B': 1.0, 'C': 1.0, 'D': 1.0}
    # リンク数の逆数（確率）
    Prob = {'A': 1/3.0, 'B': 1, 'C': 1/2.0, 'D': 1/2.0}
    # 平均評価値
    Ave_Rate = {'A->B': 1.0, 'A->C': 1.0, 'A->D': 1.0, 'B->D': 1.0,
                'C->A': 1.0, 'C->D': 1.0, 'D->A': 1.0, 'D->C': 1.0}

    # 減衰率
    d = 0.85
    for i in range(15):
        new_PR_A = PR['C'] * Prob['C'] * weight(PR['C'], PR['A'], Ave_Rate['C->A']) + \
            PR['D'] * Prob['D'] * weight(PR['D'], PR['A'], Ave_Rate['D->A'])
        new_PR_B = PR['A'] * Prob['A'] * \
            weight(PR['A'], PR['B'], Ave_Rate['A->B'])
        new_PR_C = PR['A'] * Prob['A'] * weight(PR['A'], PR['C'], Ave_Rate['A->C']) + \
            PR['D'] * Prob['D'] * weight(PR['D'], PR['C'], Ave_Rate['D->C'])
        new_PR_D = PR['A'] * Prob['A'] * weight(PR['A'], PR['D'], Ave_Rate['D->A']) + PR['B'] * \
            Prob['B'] * weight(PR['B'], PR['D'], Ave_Rate['B->D']) + PR['C'] * \
            Prob['C'] * weight(PR['C'], PR['D'], Ave_Rate['C->D'])

        PR['A'] = (1-d) + d * new_PR_A
        PR['B'] = (1-d) + d * new_PR_B
        PR['C'] = (1-d) + d * new_PR_C
        PR['D'] = (1-d) + d * new_PR_D
        # 新しい値を出力
        print("%.4f %.4f %.4f %.4f" % (PR['A'], PR['B'], PR['C'], PR['D']))


def score_ratio(account1, account2):
    score_ratio = account1 / (account1 + account2)
    return score_ratio


def weight(account1, account2, average_rate):
    average_rating = average_rate
    score = score_ratio(account1, account2)
    weight = average_rating * score
    return weight


if __name__ == '__main__':
    main()
