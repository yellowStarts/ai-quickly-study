from cmath import sqrt


def division(a, b):
    resulte = a / b
    return resulte

d = division(3, 5)
print(d)

# Homework 计算两点距离
def getDistance(x1, y1, x2, y2):
    return pow(pow(x1-x2, 2) + pow(y1-y2, 2), 0.5)

distance = getDistance(0, 0, 1, 1)
print(distance)