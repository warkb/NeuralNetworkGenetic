from game_clases.critter import Critter
from classes import *
from classes import WIDTH, HEIGHT
import pygame
from pygame.locals import *
import random
from game_params import *


WIDTHSCREEN = 1024
HEIGHTSCREEN = 768
MAINCOLOR = (21, 209, 137)

TOP_MARGIN = (HEIGHTSCREEN - HEIGHT * SPRITE_SIZE) / 2
LEFT_MARGIN = (WIDTHSCREEN - WIDTH * SPRITE_SIZE) / 2

class Game():
    def __init__(self):
        self.press_keys = type('keys', (), {})() # класс, содержащий нажатые классы для контроллера
        self.allObjects = {}
        self.grasses = self.makeGameObjectsList(Grass, GRASSES_COUNT)
        self.pigs = self.makeGameObjectsList(Pig, PIGS_COUNT)
        player_pig = Pig(0,0, self)
        player_pig.controller = player_pig.keyboard_controller
        self.pigs.append(player_pig)
        self.wolfs = self.makeGameObjectsList(Wolf, WOLFS_COUNT)
        # for obj in self.grasses + self.pigs + self.wolfs:
        #     print(obj)
        self.init_keys()

    def init_keys(self):
        self.press_keys.up = False
        self.press_keys.down = False
        self.press_keys.left = False
        self.press_keys.right = False
        self.press_keys.walk = False
        self.press_keys.eat = False

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
            if cls == Grass:
                result.append(cls(x, y))
            else:
                result.append(cls(x, y, self))
        return result

    def mainLoop(self):
        while self.running:
            self.init_keys()
            for event in pygame.event.get():
                if event.type == QUIT:
                    # выходим по нажатию на крестик
                    self.running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False

                    # управление
                    if event.key == K_w:
                        self.press_keys.up = True
                    if event.key == K_a:
                        self.press_keys.left = True
                    if event.key == K_d:
                        self.press_keys.right = True
                    if event.key == K_s:
                        self.press_keys.down = True
                    if event.key == K_SPACE:
                        self.press_keys.walk = True
                    if event.key == K_e:
                        self.press_keys.eat = True

            self.screen.fill(MAINCOLOR)

            # двигаем всех
            for obj in self.wolfs + self.pigs:
                obj.make_move()

            # рисуем всех
            for obj in self.grasses + self.pigs + self.wolfs:
                obj.updateRect(TOP_MARGIN, LEFT_MARGIN)
                self.screen.blit(obj.image, obj.rect)
            pygame.display.update()
            self.fpsClock.tick(FPS)

    def main(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTHSCREEN, HEIGHTSCREEN), 0, 32)
        self.running = True
        self.fpsClock = pygame.time.Clock()
        self.mainLoop()


if __name__ == '__main__':
    Game().main()