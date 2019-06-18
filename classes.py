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
    def __init__(self, x, y, game):
        super().__init__(x, y, 'img/pig.png', game)
        self.initEnergy(100, 10)

    def __str__(self):
        return 'Это Свинья с координатами (%s, %s)' % (self.x, self.y)

    def eat(self):
        grasses_for_eat = list(filter(lambda obj: obj.growed, self.game.get_objects_near(self.x, self.y).grasses))
        if len(grasses_for_eat) > 0:
            grass = grasses_for_eat[0]
            grass.be_eat()
            self.update_energy()



class Wolf(Critter):
    def __init__(self, x, y, game):
        super().__init__(x, y, 'img/wolf.png', game)
        self.initEnergy(100, 25)

    def __str__(self):
        return 'Это Волк с координатами (%s, %s)' % (self.x, self.y)

    def eat(self):
        pigs_for_eat = list(filter(lambda obj: True, self.game.get_objects_near(self.x, self.y).pigs))
        if len(pigs_for_eat) > 0:
            pig = pigs_for_eat[0]
            self.game.remove_pig(pig)
            self.update_energy()

