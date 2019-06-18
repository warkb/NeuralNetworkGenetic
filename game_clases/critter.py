from typing import List, Any, Union

import pygame
from enum import Enum
from game_clases.Enums import Directions
from game_params import *
from commonNeuralNetwork.commonNN import CommonNeuralNetwork

class Critter:
    def __init__(self, x, y, game, direction=Directions.up):
        self.x = x
        self.y = y
        self.game = game
        self.direction = direction
        self.initNN()
        self.life_time = 0  # сколько ходов прожило создание
        self.actions_array = [
            self.set_direction_up,
            self.set_direction_down,
            self.set_direction_left,
            self.set_direction_right,
            self.walk,
            self.eat,
            lambda: None
        ]


    def set_direction_up(self):
        self.direction = Directions.up

    def set_direction_down(self):
        self.direction = Directions.down

    def set_direction_left(self):
        self.direction = Directions.left

    def set_direction_right(self):
        self.direction = Directions.right

    def make_move(self):
        """
        Что - то делает
        :return:
        """
        self.life_time += 1
        perception = self.makePerception()
        network_result = self.neural_network.get_result([perception])[0]
        # print(network_result)
        win_index = list(network_result).index(max(network_result))
        self.actions_array[win_index]()

    def makePerception(self):
        """
        По своим параметрам, а также по массивам с объектами
        создает массив восприятия для нейронной сети
        :param grasses:
        :param pigs:
        :param wolfs:
        :return:
        """
        perception = []
        perception.append(self.x)
        perception.append(self.y)
        perception.append(self.energy)
        # 0 - нет в клетке, 1 - есть
        for j in range(-2, 3):
            for i in range(-2, 3):
                perception.append(
                    self.hasObjectInPoint(self.game.grasses, self.x + i, self.y + j)
                )
                perception.append(
                    self.hasObjectInPoint(self.game.pigs, self.x + i, self.y + j)
                )
                perception.append(
                    self.hasObjectInPoint(self.game.wolfs, self.x + i, self.y + j)
                )
        return perception

    def hasObjectInPoint(self, objects, x, y):
        """
        Проверяет, есть ли среди объектов объект,
        который занимает заданную точку
        МОЖНО ОПТИМИЗИРОВАТЬ
        :param objects:
        :param x:
        :param y:
        :return:
        """
        for obj in objects:
            if obj.x == x and obj.y == y:
                return 1
        return 0

    def updateRect(self, topPadding=0, leftPadding=0):
        """
        обновляет прямоугольник
        по координатам в матрице и зазорам по бокам выдает координаты на экране
        :param topPadding:
        :param leftPadding:
        :return:
        """
        self.rect.top = topPadding + self.y * SPRITE_SIZE
        self.rect.left = leftPadding + self.x * SPRITE_SIZE

    def initEnergy(self, maxEnergy, dEnergy):
        """
        Инициализирует значения связанные с энергией
        :param maxEnergy:
        :param dEnergy:
        :return:
        """
        self.maxEnergy = maxEnergy
        self.dEnergy = dEnergy  # энергия, которую получает существо кого-то съедая
        self.priceEnergy = 1  # энергия, которая забирается за один ход
        self.energy = self.maxEnergy / 2

    def initImage(self, link):
        """
        делает для класса изображение и прямоугольник с координатами
        :param link:
        :return:
        """
        self.image = pygame.image.load(link)
        self.image = pygame.transform.scale(self.image, (SPRITE_SIZE, SPRITE_SIZE))
        self.rect = self.image.get_rect()

    def initNN(self):
        """Инициализирует нейронную сеть"""
        """
        действия:
        пойти
        повернуть 
            вверх
            вниз
            направо
            налево
        съесть
        ничего не делать
        7
        """
        self.neural_network = CommonNeuralNetwork((78, 78, 7))

    def walk(self):
        if self.direction == Directions.up:
            if self.y > 0:
                self.y -= 1
        if self.direction == Directions.down:
            if self.y < HEIGHT - 1:
                self.y += 1
        if self.direction == Directions.left:
            if self.x > 0:
                self.x -= 1
        if self.direction == Directions.right:
            if self.x < WIDTH - 1:
                self.x += 1

        self.energy -= self.priceEnergy

    def eat(self):
        '''
        Добавляет энергии к текущем счетчику энергии
        Если энергия выше максимума - уполовинивает её и возвращает True
        Иначе False
        :return:
        '''
        self.energy += self.dEnergy
        if self.energy > self.maxEnergy:
            self.energy = self.maxEnergy / 2
            return True
        return False

