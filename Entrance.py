import sqlite3

import pygame.mouse

from Constants import *
from Settings import Setting
from button import Button


class Enter:
    def __init__(self):
        self.icon = pygame.image.load(os.path.join('images', 'top_user.png'))
        self.logo_img = pygame.image.load(os.path.join('images', 'logo.png'))
        self.alpha = 255
        self.comments_special = 'Чтобы сохранить имя или пароль при окончание введения нажмите enter'
        self.blocks = []
        self.current_menu_index_block = 0
        self.con = sqlite3.connect('database/users.db')
        cur = self.con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS USERS (
            password TEXT,
            name TEXT
        )""")

    def append_block_menu(self, name_block):
        """
        Добавление в окно меню новых блоков
        :param name_block:
        :return:
        """
        self.blocks.append(name_block)

    def draw_buttons(self, screen):
        """
        Рисование на экране кнопок меню. Каждая кнопка это экземпляр класса Button
        из файла button.py
        :param screen:
        :return:
        """
        button_name = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150, 250, 60, 'Ввести имя',
                             'images/button_image.png')
        button_name.draw(screen)
        button_password = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - button_name.rect.height + 40
                                 , 250, 60, 'Ввести пароль',
                                 'images/button_image.png')
        button_password.draw(screen)
        button_call_window_settings = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, 250, 60, 'Настройки',
                                             'images/button_settings.png')
        button_call_window_settings.draw(screen)
        return [button_name, button_password, button_call_window_settings]

    def screensaver_before_work(self, screen):
        """
        Отрисовывает заставку, которая с каждым clock.tick(FPS) будет проявляться, благодаря этому
        создаётся эффект загрузки
        :param screen:
        :return:
        """
        surface_blur = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        surface_blur.fill((0, 0, 0, self.alpha))
        screen.blit(surface_blur, (0, 0))
        self.alpha -= 10

    def update_commenting(self, screen):
        """
        Отрисовывает на специальном поле, происходящие события для более удобного пользовательского
        интерфейса
        :param screen:
        :return:
        """
        text = FONT_24.render(self.comments_special, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 5))

    def switch_block(self, cur_index):
        """
        Обновление поля класса через текущий индекс в меню, предусмотрен выход за пределы длины всех блоков
        :param cur_index:
        :return:
        """
        index = min(self.current_menu_index_block + cur_index, len(self.blocks) - 1)
        self.current_menu_index_block = max(0, index)

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.fill(DARK_GREEN)
        pygame.display.set_caption('Меню')
        pygame.display.set_icon(self.icon)
        # pygame.mixer.music.load(os.path.join('music', 'first.mp3'))
        # pygame.mixer.music.play()
        clock = pygame.time.Clock()
        name_intermed_save = ''
        password_intermed_save = ''
        running = True
        move_to_password = False
        while running:
            clock.tick(FPS)
            inputting_data = True
            screen.fill(DARK_GREEN)
            buttons = self.draw_buttons(screen)
            if len(password_intermed_save) > 9 or len(name_intermed_save) > 9:
                inputting_data = False
                self.comments_special = 'Слишком длинное поле'
                self.update_commenting(screen)
            elif len(password_intermed_save) < 9:
                inputting_data = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif inputting_data and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and move_to_password is True:
                        # если нажата клавиша enter и пользователь сейчас находится на поле ввода пароля
                        self.switch_block(1)
                        cur = self.con.cursor()
                        search_user = cur.execute('''SELECT name FROM USERS WHERE name = ?''',
                                                  (name_intermed_save,)).fetchone()
                        if not search_user:
                            # если в таблице не было найдено такого имени, то добавляем в таблицу
                            cur = self.con.cursor()
                            cur.execute("INSERT INTO USERS (password, name) VALUES (?, ?)",
                                        (password_intermed_save, name_intermed_save))
                            self.con.commit()
                            self.comments_special = 'Вы успешно зарегистрировались'
                            self.update_commenting(screen)
                        else:
                            self.comments_special = 'Пользователь с таким именем уже существует'
                            self.update_commenting(screen)
                        check_exist_user = cur.execute('''SELECT name FROM USERS WHERE name = ? AND password = ?''',
                                                       (name_intermed_save, password_intermed_save)).fetchone()
                        check_true_password = cur.execute('''SELECT name FROM USERS WHERE password = ?''',
                                                          (name_intermed_save,)).fetchone()
                        if check_exist_user:
                            # все данные есть в таблице и они корректны
                            self.comments_special = f'Вы успешно вошли в аккаунт под именем {name_intermed_save}'
                            self.update_commenting(screen)
                        elif not check_true_password:
                            # нет запроса, значит есть некорректные данные
                            self.comments_special = f'Имя или пароль введены неверно'
                            self.update_commenting(screen)
                    elif event.key == pygame.K_RETURN:
                        # переключение на блок введение пароля без нажатия кнопки
                        self.switch_block(1)
                        inputting_data = False
                        move_to_password = True
                        self.comments_special = 'Переключились на введение пароля'
                        self.update_commenting(screen)
                        name_intermed_save = password_intermed_save
                        password_intermed_save = ''
                    elif event.key == pygame.K_BACKSPACE:
                        password_intermed_save = password_intermed_save[:-1]
                    else:
                        password_intermed_save += event.unicode
                        self.comments_special = 'Вводятся символы'
                        self.update_commenting(screen)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        # удаление последнего символа при нажатии на backspace
                        password_intermed_save = password_intermed_save[:-1]
                        self.comments_special = 'Удаляются символы'
                        self.update_commenting(screen)
                # обработка нажатий на кнопки
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if buttons[0].check_click(pos):
                        self.switch_block(-1)
                        move_to_password = False
                        self.comments_special = 'Переключение на введение имени'
                        self.update_commenting(screen)
                    elif buttons[1].check_click(pos):
                        self.switch_block(1)
                        move_to_password = True
                        self.comments_special = 'Переключились на введение пароля'
                        self.update_commenting(screen)
                    elif buttons[2].check_click(pos):
                        self.switch_block(1)
                        self.comments_special = 'Переход на настройки'
                        self.update_commenting(screen)
                        running = False
                        setting = Setting()
                        setting.run()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_TAB]:
                password_intermed_save = True
            self.draw_buttons(screen)
            buttons[0].draw(screen)
            buttons[1].draw(screen)
            buttons[2].draw(screen)
            if self.alpha > 0:
                self.screensaver_before_work(screen)
            if not move_to_password:
                text = FONT_24.render(password_intermed_save, True, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 135))
            else:
                text = FONT_24.render(password_intermed_save, True, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 15))
            if self.current_menu_index_block != 0:
                text = FONT_24.render('Имя', True, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 - 180))
            else:
                text = FONT_24.render('Имя', True, PINK)
                screen.blit(text, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 - 180))
            if self.current_menu_index_block != 1:
                text = FONT_24.render('Пароль', True, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 - 80))
            else:
                text = FONT_24.render('Пароль', True, PINK)
                screen.blit(text, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 - 80))
            text = FONT_38.render('Комментарии', True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))
            self.update_commenting(screen)
            pygame.display.update()
