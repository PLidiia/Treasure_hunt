import pygame.mouse

from Constants import *
from button import Button


class Enter:
    def __init__(self):
        self.icon = pygame.image.load(os.path.join('images', 'top_user.png'))
        self.logo_img = pygame.image.load(os.path.join('images', 'logo.png'))
        self.block_ground = pygame.image.load(os.path.join('images', 'grass.png'))
        self.button_1 = ''

    def draw_items(self, screen):
        button_1 = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150, 250, 60, 'Сохранить данные',
                          'images/button_image.png', hover_image_path='images/button_image_is_hovered.png')
        self.button_1 = button_1
        button_1.draw(screen)

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.fill(DARK_GREEN)
        pygame.display.set_caption('Меню')
        pygame.display.set_icon(self.icon)
        pygame.mixer.music.load(os.path.join('music', 'first.mp3'))
        pygame.mixer_music.play()
        enter = Enter()
        alpha = 255
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.draw_items(screen)
            self.button_1.check_hover(pygame.mouse.get_pos())
            self.button_1.draw(screen)
            if alpha > 0:
                surface_blur = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                surface_blur.fill((0, 0, 0, alpha))
                screen.blit(surface_blur, (0, 0))
                alpha -= 2
            pygame.display.flip()
