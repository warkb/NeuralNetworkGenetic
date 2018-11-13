import pygame
from enum import Enum
from pygame.sprite import Sprite

WIDTH = 12
HEIGHT = 10

SPRITE_SIZE = 75 # размер спрайта в пикселях

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

class Critter:
    def __init__(self, x, y, direction=Directions.up):
        self.x = x
        self.y = y
        self.direction = direction

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

