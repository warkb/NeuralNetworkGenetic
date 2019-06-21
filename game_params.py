import pygame
pygame.init()
FPS = 5


GRASSES_COUNT = 40
PIGS_COUNT = 80
WOLFS_COUNT = 40

# экран
WIDTHSCREEN = pygame.display.Info().current_w
HEIGHTSCREEN = pygame.display.Info().current_h
MAINCOLOR = (21, 209, 137)


SPRITE_SIZE = 75 # размер спрайта в пикселях

WIDTH = WIDTHSCREEN // SPRITE_SIZE # ширина поля в клетках
HEIGHT = HEIGHTSCREEN // SPRITE_SIZE # высота поля в клетках

MAIN_FONT_SIZE = 18