# for 循环
from tracemalloc import stop


for i in range(1, 20):
    print(i)

# 遍历数组
L1 = [3, 4, 1, 6, 7, 5]
for i in L1:
    print(i)


# while 循环
stop = False
i = 0
while stop == False:
    i += 1
    print(i)
    if i >= 19:
        stop = True

# 嵌套循环
L4 = [[2, 9, -5], [-1, 0, 4], [3, 1, 2]]
for row in L4:
    for element in row:
        print(element)

# Homwwork 阶乘--for循环实现
n=5
sum = 1
for i in range(1, n+1):
    sum *= i
print(sum)

# Homwwork 阶乘--while循环实现
sum = 1              
i = 1                     
while i <= n:               
    sum *= i          
    i += 1                 
print(sum)          