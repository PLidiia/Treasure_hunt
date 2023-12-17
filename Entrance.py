import os

import pygame

from Constants import *


class Enter:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Login/registration')
        self.logo_img = pygame.image.load(os.path.join('images', 'logo.png'))
        self.file_font = os.path.join('fonts', 'RubikDoodleShadow-Regular.ttf')
        self.font_entrance = pygame.font.Font(self.file_font, 38)

    def draw_text(self, text, x, y, color=BLACK):
        text_to_render = pygame.font.Font.render(
            self.font_entrance,
            text,
            1,
            color)
        self.screen.blit(text_to_render, (x, y))
        return text_to_render

    def draw_items(self):
        self.screen.fill(DARK_GREEN)
        self.screen.blit(self.logo_img, (((SCREEN_WIDTH - self.logo_img.get_width()) // 2), 0))
        self.draw_text("Добро пожаловать в игру охота за сокровищами", 0, self.logo_img.get_height(), color=DARK_RED)
        text_object_1 = self.draw_text("Добро пожаловать в игру охота за сокровищами", 0,
                                     self.logo_img.get_height(), color=DARK_RED)
        self.draw_text("Введите своё имя", 25, self.logo_img.get_height() + text_object_1.get_height(), color=DARK_RED)
        text_object_2 = self.draw_text("Введите своё имя", 25,
                                      self.logo_img.get_height() + text_object_1.get_height(), color=DARK_RED)
        self.draw_text("Введите свою почту", 25, self.logo_img.get_height() +
                       text_object_2.get_height() + text_object_1.get_height(), color=DARK_RED)
        pygame.display.update()

    def run(self):
        pygame.init()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.draw_items()
