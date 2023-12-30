import pygame.display
import translate

from Constants import *
from button import Button


class Setting:
    def __init__(self):
        self.translator = translate.Translator(from_lang='ru', to_lang='ru')

    def translate(self, to_lang):
        translator = translate.Translator(from_lang='ru', to_lang=to_lang)
        self.translator = translator
        # end_text = translator.translate(text)
        # return end_text

    def draw_buttons(self, screen):
        button_choice_language = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150, 250, 60, 'Выберите язык',
                                        'images/button_image.png')
        button_choice_language.draw(screen)
        button_save_changes = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - button_choice_language.rect.height + 40
                                     , 250, 60, 'Сохранить изменение',
                                     'images/button_image.png')
        button_save_changes.draw(screen)
        return [button_choice_language, button_save_changes]

    def draw_language_menu(self, screen, buttons):
        margin = buttons[0].rect.width
        button_eng = Button(SCREEN_WIDTH // 2 + margin, 25, 120, 45, 'Английский',
                            'images/eng.jpg')
        button_eng.draw(screen, font=FONT_24_CLASSIC, color_font=BLUE)
        button_german = Button(SCREEN_WIDTH // 2 + margin,
                               SCREEN_HEIGHT // 2 - 225, 120, 45,
                                     'Немецкий',
                                     'images/ger.jpg')
        button_german.draw(screen, font=FONT_24_CLASSIC, color_font=BLUE)

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Настройки')
        running = True
        drawing_language_menu = False
        while running:
            screen.fill(DARK_GREEN)
            text = FONT_38.render('Настройки игры', True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 25))
            buttons = self.draw_buttons(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if drawing_language_menu is True:
                self.draw_language_menu(screen, buttons)
            elif buttons[0].check_click(pygame.mouse.get_pos()):
                self.draw_language_menu(screen, buttons)
                drawing_language_menu = True
            pygame.display.update()

    # def return_translator(self):
    #     return
