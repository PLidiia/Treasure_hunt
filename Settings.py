import pygame.display
import translate

from Constants import *
from button import Button
from Effects import screensaver_before_work


class Setting:
    def __init__(self, entry, list_fields=0):
        self.entry = entry
        self.list_fields = list_fields if not list_fields == 0 else []
        self.translator = translate.Translator(from_lang='ru', to_lang='ru')
        self.change_translator = False
        self.new_list_fields = []
        self.turning = True
        self.alpha = 255

    def translate(self, to_lang, from_to_lang='ru'):
        translator = translate.Translator(from_lang=from_to_lang, to_lang=to_lang)
        self.translator = translator
        for field in self.list_fields:
            new_field = self.translator.translate(field)
            self.new_list_fields.append(new_field)

    def draw_buttons(self, screen):
        button_choice_language = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150, 250, 60, 'Выберите язык',
                                        'images/button_image.png')
        button_choice_language.draw(screen)
        button_save_changes = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - button_choice_language.rect.height + 40
                                     , 250, 60, 'Сохранить изменение',
                                     'images/button_image.png')
        button_save_changes.draw(screen)
        button_back_to_menu = Button(10, 10, 250, 60, 'Вернуться в меню',
                                     'images/button_image.png')
        button_back_to_menu.draw(screen)
        button_music = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 280, 250, 60, 'Вкл\Выкл музыку',
                                        'images/button_image.png')
        button_music.draw(screen)
        return [button_choice_language, button_save_changes, button_back_to_menu, button_music]

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
        return [button_eng, button_german]

    def field_to_menu(self):
        return self.new_list_fields

    def check_was_launch(self):
        return self.change_translator

    def music_turn(self):
        self.turning = False

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
            buttons_settings = self.draw_buttons(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.entry.turning = self.turning
                    self.entry.run(self.new_list_fields)
                    running = False
            if self.alpha > 0:
                self.alpha = screensaver_before_work(screen, alpha=self.alpha)
            if drawing_language_menu is True:
                buttons_lang = self.draw_language_menu(screen, buttons_settings)
                if buttons_lang[0].check_click(pygame.mouse.get_pos()):
                    self.translate('en')
                    self.change_translator = True
                elif buttons_lang[1].check_click(pygame.mouse.get_pos()):
                    self.translate('de')
                    self.change_translator = True
            elif buttons_settings[0].check_click(pygame.mouse.get_pos()):
                buttons_lang = self.draw_language_menu(screen, buttons_settings)
                drawing_language_menu = True
            elif buttons_settings[2].check_click(pygame.mouse.get_pos()):
                self.entry.turning = self.turning
                self.entry.run(self.new_list_fields)
                running = False
            elif buttons_settings[3].check_click(pygame.mouse.get_pos()):
                self.turning = True
            pygame.display.update()

    # def return_translator(self):
    #     return
