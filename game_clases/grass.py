import numpy as np
import pygame
from enum import Enum
from pygame.sprite import Sprite
from game_params import *
from game_clases.rendered_object import RenderedObject
import random

class Grass(RenderedObject):
    grow_time = 10 # за столько времени вырастет трава
    def __init__(self, x, y):
        # self.x = x
        # self.y = y

        RenderedObject.__init__(self, x, y, 'img/grass.png')
        self.growed_step = self.grow_time # осталось шагов до того, чтобы цветку вырасти
        # self.image = pygame.image.load('img/grass.png')
        # self.image = pygame.transform.scale(self.image, (SPRITE_SIZE, SPRITE_SIZE))
        # self.rect = self.image.get_rect()

    @property
    def growed(self):
        return self.growed_step <= 0

    def be_eat(self):
        """Трава была съедена"""
        self.growed_step = self.grow_time

    def __str__(self):
        return 'Это Трава с координатами (%s, %s)' % (self.x, self.y)

    def draw(self, screen):
        if self.growed_step > 0:
            self.growed_step -= random.choice([0, 1, 2])
        else:
            RenderedObject.draw(self, screen)