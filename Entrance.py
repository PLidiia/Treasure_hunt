import pygame.mouse

from Constants import *
from button import Button


class Enter:
    def __init__(self):
        self.icon = pygame.image.load(os.path.join('images', 'top_user.png'))
        self.logo_img = pygame.image.load(os.path.join('images', 'logo.png'))
        self.block_ground = pygame.image.load(os.path.join('images', 'grass.png'))

    def draw_items(self, screen):
        button_1 = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150, 250, 60, 'Начать вход',
                          'images/button_image.png', hover_image_path='images/button_image_is_hovered.png')
        self.button_1 = button_1
        button_1.draw(screen)
        return button_1

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.fill(DARK_GREEN)
        pygame.display.set_caption('Меню')
        pygame.display.set_icon(self.icon)
        pygame.mixer.music.load(os.path.join('music', 'first.mp3'))
        pygame.mixer.music.play()
        enter = Enter()
        alpha = 255
        input_text = ''
        inputting_data = False
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            screen.fill(DARK_GREEN)
            btn = self.draw_items(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif inputting_data and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        inputting_data = False
                        input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        pass
                    else:
                        input_text += event.unicode
                elif btn.check_click(pygame.mouse.get_pos()):
                    inputting_data = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_TAB]:
                input_text = True
            self.draw_items(screen)
            self.button_1.check_hover(pygame.mouse.get_pos())
            self.button_1.draw(screen)
            if alpha > 0:
                surface_blur = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                surface_blur.fill((0, 0, 0, alpha))
                screen.blit(surface_blur, (0, 0))
                alpha -= 4
            text = FONT_24.render(input_text, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 135))
            pygame.display.update()
