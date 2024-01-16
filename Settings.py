import pygame.display

from Constants import *
from Effects import screensaver_before_work
from button import Button


class Setting:
    def __init__(self, entry, list_fields):
        self.entry = entry
        self.list_fields_menu = list_fields
        self.turning = True
        self.alpha = 255
        choice_lang = 'Выберите язык'
        save_changes = 'Сохранить изменение'
        back_to_menu = 'Вернуться в меню'
        turn_music = 'Вкл\Выкл музыку'
        english_lang = 'Английский'
        german_lang = 'Немецкий'
        french_lang = 'Французский'
        settings_menu = 'Настройки меню'
        translate_fields_settings = [choice_lang, save_changes, back_to_menu, turn_music, english_lang,
                                     german_lang, french_lang, settings_menu]
        self.translate_fields_settings = translate_fields_settings
        self.new_list_fields_menu_eng = ['Too long subject',
                                         'Your account has been created. Please check your email for the verification',
                                         'User with that name already exists', 'User name or password error',
                                         'Weft insertion test',
                                         'First issue',
                                         'being deleted', 'Switch to LTR', 'Go to Dashboard', 'Commentary',
                                         'Enter a password',
                                         'Enter name', 'Settings', 'First name', 'Password',
                                         'You have successfully logged in to your account', 'Password Field',
                                         'The password must contain numbers.', 'The password must contain letters.',
                                         'The password must contain letters.',
                                         'The password must contain special characters.']
        self.new_list_fields_setting_eng = ['Select language', 'Save Change', 'Return to the ', 'ON OFF', 'English',
                                            'German', 'French', 'Menu Options']
        self.new_list_fields_menu_de = ['Feld ist zu lang', 'Sie haben sich erfolgreich registriert',
                                        'Benutzer existiert bereits!', 'Ungültiger Benutzername oder Passwort',
                                        'Zur Passworteingabe gewechselt', 'Symbole eingeben', 'Löschen von Symbolen',
                                        'Namenseintrag umschalten', 'Zu den Einstellungen wechseln', 'Kommentare',
                                        'Geben Sie das Passwort ein', 'Name eingeben', 'Einstellungen', 'Vorname',
                                        'Passwort',
                                        'Sie haben sich erfolgreich angemeldet als', 'Leeres Passwort- oder Namensfeld',
                                        'Das Passwort muss Zahlen beinhalten.',
                                        'Das Passwort muss Großbuchstaben enthalten',
                                        'Das Passwort muss Kleinbuchstaben enthalten',
                                        'Das Passwort muss Sonderzeichen enthalten']
        self.new_list_fields_setting_de = ['Wählen Sie eine Sprache ', 'Änderung speichern', 'Zurück zum Menü',
                                           'Musik aktivieren deaktivieren',
                                           'Englisch', 'Deutsch', 'Französisch', '"Menüeinstellungen"']
        self.new_list_fields_menu_fr = ['Le champ est trop long', 'Vous vous êtes inscrit avec succès',
                                        'Un utilisateur avec ce nom existe déjà',
                                        "Nom d'utilisateur ou mot de passe non valide",
                                        'Passé à la saisie du mot de passe', 'Saisie des symboles',
                                        'Suppression de symboles',
                                        'Basculer la saisie du nom', 'Passer aux paramètres', 'Commentaires',
                                        'Saisir le mot de passe', 'Saisissez le nom', 'Paramètres', 'Prénom',
                                        'Mot de passe',
                                        'Vous vous êtes connecté avec succès en tant que',
                                        'Mot de passe ou champ de nom vide',
                                        'Le mot de passe doit contenir des chiffres',
                                        'Le mot de passe doit contenir des lettres majuscules',
                                        'Le mot de passe doit contenir des lettres minuscules',
                                        'Le mot de passe doit contenir des caractères spéciaux']

        self.new_list_fields_setting_fr = ['Sélectionnez une langue.', 'Enregistrer la modification', 'Retour au menu',
                                           'Activer Désactiver la musique', 'ANGLAIS', 'Allemand', 'Français',
                                           'Paramètres du menu']

    def translate(self, to_lang):
        if to_lang == 'en':
            self.translate_fields_settings = self.new_list_fields_setting_eng
            self.list_fields_menu = self.new_list_fields_menu_eng
            print(len(self.list_fields_menu))
        elif to_lang == 'fr':
            self.translate_fields_settings = self.new_list_fields_setting_fr
            self.list_fields_menu = self.new_list_fields_menu_fr
        elif to_lang == 'de':
            self.translate_fields_settings = self.new_list_fields_setting_de
            self.list_fields_menu = self.new_list_fields_menu_de

    def draw_buttons(self, screen):
        button_choice_language = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150, 250, 60,
                                        self.translate_fields_settings[0],
                                        'images/button_image.png')
        button_choice_language.draw(screen)
        button_back_to_menu = Button(10, 10, 250, 60, self.translate_fields_settings[2],
                                     'images/button_image.png')
        button_back_to_menu.draw(screen)
        button_music = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 280, 250, 60, self.translate_fields_settings[3],
                              'images/button_image.png')
        button_music.draw(screen)
        return [button_choice_language, '', button_back_to_menu, button_music]

    def draw_language_menu(self, screen, buttons):
        margin = buttons[0].rect.width
        button_eng = Button(SCREEN_WIDTH // 2 + margin, 25, 120, 45, self.translate_fields_settings[4],
                            'images/eng.jpg')
        button_eng.draw(screen, font=FONT_24_CLASSIC, color_font=BLUE)
        button_german = Button(SCREEN_WIDTH // 2 + margin,
                               SCREEN_HEIGHT // 2 - 225, 120, 45,
                               self.translate_fields_settings[5],
                               'images/ger.jpg')
        button_german.draw(screen, font=FONT_24_CLASSIC, color_font=BLUE)
        button_fr = Button(SCREEN_WIDTH // 2 + 45, 120, 120, 45, self.translate_fields_settings[6], 'images/fr.png')
        button_fr.draw(screen, font=FONT_24_CLASSIC, color_font=BLUE)
        return [button_eng, button_german, button_fr]

    def field_to_menu(self):
        return self.list_fields_menu

    def music_turn(self):
        self.turning = False

    def run(self, fields=False):
        self.list_fields_menu = self.list_fields_menu if not fields else fields
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(self.translate_fields_settings[7])
        running = True
        drawing_language_menu = False
        clock = pygame.time.Clock()
        while running:
            clock.tick(FPS)
            pygame.display.set_caption(self.translate_fields_settings[7])
            screen.fill(DARK_GREEN)
            if self.alpha > 0:
                self.alpha = screensaver_before_work(screen, self.alpha, 5)
            text = FONT_38.render(self.translate_fields_settings[7], True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 25))
            buttons_settings = self.draw_buttons(screen)
            if drawing_language_menu is True:
                self.draw_language_menu(screen, buttons_settings)
            for event in pygame.event.get():
                if drawing_language_menu is True:
                    buttons_lang = self.draw_language_menu(screen, buttons_settings)
                    if buttons_lang[0].check_click(pygame.mouse.get_pos()):
                        self.translate('en')
                    elif buttons_lang[1].check_click(pygame.mouse.get_pos()):
                        self.translate('de')
                    elif buttons_lang[2].check_click(pygame.mouse.get_pos()):
                        self.translate('fr')
                if event.type == pygame.QUIT:
                    self.entry.turning = self.turning
                    self.entry.run(self.list_fields_menu)
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if buttons_settings[0].check_click(pygame.mouse.get_pos()) is True:
                        self.draw_language_menu(screen, buttons_settings)
                        drawing_language_menu = True
                    elif buttons_settings[2].check_click(pygame.mouse.get_pos()):
                        self.entry.turning = self.turning
                        self.entry.run(self.list_fields_menu)
                        running = False
                    elif buttons_settings[3].check_click(pygame.mouse.get_pos()):
                        self.turning = True
            pygame.display.update()
