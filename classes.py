import numpy as np
import pygame
from enum import Enum
from pygame.sprite import Sprite
from game_params import *
from game_clases.grass import Grass
from game_clases.critter import Critter

percept = {
    "energy": 10,
    "x": 10,
    "y": 10
}

class Pig(Critter):
    max_lifetime = 0
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        self.initEnergy(100, 10)
        self.initImage('img/pig.png')

    def __str__(self):
        return 'Это Свинья с координатами (%s, %s)' % (self.x, self.y)


class Wolf(Critter):
    max_lifetime = 0
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        self.initEnergy(100, 25)
        self.initImage('img/wolf.png')

    def __str__(self):
        return 'Это Волк с координатами (%s, %s)' % (self.x, self.y)

