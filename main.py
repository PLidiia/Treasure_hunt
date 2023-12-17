import pygame

from Constants import *
from Entrance import Enter

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    entry = Enter()
    entry.run()