# 包含了环境（《贪吃蛇》游戏）的源代码
# 步骤一 构建环境

# 导库
import numpy as np
import pygame as pg # 构建游戏，绘制蛇和苹果，并且刷新每一帧画面

# 环境类
class Environment():

    # 初始化方法 
    def __init__(self, waitTime):
        
        # Defining the parameters
        self.width = 880            # width of the game window
        self.height = 880           # height of the game window
        self.nRows = 10             # number of rows in our board
        self.nColumns = 10          # number of columns in our board
        self.initSnakeLen = 2       # initial length of the snake
        self.defReward = -0.03      # reward for taking an action - The Living Penalty
        self.negReward = -1.        # reward for dying
        self.posReward = 2.         # reward for collecting an apple
        self.waitTime = waitTime    # slowdown after taking an action
        
        if self.initSnakeLen > self.nRows / 2:
            self.initSnakeLen = int(self.nRows / 2)
        
        self.screen = pg.display.set_mode((self.width, self.height))
        
        self.snakePos = list()
        
        # Creating the array that contains mathematical representation of the game's board
        self.screenMap = np.zeros((self.nRows, self.nColumns))
        
        for i in range(self.initSnakeLen):
            self.snakePos.append((int(self.nRows / 2) + i, int(self.nColumns / 2)))
            self.screenMap[int(self.nRows / 2) + i][int(self.nColumns / 2)] = 0.5
            
        self.applePos = self.placeApple()
        
        self.drawScreen()
        
        self.collected = False
        self.lastMove = 0

    # 放置苹果的方法
    def placeApple(self):
        posx = np.random.randint(0, self.nColumns)
        posy = np.random.randint(0, self.nRows)
        while self.screenMap[posy][posx] == 0.5:
            posx = np.random.randint(0, self.nColumns)
            posy = np.random.randint(0, self.nRows)
        
        self.screenMap[posy][posx] = 1
        
        return (posy, posx)

    # 绘制画面
    def drawScreen(self):
        
        self.screen.fill((0, 0, 0))
        
        cellWidth = self.width / self.nColumns
        cellHeight = self.height / self.nRows
        
        for i in range(self.nRows):
            for j in range(self.nColumns):
                if self.screenMap[i][j] == 0.5:
                    pg.draw.rect(self.screen, (255, 255, 255), (j*cellWidth + 1, i*cellHeight + 1, cellWidth - 2, cellHeight - 2))
                elif self.screenMap[i][j] == 1:
                    pg.draw.rect(self.screen, (255, 0, 0), (j*cellWidth + 1, i*cellHeight + 1, cellWidth - 2, cellHeight - 2))
                    
        pg.display.flip()

    # 更新蛇位置的方法
    def moveSnake(self, nextPos, col):
        
        self.snakePos.insert(0, nextPos)
        
        if not col:
            self.snakePos.pop(len(self.snakePos) - 1)
        
        self.screenMap = np.zeros((self.nRows, self.nColumns))
        
        for i in range(len(self.snakePos)):
            self.screenMap[self.snakePos[i][0]][self.snakePos[i][1]] = 0.5
        
        if col:
            self.applePos = self.placeApple()
            self.collected = True
            
        self.screenMap[self.applePos[0]][self.applePos[1]] = 1

    # 更新环境的方法
    def step(self, action):
        # action = 0 -> up
        # action = 1 -> down
        # action = 2 -> right
        # action = 3 -> left
        
        # Resetting these parameters and setting the reward to the living penalty
        gameOver = False
        reward = self.defReward
        self.collected = False
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        
        snakeX = self.snakePos[0][1]
        snakeY = self.snakePos[0][0]
        
        # Checking if an action is playable and if not then it is changed to the playable one
        if action == 1 and self.lastMove == 0:
            action = 0
        if action == 0 and self.lastMove == 1:
            action = 1
        if action == 3 and self.lastMove == 2:
            action = 2
        if action == 2 and self.lastMove == 3:
            action = 3
        
        # Checking what happens when we take this action
        if action == 0:
            if snakeY > 0:
                if self.screenMap[snakeY - 1][snakeX] == 0.5:
                    gameOver = True
                    reward = self.negReward
                elif self.screenMap[snakeY - 1][snakeX] == 1:
                    reward = self.posReward
                    self.moveSnake((snakeY - 1, snakeX), True)
                elif self.screenMap[snakeY - 1][snakeX] == 0:
                    self.moveSnake((snakeY - 1, snakeX), False)
            else:
                gameOver = True
                reward = self.negReward
                
        elif action == 1:
            if snakeY < self.nRows - 1:
                if self.screenMap[snakeY + 1][snakeX] == 0.5:
                    gameOver = True
                    reward = self.negReward
                elif self.screenMap[snakeY + 1][snakeX] == 1:
                    reward = self.posReward
                    self.moveSnake((snakeY + 1, snakeX), True)
                elif self.screenMap[snakeY + 1][snakeX] == 0:
                    self.moveSnake((snakeY + 1, snakeX), False)
            else:
                gameOver = True
                reward = self.negReward
                
        elif action == 2:
            if snakeX < self.nColumns - 1:
                if self.screenMap[snakeY][snakeX + 1] == 0.5:
                    gameOver = True
                    reward = self.negReward
                elif self.screenMap[snakeY][snakeX + 1] == 1:
                    reward = self.posReward
                    self.moveSnake((snakeY, snakeX + 1), True)
                elif self.screenMap[snakeY][snakeX + 1] == 0:
                    self.moveSnake((snakeY, snakeX + 1), False)
            else:
                gameOver = True
                reward = self.negReward 
        
        elif action == 3:
            if snakeX > 0:
                if self.screenMap[snakeY][snakeX - 1] == 0.5:
                    gameOver = True
                    reward = self.negReward
                elif self.screenMap[snakeY][snakeX - 1] == 1:
                    reward = self.posReward
                    self.moveSnake((snakeY, snakeX - 1), True)
                elif self.screenMap[snakeY][snakeX - 1] == 0:
                    self.moveSnake((snakeY, snakeX - 1), False)
            else:
                gameOver = True
                reward = self.negReward
        
        # Drawing the screen, updating last move and waiting the wait time specified
        self.drawScreen()
        
        self.lastMove = action
        
        pg.time.wait(self.waitTime)
        
        # Returning the new frame of the game, the reward obtained and whether the game has ended or not
        return self.screenMap, reward, gameOver

    # 重置环境的方法
    def reset(self):
        self.screenMap  = np.zeros((self.nRows, self.nColumns))
        self.snakePos = list()
        
        for i in range(self.initSnakeLen):
            self.snakePos.append((int(self.nRows / 2) + i, int(self.nColumns / 2)))
            self.screenMap[int(self.nRows / 2) + i][int(self.nColumns / 2)] = 0.5
        
        self.screenMap[self.applePos[0]][self.applePos[1]] = 1
        
        self.lastMove = 0