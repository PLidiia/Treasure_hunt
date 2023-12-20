import pygame.mixer_music

from Constants import *


class Enter:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Login/registration')
        self.icon = pygame.image.load(os.path.join('images', 'top_user.png'))
        pygame.display.set_icon(self.icon)
        self.logo_img = pygame.image.load(os.path.join('images', 'logo.png'))
        self.block_ground = pygame.image.load(os.path.join('images', 'grass.png'))
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load(os.path.join('music', 'first.mp3'))

    def draw_text(self, text, x, y, font=FONT_38, color=BLACK):
        text_to_render = pygame.font.Font.render(
            font,
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
        self.draw_text("Введите своё имя", 25, self.logo_img.get_height() + text_object_1.get_height(),
                       color=DARK_RED)
        text_object_2 = self.draw_text("Введите своё имя", 25,
                                       self.logo_img.get_height() + text_object_1.get_height(), color=DARK_RED)
        self.draw_text("Введите свою почту", 25, self.logo_img.get_height() +
                       text_object_2.get_height() + text_object_1.get_height() + 20, color=DARK_RED)
        self.name_btn = pygame.draw.rect(self.screen, BLUE, [400 + text_object_2.get_width(),
                                                             self.logo_img.get_height() + text_object_1.get_height(),
                                                             220, 40])
        self.draw_text('Сохранить имя', 400 + text_object_2.get_width(), self.logo_img.get_height() +
                       text_object_1.get_height(), font=FONT_24)
        self.mail_btn = pygame.draw.rect(self.screen, BLUE, [400 + text_object_2.get_width(),
                                                             self.logo_img.get_height() +
                                                             text_object_2.get_height() +
                                                             text_object_1.get_height() + 20,
                                                             220, 40])
        self.draw_text('Сохранить почту', 400 + text_object_2.get_width(), self.logo_img.get_height() +
                       text_object_1.get_height() + text_object_2.get_height() + 20, font=FONT_24)
        self.input_name = pygame.draw.rect(self.screen, PINK, [400 - self.name_btn.width - 10 +
                                                               text_object_2.get_width(),
                                                               self.logo_img.get_height() + text_object_1.get_height(),
                                                               220, 40])

        self.input_mail = pygame.draw.rect(self.screen, PINK, [400 - self.mail_btn.width - 10 +
                                                               text_object_2.get_width(),
                                                               self.logo_img.get_height() +
                                                               text_object_2.get_height() +
                                                               text_object_1.get_height() + 20,
                                                               220, 40])

    def run(self):
        pygame.init()
        pygame.mixer_music.play()
        run = True
        active_to_write_name = False
        alpha = 255
        user_name_text = ''
        while run:
            self.clock.tick_busy_loop(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        if self.name_btn.collidepoint(pygame.mouse.get_pos()):
                            pass
                if event.type == pygame.MOUSEMOTION:
                    if self.input_name.collidepoint(pygame.mouse.get_pos()):
                        active_to_write_name = True
                        print('active_to_write_name')
                if event.type == pygame.KEYDOWN:
                    if active_to_write_name:
                        if event.key == pygame.K_BACKSPACE:
                            user_name_text += user_name_text[:-1]
                            print('pygame.K_BACKSPACE')
                        else:
                            user_name_text += event.unicode
                            self.text_surface = self.draw_text(user_name_text, self.input_name.x, self.input_name.y, font=FONT_12)
                            print('event.unicode')

            self.draw_items()
            if alpha > 0:
                s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                s.fill((0, 0, 0, alpha))
                self.screen.blit(s, (0, 0))
                alpha -= 2
            self.screen.blit(self.text_surface, self.input_name.x, self.input_name.y)
            self.clock.tick(60)
            pygame.display.update()
