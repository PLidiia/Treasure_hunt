import sqlite3

import pygame.mouse

from Constants import *
from Effects import screensaver_before_work
from Levels import Choicer_Level
from Settings import Setting
from button import Button


class Enter:
    def __init__(self, turn, language):
        self.icon = pygame.image.load(os.path.join('images', 'top_user.png'))
        self.alpha = 255
        self.turning = turn
        self.language = language
        self.comments_special = 'Чтобы сохранить имя или пароль при окончание введения нажмите enter'
        self.blocks = []
        self.current_menu_index_block = 0
        self.image_background = pygame.image.load("images/menu_background.png")
        self.con = sqlite3.connect('database/users.db')
        cur = self.con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS USERS (
            password TEXT,
            name TEXT
        )""")
        self.long_field = 'Слишком длинное поле'
        self.successfull_reg = 'Вы успешно зарегистрировались'
        self.user_was = 'Пользователь с таким именем уже существует'
        self.wrong_field = 'Имя или пароль введены неверно'
        self.input_password = 'Переключились на введение пароля'
        self.inputting_chars = 'Вводятся символы'
        self.delete_chars = 'Удаляются символы'
        self.input_name = 'Переключение на введение имени'
        self.move_to_settings = 'Переход на настройки'
        self.title = 'Комментарии'
        self.text_input_password = 'Ввести пароль'
        self.text_input_name = 'Ввести имя'
        self.text_settings = 'Настройки'
        self.name = 'Имя'
        self.password = 'Пароль'
        self.successfull_login = 'Вы успешно вошли в аккаунт под именем'
        self.empty_field = 'Пустое поле для пароля или имени'
        self.nums_in_password = 'Пароль должен содержать цифры'
        self.letters_upper_in_password = 'Пароль должен содержать заглавные буквы'
        self.letters_lower_in_password = 'Пароль должен содержать строчные буквы'
        self.letters_special_in_password = 'Пароль должен содержать специальные символы'
        self.translate_fields_menu = []
        self.translate_fields_menu.append(self.long_field)
        self.translate_fields_menu.append(self.successfull_reg)
        self.translate_fields_menu.append(self.user_was)
        self.translate_fields_menu.append(self.wrong_field)
        self.translate_fields_menu.append(self.input_password)
        self.translate_fields_menu.append(self.inputting_chars)
        self.translate_fields_menu.append(self.delete_chars)
        self.translate_fields_menu.append(self.input_name)
        self.translate_fields_menu.append(self.move_to_settings)
        self.translate_fields_menu.append(self.title)
        self.translate_fields_menu.append(self.text_input_password)
        self.translate_fields_menu.append(self.text_input_name)
        self.translate_fields_menu.append(self.text_settings)
        self.translate_fields_menu.append(self.name)
        self.translate_fields_menu.append(self.password)
        self.translate_fields_menu.append(self.successfull_login)
        self.translate_fields_menu.append(self.empty_field)
        self.translate_fields_menu.append(self.nums_in_password)
        self.translate_fields_menu.append(self.letters_upper_in_password)
        self.translate_fields_menu.append(self.letters_lower_in_password)
        self.translate_fields_menu.append(self.letters_special_in_password)
        self.move_to_settings = False

    def append_block_menu(self, name_block):
        """
        Добавление в окно меню новых блоков
        :param name_block:
        :return:
        """
        self.blocks.append(name_block)

    def draw_items(self, screen):
        """
        Рисование на экране кнопок меню. Каждая кнопка это экземпляр класса Button
        из файла button.py
        :param screen:
        :return:
        """
        button_name = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150, 250, 60, self.translate_fields_menu[13],
                             'images/button_image.png')
        button_name.draw(screen)
        button_password = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - button_name.rect.height + 40
                                 , 250, 60, self.translate_fields_menu[10],
                                 'images/button_image.png')
        button_password.draw(screen)
        button_call_window_settings = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, 250, 60,
                                             self.translate_fields_menu[12],
                                             'images/button_settings.png')
        button_call_window_settings.draw(screen)
        return [button_name, button_password, button_call_window_settings]

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

    def launch_choice_menu(self, name_user):
        choicer = Choicer_Level(name_user, self.language, self.turning)
        choicer.run()

    def counting_chars(self, your_password):
        count_numbers = len([x for x in your_password if x.isdigit()])
        count_upper = len([x for x in your_password if x.isupper()])
        count_lower = len([x for x in your_password if x.islower()])
        new_len = count_numbers + count_upper + count_lower
        return new_len

    def validator(self, user_password):
        user_password = str(user_password)
        if not [x for x in user_password if x.isdigit()]:
            return self.translate_fields_menu[17]
        elif not [x for x in user_password if x.isupper()]:
            return self.translate_fields_menu[18]
        elif not [x for x in user_password if x.islower()]:
            return self.translate_fields_menu[19]
        elif self.counting_chars(user_password) == len(user_password):
            return self.translate_fields_menu[20]
        return user_password

    def double_text(self, text):
        if text != self.comments_special:
            return True
        return False

    def control_len_input_fields(self, password_intermed_save, name_intermed_save, screen):
        if len(password_intermed_save) > 9 or len(name_intermed_save) > 9:
            if self.double_text(self.translate_fields_menu[0]):
                self.comments_special = self.translate_fields_menu[0]
                self.update_commenting(screen)
            return False
        else:
            return True

    def run(self, fields):
        '''Функция screensaver_before_work работает не совсем корректно в отличие от других окон, это может быть
        связано с большим объёмом стека событий, что делает запуск данного окна менее плавным, чем
        например в окнах Settings и Levels'''
        self.translate_fields_menu = self.translate_fields_menu if not fields else fields
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Меню')
        pygame.display.set_icon(self.icon)
        if self.turning is True:
            pygame.mixer.music.load(os.path.join('music', 'first.mp3'))
            pygame.mixer.music.play()
        name_intermed_save = ''
        password_intermed_save = ''
        clock = pygame.time.Clock()
        running = True
        move_to_password = False
        entrance_about = True
        finish_password = False
        inputting_data = True
        start_menu = False
        one_message_about_switch = 0
        while running:
            clock.tick(FPS)
            screen.blit(self.image_background, (0, 0))
            buttons = self.draw_items(screen)
            inputting_data = self.control_len_input_fields(password_intermed_save, name_intermed_save, screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        # удаление последнего символа
                        if move_to_password is True:
                            password_intermed_save = password_intermed_save[:-1]
                        else:
                            name_intermed_save = name_intermed_save[:-1]
                    elif event.key == pygame.K_RETURN:
                        if move_to_password is True:
                            self.switch_block(1)
                            finish_password = True
                        else:
                            self.switch_block(1)
                            move_to_password = True
                    elif entrance_about is True:
                        inputting_data = self.control_len_input_fields(password_intermed_save, name_intermed_save,
                                                                       screen)
                        if inputting_data is True:
                            if move_to_password is True:
                                if one_message_about_switch == 0:
                                    if self.double_text(self.translate_fields_menu[4]):
                                        self.comments_special = self.translate_fields_menu[4]
                                        self.update_commenting(screen)
                                        one_message_about_switch = 1
                                password_intermed_save += event.unicode
                            else:
                                if self.double_text(self.translate_fields_menu[5]):
                                    self.comments_special = self.translate_fields_menu[5]
                                    self.update_commenting(screen)
                                name_intermed_save += event.unicode
                # обработка нажатий на кнопки
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if buttons[0].check_click(pos):
                        self.switch_block(-1)
                        move_to_password = False
                        if self.double_text(self.translate_fields_menu[7]):
                            self.comments_special = self.translate_fields_menu[7]
                            self.update_commenting(screen)
                    elif buttons[1].check_click(pos):
                        self.switch_block(1)
                        move_to_password = True
                        if one_message_about_switch == 0:
                            self.comments_special = self.translate_fields_menu[4]
                            self.update_commenting(screen)
                    elif buttons[2].check_click(pos):
                        self.switch_block(0)
                        move_to_password = False
                        self.move_to_settings = True
                        running = False
                        setting = Setting(self, self.translate_fields_menu)
                        setting.run()
            self.draw_items(screen)
            for elem in range(0, len(buttons) - 1):
                buttons[elem].draw(screen)
            if self.alpha > 0:
                self.alpha = screensaver_before_work(screen, self.alpha, 15)
            if finish_password:
                if move_to_password is True and entrance_about is True:
                    # если нажата клавиша enter и пользователь сейчас находится на поле ввода пароля
                    self.switch_block(1)
                    if name_intermed_save != '' and password_intermed_save != '':
                        validate_password_user = self.validator(password_intermed_save)
                        # !!! Логика. При вводе пароля не подходящему критериям, выводится сообщение, несмотря
                        # на то что пароль был неверным по отношению к данному имени, выбранного из бд
                        if validate_password_user == password_intermed_save:
                            cur = self.con.cursor()
                            search_name = cur.execute('''SELECT name FROM USERS WHERE name = ?''',
                                                      (name_intermed_save,)).fetchone()
                            if not search_name:
                                # если в таблице не было найдено такого имени, то добавляем в таблицу
                                cur = self.con.cursor()
                                cur.execute("INSERT INTO USERS (password, name) VALUES (?, ?)",
                                            (password_intermed_save, name_intermed_save))
                                self.con.commit()
                                if self.double_text(self.translate_fields_menu[1]):
                                    self.comments_special = self.translate_fields_menu[1]
                                    self.update_commenting(screen)
                                    self.launch_choice_menu(name_user=name_intermed_save)
                            else:
                                entrance_about = False
                                if self.double_text(self.translate_fields_menu[2]):
                                    self.comments_special = self.translate_fields_menu[2]
                                    self.update_commenting(screen)
                            check_exist_user = cur.execute(
                                '''SELECT name FROM USERS WHERE password = ? AND name = ?''',
                                (password_intermed_save, name_intermed_save)).fetchone()
                            if check_exist_user:
                                # уже вошли
                                entrance_about = False
                                # все данные есть в таблице и они корректны
                                if self.double_text(f'{self.translate_fields_menu[15]} {name_intermed_save}'):
                                    self.comments_special = f'{self.translate_fields_menu[15]} {name_intermed_save}'
                                    self.update_commenting(screen)
                                    self.launch_choice_menu(name_user=name_intermed_save)

                            else:
                                if self.double_text(self.translate_fields_menu[3]):
                                    self.comments_special = self.translate_fields_menu[3]
                                    self.update_commenting(screen)
                        else:
                            self.comments_special = validate_password_user
                            self.update_commenting(screen)
                    else:
                        if self.validator(password_intermed_save) != password_intermed_save:
                            if self.double_text(self.translate_fields_menu[16]):
                                self.comments_special = self.translate_fields_menu[16]
                                self.update_commenting(screen)
                elif move_to_password is False:
                    # клавиша enter нажата при окончании введении имени, значит будет  введние пароля
                    # переключение на блок введение пароля без нажатия кнопки
                    self.switch_block(1)
                    inputting_data = False
                    move_to_password = True
                    if self.double_text(self.translate_fields_menu[4]):
                        self.comments_special = self.translate_fields_menu[4]
                        self.update_commenting(screen)
                    name_intermed_save = password_intermed_save
                    password_intermed_save = ''
            if not move_to_password:
                text = FONT_24.render(name_intermed_save, True, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 135))
            else:
                text = FONT_24.render(password_intermed_save, True, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 15))
            if self.current_menu_index_block != 0:
                text = FONT_24.render(self.translate_fields_menu[13], True, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 - 180))
            else:
                text = FONT_24.render(self.translate_fields_menu[13], True, PINK)
                screen.blit(text, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 - 180))
            if self.current_menu_index_block != 1:
                text = FONT_24.render(self.translate_fields_menu[14], True, WHITE)
                screen.blit(text, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 - 80))
            else:
                text = FONT_24.render(self.translate_fields_menu[14], True, PINK)
                screen.blit(text, (SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 - 80))
            text = FONT_38.render(self.translate_fields_menu[9], True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))
            self.update_commenting(screen)
            pygame.display.update()
