import numpy as np
import matplotlib.pyplot as plt

#シミュレーションの回数,確率,スパマーの割合
#アカウントランクの適応
class Simulation:
    def __init__(self, accounts=1000, email_sent=10000, email_received=9000, msp_enabled=True, account_rank_system_enabled=True, simulation_times=1000):
        self.accounts = accounts
        self.xn_values = np.random.uniform(0, 100, accounts)  # SPAMERとML送信者のMSC返金率をランダム生成
        self.email_sent = email_sent
        self.email_received = email_received
        self.msp_enabled = msp_enabled
        self.account_rank_system_enabled = account_rank_system_enabled
    
    def calculate_msc_purchase(self):
        if self.msp_enabled:
            spam_ratio = np.mean(self.xn_values) / 100  # 平均のMSC返金率をSPAM比率とする
        else:
            spam_ratio = 0  # MSCが無効な場合、SPAM比率は0

        if self.account_rank_system_enabled:
            account_rank = np.mean(self.xn_values)  # アカウントランクは平均のMSC返金率とする
        else:
            account_rank = 0  # アカウントランクシステムが無効な場合、アカウントランクは0

        msc_purchase = self.email_sent * (1 - spam_ratio) - self.email_received * (account_rank / 100)
        return msc_purchase

    def create3dGrapf(self,msc_purchase,state,color,graph_name):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.bar(state, 0, msc_purchase , color=color, alpha=0.5)
        ax.set_xlabel('シミュレーション')
        ax.set_ylabel('返金率・アカウントランク')
        ax.set_zlabel('MSC購入数')
        plt.savefig(graph_name)
        
