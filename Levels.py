import pygame.mouse

from Constants import *
from Effects import screensaver_before_work
from button import Button
from map_1 import Map
from pathes_about_map import Level_1


class Choicer_Level:
    def __init__(self, name_user, language, turn):
        self.name_user = name_user
        self.language = language
        self.turning = turn
        self.alpha = 255
        self.map_1 = 'Карта 1'
        self.launch_map = 'Запустить карту'
        self.levels_game = 'Уровни игры'
        self.choice_levels_menu = [self.map_1, self.launch_map, self.levels_game]
        self.choice_levels_menu_en = ['Map 1', 'Launch Map', 'Game Levels']
        self.choice_levels_menu_de = ['Karte 1', 'Karte einführen', 'Spiellevels']
        self.choice_levels_menu_fr = ['Carte 1', 'Carte de lancement', 'Niveaux de jeu']
        if self.language == 'en':
            self.choice_levels_menu = self.choice_levels_menu_en
        elif self.language == 'fr':
            self.choice_levels_menu = self.choice_levels_menu_fr
        elif self.language == 'de':
            self.choice_levels_menu = self.choice_levels_menu_de

    def draw_items(self, screen):
        text = FONT_24.render(self.name_user, True, WHITE)
        screen.blit(text, (10, 10))
        text = FONT_38.render(self.choice_levels_menu[0], True, BLUE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2 - 100, SCREEN_HEIGHT // 2 -
                           text.get_height() // 2))
        map_1 = pygame.image.load('images/map_1.png').convert_alpha()
        width = 100
        height = 100
        map_1 = pygame.transform.scale(map_1, (width, height))
        map_1_rect = map_1.get_rect(topleft=(SCREEN_WIDTH // 2 - text.get_width() // 2 - 100
                                             , SCREEN_HEIGHT // 2 - text.get_height() // 2 + 100))
        screen.blit(map_1, map_1_rect)
        button_launch_map_1 = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100, 120, 50,
                                     self.choice_levels_menu[1]
                                     , 'images/button_levels.png')
        button_launch_map_1.draw(screen)
        return [button_launch_map_1]

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(self.choice_levels_menu[2])
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(FPS)
            screen.fill(DARK_GREEN)
            buttons = self.draw_items(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and buttons[0].check_click(pygame.mouse.get_pos()):
                    level_1 = Map(Level_1, self.name_user, self.turning, self.language)
                    level_1.run()
            if self.alpha > 0:
                self.alpha = screensaver_before_work(screen, self.alpha, 2)
            pygame.display.update()
