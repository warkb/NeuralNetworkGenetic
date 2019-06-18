import numpy as np
import pygame
from enum import Enum
from pygame.sprite import Sprite
from game_params import *
from game_clases.rendered_object import RenderedObject

class Grass(Sprite, RenderedObject):
    grow_time = 10 # за столько времени вырастет трава
    def __init__(self, x, y):
        # self.x = x
        # self.y = y
        RenderedObject.__init__(self, x, y, 'img/grass.png')
        self.growed = True # выросла ли трава или нет
        # self.image = pygame.image.load('img/grass.png')
        # self.image = pygame.transform.scale(self.image, (SPRITE_SIZE, SPRITE_SIZE))
        # self.rect = self.image.get_rect()

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
