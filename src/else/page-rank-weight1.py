def main():
    # PageRank初期値
    PR = {'A': 1.0, 'B': 1.0, 'C': 1.0, 'D': 1.0}
    # リンク数の逆数（確率）
    Prob = {'A': 1/3.0, 'B': 1, 'C': 1/2.0, 'D': 1/2.0}
    Weight = {'A->B': 1.0, 'A->C': 0.3, 'A->D': 1.0, 'B->D': 0.7,
              'C->A': 1.0, 'C->D': 0.8, 'D->A': 0.8, 'D->C': 0.6}
    # 減衰率
    d = 0.85
    for i in range(50):
        new_PR_A = PR['C'] * Prob['C'] * Weight['C->A'] + \
            PR['D'] * Prob['D'] * Weight['D->A']
        new_PR_B = PR['A'] * Prob['A'] * Weight['A->B']
        new_PR_C = PR['A'] * Prob['A'] * Weight['A->C'] + \
            PR['D'] * Prob['D'] * Weight['D->C']
        new_PR_D = PR['A'] * Prob['A'] * Weight['A->D'] + PR['B'] * \
            Prob['B'] * Weight['B->D'] + PR['C'] * Prob['C'] * Weight['C->D']

        PR['A'] = (1-d) + d * new_PR_A
        PR['B'] = (1-d) + d * new_PR_B
        PR['C'] = (1-d) + d * new_PR_C
        PR['D'] = (1-d) + d * new_PR_D
# 新しい値を出力
        print("%.4f %.4f %.4f %.4f" % (PR['A'], PR['B'], PR['C'], PR['D']))


if __name__ == '__main__':
    main()
