def main():
    # PageRank初期値
    PR = {'A': 1.0, 'B': 1.0, 'C': 1.0, 'D': 1.0}
    # リンク数の逆数（確率）
    Prob = {'A': 1/3.0, 'B': 1, 'C': 1/2.0, 'D': 1/4.0}
    # 減衰率
    d = 0.85
    # 10回回す*
    for i in range(15):
        new_PR_A = PR['C'] * Prob['C'] + PR['D'] * Prob['D']
        new_PR_B = PR['A'] * Prob['A'] + PR['D'] * Prob['D']
        new_PR_C = PR['A'] * Prob['A'] + PR['D'] * Prob['D']
        new_PR_D = PR['A'] * Prob['A'] + PR['B'] * \
            Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D']

        PR['A'] = (1-d) + d * new_PR_A
        PR['B'] = (1-d) + d * new_PR_B
        PR['C'] = (1-d) + d * new_PR_C
        PR['D'] = (1-d) + d * new_PR_D
        # 新しい値を出力
        print("%.4f %.4f %.4f %.4f" % (PR['A'], PR['B'], PR['C'], PR['D']))


if __name__ == '__main__':
    main()
