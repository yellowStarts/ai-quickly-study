# 训练AI模型玩《贪吃蛇》的源代码
# 步骤四 训练AI模型

# 导库
from environment import Environment
from brain import Brain
from DQN import Dqn
import numpy as np
import matplotlib.pyplot as plt

# 定义参数
memSize = 60000 # 经验回放记忆的最大容量
batchSize = 32 # 在每个迭代从经验回放记忆中抽取记忆批量用于训练时，获得的输入批量和目标批量的尺寸
learningRate = 0.0001 # Brain类中Adam优化器的学习速率
gamma = 0.9 # 经验回放记忆的折扣因子
nLastStates = 4 # 用于记录当前游戏状态的最新画面的数量

epsilon = 1. # 最初的随机系数，即执行随机行为的概率
epsilonDecayRate = 0.0002 # 每局游戏或周期减小随机系数epsilon的幅度 
minEpsilon = 0.05 # 最小可接受的随机系数，任何调整不可低于该系数

filepathToSave = 'model2.h5' # 模型文件要保存到的路径

# 创建环境、大脑以及经验回放记忆
env = Environment(0)
brain = Brain((env.nRows, env.nColumns, nLastStates), learningRate)
model = brain.model
dqn = Dqn(memSize, gamma)

# 重置AI模型的状态
def resetStates():
    currentState = np.zeros((1, env.nRows, env.nColumns, nLastStates))
    
    for i in range(nLastStates):
        currentState[:,:,:,i] = env.screenMap
    
    return currentState, currentState

# 开始编写训练的代码
epoch = 0 # 当前的轮次
scores = list() # 储存了每100局游戏或轮次获得的平均总分
maxNCollected = 0 # 训练中得到的最高总分
nCollected = 0. # 每局或轮次得到的总分 
totNCollected = 0 # 在100局游戏或轮次中蛇吃掉的苹果总数
while True:
    # 重置环境和游戏状态
    env.reset()
    currentState, nextState = resetStates()
    epoch += 1
    gameOver = False
    
    # 开始游戏并训练ai
    while not gameOver: 
        
        # Choosing an action to play
        if np.random.rand() < epsilon:
            action = np.random.randint(0, 4)
        else:
            qvalues = model.predict(currentState)[0]
            action = np.argmax(qvalues)
        
        # 更新环境
        state, reward, gameOver = env.step(action)
        
        # 需要将一帧新画面添加到nextState中，并且移除最旧的一帧画面
        state = np.reshape(state, (1, env.nRows, env.nColumns, 1))
        nextState = np.append(nextState, state, axis = 3)
        nextState = np.delete(nextState, 0, axis = 3)
        
        # 通过remember方法将过渡信息加入记忆，然后从记忆抽取一个随机的批量来训练模型
        dqn.remember([currentState, action, reward, nextState], gameOver)
        inputs, targets = dqn.get_batch(model, batchSize)
        model.train_on_batch(inputs, targets)
        
        # 一个输出批量，然后基于它们进行训练。
        if env.collected:
            nCollected += 1
        
        currentState = nextState
    
    # 检验当前的轮次是否打破了一轮次吃苹果数的历史纪录（该纪录必须大于2）
    # 如果确实如此，则更新最佳纪录并且将当前的模型保存到先前设定的文件路径。此处还增加了totNCollected并为下一轮次将nCollected重置为0
    if nCollected > maxNCollected and nCollected > 2:
        maxNCollected = nCollected
        model.save(filepathToSave)
    
    totNCollected += nCollected
    nCollected = 0
    
    # 进行完100轮次游戏后，显示平均总分
    if epoch % 100 == 0 and epoch != 0:
        scores.append(totNCollected / 100)
        totNCollected = 0
        plt.plot(scores)
        plt.xlabel('Epoch / 100')
        plt.ylabel('Average Score')
        plt.savefig('stats.png')
        plt.close()
    
    # 降低随机系数
    if epsilon > minEpsilon:
        epsilon -= epsilonDecayRate
    
    # 展示了每局游戏的一些额外信息
    print('Epoch: ' + str(epoch) + ' Current Best: ' + str(maxNCollected) + ' Epsilon: {:.5f}'.format(epsilon))