from collections import namedtuple
from typing import List, Any, Union

import pygame
from enum import Enum
from game_clases.Enums import Directions
from game_clases.rendered_object import RenderedObject
from game_params import *
from commonNeuralNetwork.commonNN import CommonNeuralNetwork
from copy import deepcopy


class Critter(RenderedObject):
    best_lifetime = 0 # самый долгий срок жизни
    def __init__(self, x, y, image_link, game, direction=Directions.up):
        RenderedObject.__init__(self, x, y, image_link)
        self.game = game
        self.direction = direction
        self.initNN()
        self.life_time = 0  # сколько ходов прожило создание
        self.has_child = False # может ли создание сейчас родить ребенка
        self.actions_array = [
            self.set_direction_up,
            self.set_direction_down,
            self.set_direction_left,
            self.set_direction_right,
            self.walk,
            self.eat,
            lambda: None
        ]
        self.controller = self.neural_network_controller

    def __del__(self):
        pass

    def die(self):
        print('Ohh no...')
        if self.life_time > __class__.best_lifetime:
            __class__.best_lifetime = self.life_time

    def neural_network_controller(self):
        """
        Управляет созданием с помощью нейронной сети
        :return: индекс действия массива actions_array
        """
        perception = self.makePerception()
        network_result = self.neural_network.get_result([perception])[0]
        return list(network_result).index(max(network_result))

    def keyboard_controller(self):
        """
        Управляет существом с помомщью клавиатуры
        :return: индекс действия массива actions_array
        """
        inputs = self.game.press_keys
        if inputs.up:
            self.direction = Directions.up
            return 4
        if inputs.down:
            self.direction = Directions.down
            return 4
        if inputs.left:
            self.direction = Directions.left
            return 4
        if inputs.right:
            self.direction = Directions.right
            return 4
        if inputs.walk:
            return 4
        if inputs.eat:
            return 5
        return 6

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
        self.energy -= self.priceEnergy
        if self.energy < 0:
            self.game.remove_critter(self)
        win_index = self.controller()
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
        TODO: ОПТИМИЗИРОВАТЬ
        :param objects:
        :param x:
        :param y:
        :return:
        """
        for obj in objects:
            if obj.x == x and obj.y == y:
                return 1
        return 0

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
        NewPos = type('NewPos', (), {})
        new_pos = NewPos()
        new_pos.x = self.x
        new_pos.y = self.y
        if self.direction == Directions.up:
            if self.y > 0:
                new_pos.y -= 1
        if self.direction == Directions.down:
            if self.y < HEIGHT - 1:
                new_pos.y += 1
        if self.direction == Directions.left:
            if self.x > 0:
                new_pos.x -= 1
        if self.direction == Directions.right:
            if self.x < WIDTH - 1:
                new_pos.x += 1
        if self.game.is_free_cell(new_pos.x, new_pos.y):
            self.x = new_pos.x
            self.y = new_pos.y
        self.energy -= self.priceEnergy

    def eat(self):
        '''
        Добавляет энергии к текущем счетчику энергии
        Если энергия выше максимума - уполовинивает её и возвращает True
        Иначе False
        :return:
        '''
        pass

    def make_child(self):
        """
        Рождает нового ребенка
        :return: Critter
        """
        new_child = self.__class__(self.x, self.y, self.game)
        new_child.neural_network = deepcopy(self.neural_network)
        new_child.neural_network.mutate(5, 25)
        return new_child

    def update_energy(self):
        """Обновляет показатель энергии, если попытка съесть оказалась удачной"""
        # if self.controller == self.keyboard_controller:
        #     print(self.game.get_objects_near(self.x, self.y).grasses)
        self.energy += self.dEnergy
        if self.energy > self.maxEnergy:
            self.has_child = True
            self.energy = self.maxEnergy / 2
            return True
        return False

