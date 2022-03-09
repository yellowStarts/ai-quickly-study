# 导库
import numpy as np
import matplotlib.pyplot as plt
import random

N = 10000  # 顾客数量
d = 9  # 广告策略数量

# 环境矩阵（数据集）
conversion_rates = [0.05, 0.13, 0.09, 0.16, 0.11, 0.04, 0.20, 0.08, 0.01]
X = np.array(np.zeros([N, d]))

for i in range(N):
    for j in range(d):
        if np.random.rand() <= conversion_rates[j]:
            X[i, j] = 1

strategies_selected_rs = [] # 由随机选择算法在各回合中选择的策略所构成的列表。将其初始化为一个空的列表。
strategies_selected_ts = [] # 由汤普森采样模型在各回合中选择的策略所构成的列表。将其初始化为一个空的列表。
total_reward_rs = 0 # 通过随机选择算法在各回合中累积的总奖励。将其初始化为0。
total_reward_ts = 0 # 通过汤普森采样模型在各回合中累积的总奖励。将其初始化为0。
numbers_of_reward_1 = [0] * d # 一个具有9个元素的列表，每个元素将包含其获得为1的奖励的次数。将其初始化为由9个0组成的列表。
numbers_of_reward_0 = [0] * d # 一个具有9个元素的列表，每个元素将包含其获得为0的奖励的次数。将其初始化为由9个0组成的列表。

for n in range(0, N):
    # 随机选择算法
    strategy_rs = random.randrange(d)
    strategies_selected_rs.append(strategy_rs)
    reward_rs = X[n, strategy_rs]
    total_reward_rs += reward_rs

    # 汤普森采样模型
    strategy_ts = 0
    max_random = 0
    for i in range(0, d):
        random_beta = np.random.beta(numbers_of_reward_1[i]+1, numbers_of_reward_0[i] + 1)
        if random_beta > max_random:
            max_random = random_beta
            strategy_ts = i
    reward_ts = X[n, strategy_ts]
    if reward_ts == 1:
        numbers_of_reward_1[strategy_ts] += 1
    else:
        numbers_of_reward_0[strategy_ts] += 1

    strategies_selected_ts.append(strategy_ts)
    total_reward_ts += reward_ts

# 计算汤普森采样关于基准（即随机选择）的相对回报
relative_return = (total_reward_ts - total_reward_rs) / total_reward_rs * 100
print("相对回报: {:.0f} %".format(relative_return))

# 绘制所选策略的直方图
plt.hist(strategies_selected_ts)
plt.title("Histogram of Selections")
plt.xlabel('Strategy')
plt.ylabel('Number of times the strategy was selected')
plt.show()