# 测试AI模型的性能的源代码

# 导库
from environment import Environment
from brain import Brain
import numpy as np

# 定义参数
nLastStates = 4
filepathToOpen = 'model.h5' # 测试的模型的文件路径
slowdown = 75 # 代表每次执行行为之间停顿时间的变量，这样就能清楚地看到AI模型如何执行行为。

# 创建Environment和Brain类的对象
env = Environment(slowdown)
brain = Brain((env.nRows, env.nColumns, nLastStates))
model = brain.loadModel(filepathToOpen)

# 重置状态的方法
def resetStates():
    currentState = np.zeros((1, env.nRows, env.nColumns, nLastStates))
    
    for i in range(nLastStates):
        currentState[:,:,:,i] = env.screenMap
   
    return currentState, currentState

# Starting the main loop
while True:
    # Resetting the game and the game states
    env.reset()
    currentState, nextState = resetStates()
    gameOver = False
    
    # Playing the game
    while not gameOver: 
        
        # Choosing an action to play
        qvalues = model.predict(currentState)[0]
        action = np.argmax(qvalues)
        
        # 更新环境
        state, _, gameOver = env.step(action)
        
        # Adding new game frame to next state and deleting the oldest one from next state
        state = np.reshape(state, (1, env.nRows, env.nColumns, 1))
        nextState = np.append(nextState, state, axis = 3)
        nextState = np.delete(nextState, 0, axis = 3)
        
        # Updating current state
        currentState = nextState