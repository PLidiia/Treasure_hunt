import pygame

from csv_work import work_with_many_nestings


def different_animations():
    animations = {
        'walk': [],
        'jump': []
    }
    for animation in animations.keys():
        path_to_image = 'images/terrain/player' + '/' + str(animation)
        animations[animation] = work_with_many_nestings(path_to_image)
    return animations


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.x = pos[0]
        self.y = pos[1]
        self.animations = different_animations()
        self.search_box = False
        self.index_frame = 0
        self.image = pygame.Surface((32, 64))
        self.rect = self.image.get_rect(bottomleft=(self.x, self.y + 165))
        self.stamina = 6
        self.direction_moving = pygame.math.Vector2(0, 0)

    def keyboard_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction_moving.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction_moving.x = -1
        elif keys[pygame.K_a]:
            self.search_box = True

        else:
            self.direction_moving.x = 0

    def moving(self):
        types_of_move = self.animations['walk']
        self.index_frame += 0.15
        if self.index_frame >= len(types_of_move):
            self.index_frame = 0
            self.image = types_of_move[int(self.index_frame)]
        else:
            self.image = types_of_move[int(self.index_frame)]

    def update(self):
        self.keyboard_input()
        # обновляем положение фигуры, по тому на какие клавиши нажал пользователь
        self.rect.x += self.direction_moving.x * self.stamina
        self.moving()
