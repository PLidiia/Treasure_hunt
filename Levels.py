import pygame.mouse

from Constants import *
from button import Button
from map_1 import Level
from pathes_about_map import Level_1


class choice_levels:
    def __init__(self, name_user):
        self.name_user = name_user

    def draw_items(self, screen):
        text = FONT_24.render(self.name_user, True, WHITE)
        screen.blit(text, (10, 10))
        text = FONT_38.render('Карта 1', True, BLUE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2 - 100, SCREEN_HEIGHT // 2 -
                           text.get_height() // 2))
        map_1 = pygame.image.load('images/map_1.png').convert_alpha()
        width = 100
        height = 100
        map_1 = pygame.transform.scale(map_1, (width, height))
        map_1_rect = map_1.get_rect(topleft=(SCREEN_WIDTH // 2 - text.get_width() // 2 - 100
                                             , SCREEN_HEIGHT // 2 - text.get_height() // 2 + 100))
        screen.blit(map_1, map_1_rect)
        button_launch_map_1 = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100, 120, 50, 'Запустить карту'
                                     , 'images/button_levels.png')
        button_launch_map_1.draw(screen)
        return [button_launch_map_1]

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Уровни игры')
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                clock.tick(FPS)
                screen.fill(DARK_GREEN)
                buttons = self.draw_items(screen)
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and buttons[0].check_click(pygame.mouse.get_pos()):
                    print(Level_1['terrain'])
                    level_1 = Level(self.name_user, Level_1['terrain'])
                    level_1.run()
            pygame.display.update()
