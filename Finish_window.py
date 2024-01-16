from Constants import *


class Finish:
    def __init__(self, scores, name, result_of_game):
        self.scores = scores
        self.name = name
        self.result_of_game = result_of_game

    def draw_items(self, screen):
        if self.result_of_game != 'Вы проиграли':
            text = FONT_24.render(self.name, True, WHITE)
            screen.blit(text, (10, 10))
            text = FONT_24.render(str(self.scores), True, WHITE)
            screen.blit(text, (100, 10))
        text = FONT_56.render(self.result_of_game, True, WHITE)
        screen.blit(text, (100, 50))

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Финальное окно')
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(FPS)
            screen.fill(DARK_GREEN)
            self.draw_items(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()
