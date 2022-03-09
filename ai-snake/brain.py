# 构建卷积神经网络(CNN)的源代码。
# 步骤二 构建大脑

# 导库
import keras
# Sequential 用于初始化神经网络和定义网络大致架构的类
# load_model 用于从文件导入模型的函数
from keras.models import Sequential, load_model
# Dense 用于在人工神经网络（ANN）中创建全连接层的方法
# Dropout 用于向网络增加丢弃法的类
# Conv2D 用于构建卷积层的类
# MaxPooling2D 用于构建最大池化层的类
# Flatten 用于扁平化输入的类，这样就可以获得经典ANN所需的输入形式 
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
# adam_v2 用于优化神经网络的优化器，它在训练CNN时会派上用场
from keras.optimizers import adam_v2

# 大脑类
class Brain():

    # 初始化方法
    # iS 输入形状
    # lr 学习速率 
    def __init__(self, iS = (100,100,3), lr = 0.0005):
        
        self.learningRate = lr
        self.inputShape = iS
        self.numOutputs = 4
        self.model = Sequential() 
        
        # 为模型添加一个新的卷积层
        # 它有32个3×3的滤波器，并使用ReLU作为激活函数
        self.model.add(Conv2D(32, (3,3), activation = 'relu', input_shape = self.inputShape))
        
        # 添加池化层 窗口大小为2×2
        self.model.add(MaxPooling2D((2,2)))
        
        # 添加第二个卷积层
        self.model.add(Conv2D(64, (2,2), activation = 'relu'))
        
        # 扁平化为一个1D向量
        self.model.add(Flatten())
        
        # 为模型新添加了一个拥有256个神经元的隐藏层，并使用ReLU作为激活函数
        self.model.add(Dense(units = 256, activation = 'relu'))
        
        # 创建神经网络的最后一层——输出层
        self.model.add(Dense(units = self.numOutputs))
        
        # 整合整个模型。它将通过配置损失函数和优化器来告诉模型在训练过程中该如何计算误差、如何优化权重
        self.model.compile(loss = 'mean_squared_error', optimizer = adam_v2.Adam(lr = self.learningRate))

    # 从文件导入模型的方法
    def loadModel(self, filepath):
        self.model = load_model(filepath)
        return self.model