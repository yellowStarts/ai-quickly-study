# 导库
import numpy as np

# 设置老虎机的胜率的转化率(conversionRates)列表
conversionRates = [0.15, 0.04, 0.13, 0.11, 0.05]
N = 10000 # 样本数
d = len(conversionRates) # 转换率列表长度

# 定义每台老虎机样本（即每局下注）输赢的数据集
X = np.zeros((N, d))
for i in range(N):
    for j in range(d):
        if np.random.rand() < conversionRates[j]:
            X[i][j] = 1

# 创建两个数组记录下注每台老虎机的输赢状况
nPosReward = np.zeros(d) # 赢钱次数
nNegReward = np.zeros(d) # 输钱次数

# 遍历数据集中的每个样本选择胜率最高的机器
for i in range(N):
    selected = 0 # 被选中的机器
    maxRandom = 0 # 记录所有机器中获取的最高贝塔分布猜想
    for j in range(d):
        randomBeta = np.random.beta(nPosReward[j] + 1, nNegReward[j] + 1)
        if randomBeta > maxRandom:
            maxRandom = randomBeta
            selected = j
    if X[i][selected] == 1:
        nPosReward[selected] += 1
    else:
        nNegReward[selected] += 1

# 显示代码分析出的最佳机器
nSelectd = nPosReward + nNegReward
for i in range(d):
    print('机器 ' + str(i+1) + ' 号被选择 ' + str(nSelectd[i]) + ' 次')

print('结果：最好的机器是 ' + str(np.argmax(nSelectd) + 1) + '号')