def main():
    # PageRank初期値
    PR = {'A': 1.0, 'B': 1.0, 'C': 1.0, 'D': 1.0, 'E': 1.0, 'F': 1.0,
          'G': 1.0, 'H': 1.0, 'I': 1.0, 'J': 1.0, 'K': 1.0, 'L': 1.0,
          'M': 1.0, 'N': 1.0, 'O': 1.0, 'P': 1.0, 'Q': 1.0, 'R': 1.0,
          'S': 1.0, 'T': 1.0, 'U': 1.0}
    # リンク数の逆数（確率）
    Prob = {'A': 1/20.0, 'B': 1/20.0, 'C': 1/20.0, 'D': 1/20.0, 'E': 1/20.0, 'F': 1/20.0,
            'G': 1/20.0, 'H': 1/20.0, 'I': 1/20.0, 'J': 1/20.0, 'K': 1/20.0, 'L': 1/20.0,
            'M': 1/20.0, 'N': 1/20.0, 'O': 1/20.0, 'P': 1/20.0, 'Q': 1/20.0, 'R': 1/20.0,
            'S': 1/20.0, 'T': 1/20.0, 'U': 1/20.0}
    # 減衰率
    d = 0.85

    for i in range(30):
        new_PR_A = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_B = PR['A'] * Prob['A'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_C = PR['B'] * Prob['B'] + PR['A'] * Prob['A'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_D = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['A'] * Prob['A'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_E = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['A'] * Prob['A'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_F = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_G = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_H = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_I = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_J = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_K = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_L = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_M = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_N = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_O = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_P = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_Q = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_R = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_S = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_T = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']
        new_PR_U = PR['B'] * Prob['B'] + PR['C'] * Prob['C'] + PR['D'] * Prob['D'] + PR['E'] * Prob['E'] + PR['F'] * Prob['F'] + PR['G'] * Prob['G'] + PR['H'] * Prob['H'] + PR['I'] * Prob['I'] + PR['J'] * Prob['J'] + PR['K'] * \
            Prob['K'] + PR['L'] * Prob['L'] + PR['M'] * Prob['M'] + PR['N'] * Prob['N'] + PR['O'] * Prob['O'] + PR['P'] * \
            Prob['P'] + PR['Q'] * Prob['Q'] + PR['R'] * Prob['R'] + \
            PR['S'] * Prob['S'] + PR['T'] * Prob['T'] + PR['U'] * Prob['U']

        PR['A'] = (1-d) + d * new_PR_A
        PR['B'] = (1-d) + d * new_PR_B
        PR['C'] = (1-d) + d * new_PR_C
        PR['D'] = (1-d) + d * new_PR_D
        PR['E'] = (1-d) + d * new_PR_E
        PR['F'] = (1-d) + d * new_PR_F
        PR['G'] = (1-d) + d * new_PR_G
        PR['H'] = (1-d) + d * new_PR_H
        PR['I'] = (1-d) + d * new_PR_I
        PR['J'] = (1-d) + d * new_PR_J
        PR['K'] = (1-d) + d * new_PR_K
        PR['L'] = (1-d) + d * new_PR_L
        PR['M'] = (1-d) + d * new_PR_M
        PR['N'] = (1-d) + d * new_PR_N
        PR['O'] = (1-d) + d * new_PR_O
        PR['P'] = (1-d) + d * new_PR_P
        PR['Q'] = (1-d) + d * new_PR_Q
        PR['R'] = (1-d) + d * new_PR_R
        PR['S'] = (1-d) + d * new_PR_S
        PR['T'] = (1-d) + d * new_PR_T
        PR['U'] = (1-d) + d * new_PR_U
        # 新しい値を出力
        print(PR['A'], PR['B'], PR['C'], PR['D'], PR['E'], PR['F'], PR['G'], PR['H'], PR['I'],
              PR['J'], PR['K'], PR['L'], PR['M'], PR['N'], PR['O'], PR['P'], PR['Q'], PR['R'], PR['S'], PR['T'], PR['U'])


if __name__ == '__main__':
    main()
