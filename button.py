import pygame

from Constants import *


class Button:
    def __init__(self, x, y, w, h, text, image_path, hover_image_path=None, sound_path=None):
        # сохраняем геометрические параметры кнопки
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        # сохраняем графические параметры кнопки
        self.text = text
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.w, self.h))
        # сохраняем картинку при наведении, по умолчанию это тоже самая картинка
        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = pygame.image.load(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (self.w, self.h))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
        self.is_hovered = False

    def draw(self, screen, font=FONT_24):
        cur_image = self.hover_image if self.is_hovered else self.image
        screen.blit(cur_image, self.rect.topleft)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        """Проверяем коллизию между кнопкой и координатами мыши и сохраняем в атрибут класса
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.image = self.hover_image

    def button_event(self, event):
        '''Для событий, происходящих с кнопкой
        '''
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
        elif event.type == pygame.MOUSEBUTTONUP and self.is_hovered:
            self.is_hovered = False

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            return True
        else:
            return False