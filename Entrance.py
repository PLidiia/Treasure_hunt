import sqlite3

import pygame.mouse

from Constants import *
from button import Button


class Enter:
    def __init__(self):
        self.icon = pygame.image.load(os.path.join('images', 'top_user.png'))
        self.logo_img = pygame.image.load(os.path.join('images', 'logo.png'))
        self.alpha = 255
        self.comments_special = ''
        self.con = sqlite3.connect('database/users.db')
        cur = self.con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS USERS (
            password TEXT,
            name TEXT
        )""")

    def draw_items(self, screen):
        # концепция кнопок не совсем уместна, потому что не обрабатываются для кнопок button_name
        # и button_db нажатия и кнопки используются только как плашки с текстом
        button_name = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150, 250, 60, 'Ввести имя',
                             'images/button_image.png')
        button_name.draw(screen)
        button_db = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - button_name.rect.height + 40
                           , 250, 60, 'Ввести пароль',
                           'images/button_image.png')
        button_db.draw(screen)
        return [button_name, button_db]

    def screensaver(self, screen):
        surface_blur = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        surface_blur.fill((0, 0, 0, self.alpha))
        screen.blit(surface_blur, (0, 0))
        self.alpha -= 10

    def update_commenting(self, screen):
        text = FONT_24.render(self.comments_special, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 5))

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.fill(DARK_GREEN)
        pygame.display.set_caption('Меню')
        pygame.display.set_icon(self.icon)
        pygame.mixer.music.load(os.path.join('music', 'first.mp3'))
        pygame.mixer.music.play()
        enter = Enter()
        name_intermed_save = ''
        input_text = ''
        run = True
        move_to_mail = False
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            inputting_data = True
            screen.fill(DARK_GREEN)
            buttons = self.draw_items(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif inputting_data and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and move_to_mail is True:
                        cur = self.con.cursor()
                        search_user = cur.execute('''SELECT name FROM USERS WHERE name = ?''',
                                                  (name_intermed_save,)).fetchone()
                        if not search_user:
                            cur = self.con.cursor()
                            cur.execute("INSERT INTO USERS (password, name) VALUES (?, ?)",
                                        (name_intermed_save, input_text))
                            self.con.commit()
                            self.comments_special = 'Пользователь с таким именем уже существует'
                            self.update_commenting(screen)
                        else:
                            self.comments_special = 'Пользователь с таким именем уже существует'
                            self.update_commenting(screen)
                    elif event.key == pygame.K_RETURN:
                        inputting_data = False
                        move_to_mail = True
                        self.comments_special = 'Переключились на введение пароля'
                        self.update_commenting(screen)
                        name_intermed_save = input_text
                        input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                        self.comments_special = 'Вводятся символы'
                        self.update_commenting(screen)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                        self.comments_special = 'Удаляются символы'
                        self.update_commenting(screen)
            if len(input_text) > 9 or len(name_intermed_save) > 9:
                inputting_data = False
                self.comments_special = 'Слишком длинное поле'
                self.update_commenting(screen)
            elif len(input_text) < 9:
                inputting_data = True
            keys = pygame.key.get_pressed()
            if keys[pygame.K_TAB]:
                input_text = True
            self.draw_items(screen)
            buttons[0].draw(screen)
            buttons[1].draw(screen)
            if self.alpha > 0:
                self.screensaver(screen)
            if not move_to_mail:
                text = FONT_24.render(input_text, True, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 135))
            else:
                text = FONT_24.render(input_text, True, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 15))
            text = FONT_24.render('Имя', True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 - 180))
            text = FONT_24.render('Пароль', True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 - 80))
            text = FONT_38.render('Комментарии', True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))
            self.update_commenting(screen)
            pygame.display.update()
