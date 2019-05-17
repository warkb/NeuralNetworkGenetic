import numpy as np
import pygame
from enum import Enum
from pygame.sprite import Sprite

WIDTH = 12
HEIGHT = 10

SPRITE_SIZE = 75 # размер спрайта в пикселях
"""
действия:
пойти вверх
вниз
направо
налево
сделать шаг
съесть
ничего не делать
6
"""
class Directions(Enum):
    up = 1
    down = 2
    left = 3
    right = 4

class Grass(Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('img/grass.png')
        self.image = pygame.transform.scale(self.image, (SPRITE_SIZE, SPRITE_SIZE))
        self.rect = self.image.get_rect()

    def __str__(self):
        return 'Это Трава с координатами (%s, %s)' % (self.x, self.y)

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

percept = {
    "energy": 10,
    "x": 10,
    "y": 10,

}

class Critter:
    def __init__(self, x, y, direction=Directions.up):
        self.x = x
        self.y = y
        self.direction = direction

    def action(self, percept):
        """
        Что - то делает по словарю восприятия percept
        :return:
        """
        pass

    def makePerception(self, grasses, pigs, wolfs):
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
        # добавляем информацию по траве
        # 0 - нет в клетке, 1 - есть
        for j in range(-2, 3):
            for i in range(-2, 3):
                perception.append(
                    self.hasObjectInPoint(grasses, self.x + i, self.y + j)
                )
                perception.append(
                    self.hasObjectInPoint(pigs, self.x + i, self.y + j)
                )
                perception.append(
                    self.hasObjectInPoint(wolfs, self.x + i, self.y + j)
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
        0

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

class Pig(Critter):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.initEnergy(100, 10)
        self.initImage('img/pig.png')

    def __str__(self):
        return 'Это Свинья с координатами (%s, %s)' % (self.x, self.y)


class Wolf(Critter):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.initEnergy(100, 25)
        self.initImage('img/wolf.png')

    def __str__(self):
        return 'Это Волк с координатами (%s, %s)' % (self.x, self.y)


class Entities(Enum):
    grass = Grass
    pig = Pig
    wolf = Wolf

