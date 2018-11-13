from classes import *
from classes import WIDTH, HEIGHT
import pygame
from pygame.locals import *
import random

WIDTHSCREEN = 1024
HEIGHTSCREEN = 768
MAINCOLOR = (21, 209, 137)

TOP_MARGIN = (HEIGHTSCREEN - HEIGHT * SPRITE_SIZE) / 2
LEFT_MARGIN = (WIDTHSCREEN - WIDTH * SPRITE_SIZE) / 2

class Game():
    def __init__(self):
        self.allObjects = {}
        self.grasses = self.makeGameObjectsList(Grass, 50)
        self.pigs = self.makeGameObjectsList(Pig, 25)
        self.wolfs = self.makeGameObjectsList(Wolf, 10)
        for obj in self.grasses + self.pigs + self.wolfs:
            print(obj)

    def makeGameObjectsList(self, cls, number):
        """
        Создает number сущностей заданного класса со случайными координатами
        в прямоугольнике (WIDTH, HEIGHT)
        :param cls:
        :param number:
        :return:
        """
        result = []
        for i in range(number):
            x = random.randrange(WIDTH)
            y = random.randrange(HEIGHT)
            result.append(cls(x, y))
        return result

    def mainLoop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    # выходим по нажатию на крестик
                    self.running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
            self.screen.fill(MAINCOLOR)

            #рисуем всех
            for obj in self.grasses + self.pigs + self.wolfs:
                obj.updateRect(TOP_MARGIN, LEFT_MARGIN)
                self.screen.blit(obj.image, obj.rect)
            pygame.display.update()
            self.fpsClock.tick(30)

    def main(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTHSCREEN, HEIGHTSCREEN), 0, 32)
        self.running = True
        self.fpsClock = pygame.time.Clock()
        self.mainLoop()


if __name__ == '__main__':
    Game().main()