import numpy as np
import matplotlib.pyplot as plt

# シミュレーション1: 理想状態
spam_return = 0  # SPAMERのMSC返金率
ml_return = 100  # ML送信者のMSC返金率
user_return = 100  # 一般ユーザのMSC返金率

# シミュレーション2: 現実的なシミュレーション1
spam_return_real = 10  # SPAMERのMSC返金率
ml_return_real = 80  # ML送信者のMSC返金率
user_return_real = 90  # 一般ユーザのMSC返金率

# シミュレーション3: 現実的なシミュレーション3
n_accounts = 1000  # アカウント数
xn_values = np.random.uniform(0, 100, n_accounts)  # SPAMERとML送信者のMSC返金率をランダム生成

# メール送信数とメール受信数
email_sent = 100000  # 仮想的なメール送信数
email_received = 90000  # 仮想的なメール受信数

# MSCの有無でSPAM比率を比較
msp_enabled = True  # MSCが有効かどうか
account_rank_system_enabled = True  # アカウントランクシステムが有効かどうか

# シミュレーション1: 理想状態
msc_purchase_ideal = calculate_msc_purchase(email_sent, xn_values, msp_enabled=False, account_rank_system_enabled=False)

# シミュレーション2: 現実的なシミュレーション1
msc_purchase_real1 = calculate_msc_purchase(email_sent, xn_values, msp_enabled=True, account_rank_system_enabled=True)

# シミュレーション3: 現実的なシミュレーション3
msc_purchase_real3 = calculate_msc_purchase(email_sent, xn_values, msp_enabled=msp_enabled, account_rank_system_enabled=account_rank_system_enabled)

# 3Dグラフ化
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 各シミュレーションのMSC購入数をプロット
ax.bar("理想状態", 0, msc_purchase_ideal , color='b', alpha=0.5)
ax.bar("現実的なシミュレーション1", 1, msc_purchase_real1 , color='g', alpha=0.5)
ax.bar("現実的なシミュレーション3", 2, msc_purchase_real3 , color='r', alpha=0.5)

ax.set_xlabel('シミュレーション')
ax.set_ylabel('返金率・アカウントランク')
ax.set_zlabel('MSC購入数')

plt.savefig('simulation.png')

plt.show()
