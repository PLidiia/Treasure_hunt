import pygame
import os

pygame.font.init()
all_sprites = pygame.sprite.Group()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60
DARK_GREEN = (87, 122, 77)
DARK_RED = (163, 0, 34)
BROWN = (77, 8, 4)
BLACK = (0, 0, 0)
WHITE = (0, 0, 0)
BLUE = (65, 179, 222)
PINK = (255, 208, 214)
file_font = os.path.join('fonts', 'RubikDoodleShadow-Regular.ttf')
FONT_38 = pygame.font.Font(file_font, 38)
FONT_24 = pygame.font.Font(file_font, 24)
FONT_12 = pygame.font.Font(file_font, 12)