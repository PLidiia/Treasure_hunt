from Constants import *


def screensaver_before_work(screen, alpha):
    """
    Отрисовывает заставку, которая с каждым clock.tick(FPS) будет проявляться, благодаря этому
    создаётся эффект загрузки
    :param screen:
    :return:
    """
    surface_blur = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    surface_blur.fill((0, 0, 0, alpha))
    screen.blit(surface_blur, (0, 0))
    alpha -= 10
    return alpha
