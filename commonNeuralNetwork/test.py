import numpy as np
from commonNN import CommonNeuralNetwork

def testNN():
    nn = CommonNeuralNetwork((3, 4, 1))
    print(nn.get_result(np.array([[1, 1, 1]])))
    X = np.array([[0, 0, 1],
                  [0, 1, 1],
                  [1, 0, 1],
                  [1, 1, 1]])

    y = np.array([[0],
                  [1],
                  [1],
                  [0]])
    print('Проверяем, что сеть учится')
    print(nn.get_result(X))
    nn.learn_network(X, y, 10000)
    print(nn.get_result(X))
    print('Проверяем мутацию')
    nn.mutate(5, 25)
    print(nn.get_result(X))
    # print('Проверяем сохранение и загрузку сети из файла')
    # filename = 'saveme'
    # nn.save_network(filename)
    # newnn = CommonNeuralNetwork((3, 4, 1))
    # print(newnn.get_result(X))
    # newnn.load_network(filename)
    # print(newnn.get_result(X))


def fuzzy_logic_test():
    fuzzyAnd = lambda a, b: max(a, b)
    fuzzyOr = lambda a, b: min(a, b)
    fuzzyNot = lambda a: 1 - a


    def spikeProfile(value, low, hight):
        if low < 0 and hight < 0:
            hight = -(hight - low)
        elif low < 0 and hight > 0:
            hight += -low
        elif low > 0 and hight > 0:
            hight -= low

        peak = (hight / 2)
        low = 0
        if value < peak:
            return value / peak
        if value > peak:
            return (hight - value) / peak
        return 1

    def plateauProfile(value, low, lo_plat, hi_plat, hi):
        value += -low;
        if low < 0:
            lo_plat += -low
            hi_plat += -low
            hi += -low
            low = 0
        else:
            lo_plat -= low
            hi_plat -= low
            hi -= low
            low = 0

        upslope = (1 / (lo_plat - low))
        downslope = (1 / hi - hi_plat)

        if value < low:
            return 0
        if value > hi:
            return 0
        if value >= lo_plat and value <= hi_plat:
            return 1
        if value < lo_plat:
            return (value - low) * upslope
        if value > hi_plat:
            return (hi-value) * downslope
        return 0

if __name__ == '__main__':
    testNN()