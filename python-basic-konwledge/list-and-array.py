# 一维列表的创建
import numpy as np
L1 = list()
L2 = []

L3 = [3, 4, 1, 6, 7, 5]
# 二维列表
L4 = [[2, 9, -5], [-1, 0, 4], [3, 1, 2]]

# 创建 NumPy数组
nparray = np.zeros((5, 5))

print(L3[0])
print(L4[1])
print(L4[1][1])

# Homework 求 L4 平均值
avg = np.average(L4)
print(avg) # 等价于 print(15/9)
