import pygame.display
import translate

from Constants import *
from button import Button


class Setting:
    def __init__(self):
        pass

    def translate(self, text, from_lang, to_lang):
        translator = translate.Translator(from_lang=from_lang, to_lang=to_lang)
        end_text = translator.translate(text)
        return end_text

    def draw_items(self, screen):
        button_choice_language = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150, 250, 60, 'Выберите язык',
                                        'images/button_image.png')
        button_choice_language.draw(screen)
        button_save_changes = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - button_choice_language.rect.height + 40
                                     , 250, 60, 'Сохранить изменение',
                                     'images/button_image.png')
        button_save_changes.draw(screen)
        return [button_choice_language, button_save_changes]

    def run(self, screen):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        running = True
        while running:
            screen.fill(DARK_GREEN)
            text = FONT_38.render('Настройки игры', True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 25))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                pygame.display.update()
