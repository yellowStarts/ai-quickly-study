# 预测房价
# 导库
import pandas as pd
import numpy as np
import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.optimizers import adam_v2
Adam = adam_v2.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08)

# 导入数据集
dataset = pd.read_csv('kc_house_data.csv')

# 特征数据
# 将自第4列开始的所有数据从原始数据中提取了出来
# （也就是剔除了ID、房屋出售日期和价格这3列）
# 使用.iloc来切分数据集，使用.values将分离出来的数据集转换成NumPy对象
X = dataset.iloc[:, 3:].values
# 将邮政编码从数据中排除，不幸的是，这一列在特征数据的中间
# 使用了NumPy的np.r_函数将X分成分了不包含邮政编码列的两部分，
# 然后再重新组合成新的数据
X = X[:, np.r_[0:13, 14:18]]
# 提取价格数据
y = dataset.iloc[:, 2].values

# 准备训练集和测试集数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# 数据缩放
xscaler = MinMaxScaler(feature_range = (0, 1))
X_train = xscaler.fit_transform(X_train)
X_test = xscaler.transform(X_test)

yscaler = MinMaxScaler(feature_range = (0, 1))
y_train = yscaler.fit_transform(y_train.reshape(-1, 1))
y_test = yscaler.transform(y_test.reshape(-1, 1))

# 构建神经网络
model = Sequential()
model.add(Dense(units = 64, kernel_initializer = 'uniform',
activation = 'relu', input_dim = 17))
model.add(Dense(units = 16, kernel_initializer = 'uniform',
activation = 'relu'))
model.add(Dense(units = 1, kernel_initializer = 'uniform',
activation = 'relu'))
model.compile(optimizer = adam_v2.Adam(lr = 0.001), loss = 'mse',
metrics = ['mean_absolute_error'])

# 训练神经网络
model.fit(X_train, y_train, batch_size = 32, epochs = 100,
validation_data = (X_test, y_test))

# 展示结果
# 预测
y_test= yscaler.inverse_transform(y_test)
prediction = yscaler.inverse_transform(model.predict(X_test))
# 计算误差
error = abs(prediction - y_test) / y_test
print(np.mean(error))

