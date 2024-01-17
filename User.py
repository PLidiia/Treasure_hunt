from Constants import *
from csv_work import work_with_many_nestings

all_sprites = pygame.sprite.Group()


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
        super().__init__(all_sprites)
        self.x = pos[0]
        self.y = pos[1]
        self.animations = different_animations()
        self.search_box = False
        self.index_frame = 0
        self.image = pygame.Surface((32, 64))
        self.rect = self.image.get_rect(bottomleft=(self.x, self.y + 190))
        self.image = self.animations['walk'][self.index_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.stamina = 1
        self.jump = False
        self.air = False
        self.shift = 1
        self.move_right = None
        self.move_left = None
        self.speed_jump = 2
        self.vel_y = 0
        self.gravity = 1
        self.direction_moving = pygame.math.Vector2(0, 0)

    def keyboard_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction_moving.x = 1
            self.move_right = True
        elif keys[pygame.K_LEFT]:
            self.direction_moving.x = -1
            self.move_left = True
        elif keys[pygame.K_a]:
            self.search_box = True
        else:
            self.direction_moving.x = 0
        if keys[pygame.K_SPACE]:
            self.fly()
        elif keys[pygame.K_DOWN]:
            self.fall()

    def fly(self):
        for n in range(4):
            self.rect.y -= 1

    def fall(self):
        for n in range(4):
            self.rect.y += 1

    def moving(self):
        types_of_move = self.animations['walk']
        self.index_frame += 0.15
        if self.index_frame >= len(types_of_move):
            self.index_frame = 0
            self.image = types_of_move[int(self.index_frame)]
        else:
            self.image = types_of_move[int(self.index_frame)]

    def reverse_image(self):
        if self.direction_moving.x == -1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.keyboard_input()
        if self.direction_moving.x:
            self.moving()
            self.reverse_image()
