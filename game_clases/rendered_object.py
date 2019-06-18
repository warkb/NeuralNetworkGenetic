import pygame
from game_params import *

class RenderedObject:
    """
    Объект, отображаемый на экране
    """
    TOP_MARGIN = (HEIGHTSCREEN - HEIGHT * SPRITE_SIZE) / 2
    LEFT_MARGIN = (WIDTHSCREEN - WIDTH * SPRITE_SIZE) / 2
    def __init__(self, x, y, path_to_img):
        self.x = x
        self.y = y
        self.initImage(path_to_img)

    def initImage(self, link):
        """
        делает для класса изображение и прямоугольник с координатами
        :param link:
        :return:
        """
        self.image = pygame.image.load(link)
        self.image = pygame.transform.scale(self.image, (SPRITE_SIZE, SPRITE_SIZE))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        """
        Рисует объект на экране
        :param screen:
        :return:
        """
        self.updateRect(self.TOP_MARGIN, self.LEFT_MARGIN)
        screen.blit(self.image, self.rect)