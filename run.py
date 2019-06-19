from game_clases.critter import Critter
from classes import *
from classes import WIDTH, HEIGHT
import pygame
from pygame.locals import *
import random
from game_params import *

class Game():
    def __init__(self):
        self.press_keys = type('keys', (), {})() # класс, содержащий нажатые классы для контроллера
        self.allObjects = {}
        self.holded_places = []
        self.grasses = self.makeGameObjectsList(Grass, GRASSES_COUNT)
        self.pigs = self.makeGameObjectsList(Pig, PIGS_COUNT)
        self.wolfs = self.makeGameObjectsList(Wolf, WOLFS_COUNT)
        player_wolf = Wolf(0,0, self)
        player_wolf.controller = player_wolf.keyboard_controller
        self.wolfs.append(player_wolf)
        # for obj in self.grasses + self.pigs + self.wolfs:
        #     print(obj)
        self.init_keys()
        self.last_delay = 1 # для отрисовки fps
        self.fpses = []

    def remove_pig(self, pig):
        if pig in self.pigs:
            self.pigs.remove(pig)
        pig.die()
        del pig

    def remove_wolf(self, wolf):
        if wolf in self.wolfs:
            self.wolfs.remove(wolf)
        wolf.die()
        del wolf

    def remove_critter(self, critter):
        if isinstance(critter, Pig):
            self.remove_pig(critter)
        else:
            self.remove_wolf(critter)

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
            while True:
                # для того, чтобы не было несколько животных в одной клетке
                if len(self.holded_places) >= WIDTH * HEIGHT:
                    raise BaseException('Нету места')
                x = random.randrange(WIDTH)
                y = random.randrange(HEIGHT)
                if cls == Grass:
                    # если трава то пофиг
                    result.append(cls(x, y))
                    break
                new_place = (x, y)
                if (new_place not in self.holded_places):
                    self.holded_places.append(new_place)
                    result.append(cls(x, y, self))
                    break
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
                # если кто-то может родить - пусть рожает
                if obj.has_child:
                    new_child = obj.make_child()
                    if isinstance(new_child, Pig):
                        self.pigs.append(new_child)
                    else:
                        self.wolfs.append(new_child)

            # рисуем всех
            maxPigCurrentLife = 0
            maxWolfCurrentLife = 0
            for obj in self.grasses + self.pigs + self.wolfs:
                if isinstance(obj, Pig):
                    maxPigCurrentLife = max(maxPigCurrentLife, obj.life_time)
                if isinstance(obj, Wolf):
                    maxWolfCurrentLife = max(maxWolfCurrentLife, obj.life_time)
                obj.draw(self.screen)
            # рисуем разную информацию
            maxPigLifeSurf = self.mainFont.render(
                f'Самая живучая свинья продержалась {max(Pig.best_lifetime, maxPigCurrentLife)} ходов',
                True, (255, 0, 0))
            maxPigLifeRect = maxPigLifeSurf.get_rect()
            maxPigLifeRect.topleft = (0, 0)

            self.screen.blit(maxPigLifeSurf, maxPigLifeRect)
            maxWolfLifeSurf = self.mainFont.render(
                f'Самый живучий волк продержался {max(Wolf.best_lifetime, maxWolfCurrentLife)} ходов',
                True, (255, 0, 0)
            )
            maxWolfLifeRect = maxWolfLifeSurf.get_rect()
            maxWolfLifeRect.topleft = (0, MAIN_FONT_SIZE)
            currentFps = round(1000 / self.last_delay)
            self.fpses.append(currentFps)
            fpsSurf = self.mainFont.render(f'FPS: {currentFps}', True, (255, 0, 0))
            fpsRect = fpsSurf.get_rect()
            fpsRect.topleft = (0, MAIN_FONT_SIZE * 2)
            self.screen.blit(maxWolfLifeSurf, maxWolfLifeRect)
            self.screen.blit(fpsSurf, fpsRect)
            # рисуем количество свиней
            pigsCountSurf = self.mainFont.render(f'Свиней: {len(self.pigs)}', True, (255, 0, 0))
            pigsCountRect = pigsCountSurf.get_rect()
            pigsCountRect.topleft = (0, MAIN_FONT_SIZE * 3)
            self.screen.blit(pigsCountSurf, pigsCountRect)
            # аналогично волков
            wolfsCountSurf = self.mainFont.render(f'Волков: {len(self.wolfs)}', True, (255, 0, 0))
            wolfsCountRect = wolfsCountSurf.get_rect()
            wolfsCountRect.topleft = (0, MAIN_FONT_SIZE * 4)
            self.screen.blit(wolfsCountSurf, wolfsCountRect)
            pygame.display.update()
            self.last_delay = self.fpsClock.tick(FPS)

    def get_objects_near(self, x, y):
        """
        Получает объекты в квадрате 3Х3 c центром в координатах x и y
        """
        result = type('Near_objects', (), {})
        result.grasses = []
        result.pigs = []
        result.wolfs = []
        for obj in self.grasses + self.wolfs + self.pigs:
            if abs(obj.x - x) < 2 and abs(obj.y - y) < 2:
                if isinstance(obj, Grass):
                    result.grasses.append(obj)
                if isinstance(obj, Pig):
                    result.pigs.append(obj)
                if isinstance(obj, Wolf):
                    result.wolfs.append(obj)
        return result

    def main(self):
        pygame.init()
        self.mainFont = pygame.font.Font('resourses\\arial.ttf', MAIN_FONT_SIZE)
        self.screen = pygame.display.set_mode((WIDTHSCREEN, HEIGHTSCREEN), 0, 32)
        self.running = True
        self.fpsClock = pygame.time.Clock()
        self.mainLoop()
        print(f'Средний fps: {sum(self.fpses) / len(self.fpses)}')


if __name__ == '__main__':
    Game().main()