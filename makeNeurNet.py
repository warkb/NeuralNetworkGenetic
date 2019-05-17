from classes import WIDTH, HEIGHT
from copy import copy
"""
Тут мы будем делать нейронные сети
Конечная цель - засерелиазовать сеть, которая будет верно реагировать
на еду и опасность перед глазами, в файл

На что будет реагировать:
 * Еда перед собой - съесть
 * Еда на клетку вперед - пойти вперед
 * Еда на клетку назад - пойти назад
 * Еда на клетку влево - пойти влево
 * Еда на клетку вправо - пойти вправо
    [0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
"""
import numpy as np

def setPointToArr(dx, dy, type):
    """
    Возвращает индекс
    чтобы не выщитывать какая ячейка массива какой точке на поле
    и типу объекта соответствует
    0 - трава
    1 - свинья
    2 - хищник
    :param dx:
    :param dy:
    :param type:
    :return:
    """
    ind = 3 + 3 * ((dy + 2) * 5 + (dx + 2)) + type
    return ind

def makeLearnSetForPig():
    learnSet = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            for energy in 100:
                arr = [x, y, energy] + [] * 75
                # если травка рядом - съесть
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        copyArr = copy(arr)
                        copyArr[setPointToArr(i, j, 0)] = 1
                        learnSet.append(copyArr)
                # если травка справа - шагнуть направо
                for j in range(-1, 2):
                    copyArr = copy(arr)
                    copyArr[setPointToArr(1, j, 0)] = 1
                    learnSet.append(copyArr)
                # если травка слева - шагнуть налево
                for j in range(-1, 2):
                    copyArr = copy(arr)
                    copyArr[setPointToArr(-1, j, 0)] = 1
                    learnSet.append(copyArr)
                # если травка наверху - шагнуть наверху
                for j in range(-1, 2):
                    copyArr = copy(arr)
                    copyArr[setPointToArr(j, -1, 0)] = 1
                    learnSet.append(copyArr)
                # если травка внизу - шагнуть вниз
                for j in range(-1, 2):
                    copyArr = copy(arr)
                    copyArr[setPointToArr(j, 1, 0)] = 1
                    learnSet.append(copyArr)
    return learnSet

def makeLearnSetForWolf():
    learnSet = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            for energy in 100:
                arr = [x, y, energy] + [] * 75
                # если травка рядом - съесть
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        copyArr = copy(arr)
                        copyArr[setPointToArr(i, j, 1)] = 1
                        learnSet.append(copyArr)
                # если травка справа - шагнуть направо
                for j in range(-1, 2):
                    copyArr = copy(arr)
                    copyArr[setPointToArr(1, j, 1)] = 1
                    learnSet.append(copyArr)
                # если травка слева - шагнуть налево
                for j in range(-1, 2):
                    copyArr = copy(arr)
                    copyArr[setPointToArr(-1, j, 1)] = 1
                    learnSet.append(copyArr)
                # если травка наверху - шагнуть наверху
                for j in range(-1, 2):
                    copyArr = copy(arr)
                    copyArr[setPointToArr(j, -1, 1)] = 1
                    learnSet.append(copyArr)
                # если травка внизу - шагнуть вниз
                for j in range(-1, 2):
                    copyArr = copy(arr)
                    copyArr[setPointToArr(j, 1, 1)] = 1
                    learnSet.append(copyArr)
    return learnSet

def nonlin(x,deriv=False):
    if(deriv==True):
        return x * (1 - x)
    return 1/(1+np.exp(-x))

X = np.array([[0, 0],
              [0, 1],
              [1, 0],
              [1, 1]])

Y = np.array([[0],
              [1],
              [1],
              [0]])
D1 = 2
D2 = 1
D3 = 5

syn0 = syn0 = 2*np.random.random((D1, D3)) - 1
syn1 = 2*np.random.random((D3,D2)) - 1

def getResult(syn0, syn1, X):
    l0 = X
    l1 = nonlin(np.dot(l0, syn0))
    l2 = nonlin(np.dot(l1, syn1))
    return l2

def toLearnNeurNetwork(syn0, syn1, X, Y):
    """
    Обучает нейронную сеть
    :param syn0:
    :param syn1:
    :param X:
    :param Y:
    :return:
    """
    printStep = 600
    for j in range(60000):
        # проходим вперёд по слоям 0, 1 и 2
        l0 = X
        l1 = nonlin(np.dot(l0, syn0))
        l2 = nonlin(np.dot(l1, syn1))

        # как сильно мы ошиблись относительно нужной величины?
        l2_error = Y - l2

        if (j % printStep) == 0:
            print("Error: " + str(np.mean(np.abs(l2_error))))

        # в какую сторону нужно двигаться?
        # если мы были уверены в предсказании, то сильно менять его не надо
        l2_delta = l2_error * nonlin(l2, deriv=True)

        # как сильно значения l1 влияют на ошибки в l2?
        l1_error = l2_delta.dot(syn1.T)

        # в каком направлении нужно двигаться, чтобы прийти к l1?
        # если мы были уверены в предсказании, то сильно менять его не надо
        l1_delta = l1_error * nonlin(l1, deriv=True)

        syn1 += l1.T.dot(l2_delta)
        syn0 += l0.T.dot(l1_delta)

toLearnNeurNetwork(syn0, syn1, X, Y)
for el in X:
    print(getResult(syn0, syn1, el))