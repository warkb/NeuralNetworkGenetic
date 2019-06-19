# https://habr.com/ru/post/271563/
import pickle
import numpy as np
import random as rd

class NotEqualArgumentsInputsException(Exception):
    def __init__(self, text='Не совподает количество входных ячеек и аргументов'):
        self.txt = text


class CommonNeuralNetwork():
    """Класс с нейронной сетью"""
    def __init__(self, counts):
        """
        :parm counts: (int) - кортеж с цифрами - количество нейронов в каждом слое
        TODO: 3-слойная нейронная сеть, выученная делать xor
        """
        self.counts = tuple(x for x in counts)
        self.layers = []
        for i in range(len(counts)):
            if i == len(counts) - 1:
                break
            self.layers.append(2 * np.random.random((counts[i], counts[i + 1])) - 1)
        self.layers = tuple(self.layers)

    @staticmethod
    def sigmoid(x):
        """Функция активации для нейронной сети"""
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def deriv_sigmoid(x):
        """Производная от сигмоиды"""
        return x * (1 - x)

    def get_result(self, x):
        """
        Возвращает результат прямого распространения
        """
        x = np.array(x)
        if len(x[0]) != len(self.layers[0]):
            print(f'{len(x[0])} != {len(self.layers[0])}')
            raise NotEqualArgumentsInputsException()
        result = x
        for i, layer in enumerate(self.layers):
            # print(f'x.shape=({result.shape})')
            # print(f'layer.shape={layer.shape}')
            # print('===============================')
            # print(result)
            # print(layer)
            result = self.sigmoid(np.matmul(result, layer))

        return result

    def learn_network(self, input_array, output_array, iterations_count=1000, epsilon=0):
        """Обучает нейронную сеть на примерах
        :param input_array: массив примеров входных значений
        :param output_array: массив примеро выходных значений
        :param iterations_count: количество итераций обучения
        :param epsilon: максимальная ошибка
        """
        # if len(input_array[0]) != len(self.layers[0]):
        #     raise NotEqualArgumentsInputsException('Не совпадает количество входных ячеек и аргументов')
        # if len(output_array[0]) != len(self.layers[-1]):
        #     raise NotEqualArgumentsInputsException('Не совпадает количество выходныз ячеек и аргументов')
        for iter_num in range(iterations_count):
            results = [input_array]
            # получаем выходные сигналы для каждого слоя
            for i, layer in enumerate(self.layers):
                results.append(self.sigmoid(np.matmul(results[-1], layer)))
            # выполняем обратное распространение
            errors = [output_array - results[-1]]
            if (iter_num % (iterations_count / 10)) == 0:
                print("Error:" + str(np.mean(np.abs(errors[0]))))
            deltas = []
            for i in range(len(results) - 1, 0, -1):
                # print(i)
                delta = errors[0] * CommonNeuralNetwork.deriv_sigmoid(results[i])
                deltas.insert(0, delta)
                error = deltas[0].dot(self.layers[i - 1].T)
                errors.insert(0, error)

            # меняем веса
            for i, layer in enumerate(self.layers):
                layer += results[i].T.dot(deltas[i])

    def save_network(self, filename):
        """
        Сохраняем сеть в файл
        :param filename: путь к файлу
        """
        with open(filename, 'wb') as f:
            pickle.dump(self.layers, f)

    def load_network(self, filename):
        """
        Загружает сеть из файла
        :param filename: путь к файлу
        """
        with open(filename, 'rb') as f:
            self.layers = pickle.load(f)

    def mutate(self, count=1, percent=10):
        """
        Меняет count весов на percent процентов
        :param count:
        :param percent:
        :return: None
        """
        for _ in range(count):
            lay = rd.choice(self.layers)
            ind = rd.randrange(0, len(lay) - 1)
            lay[ind] += rd.choice((-1,1)) * lay[ind] * percent / 100
