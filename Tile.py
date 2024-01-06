from Constants import *
from csv_work import work_with_many_nestings


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        # двигаемся только по горизонтали, по вертикали координата с течением времени не меняется
        self.rect.x += shift


class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class Boxes(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load('images/terrain/boxes.png').convert_alpha())
        margin = y + size
        # для корректного отображение на карте, левая точка низа четырёхугольника располагается на координате x
        # данного изображение ("клетки") на карте и тк ось ординат направлена вниз в pygame, то чтобы сундук с
        # сокравищами стоял на земле, то нужно координату y прибавить размер, условно сундук будет на
        # самой крайней точки
        self.rect = self.image.get_rect(bottomleft=(x, margin))


class Tile_With_Animation(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames_sprite = work_with_many_nestings(path)
        self.index_frame = 0
        if self.index_frame < len(self.frames_sprite) > 0:
            self.cur_image_frame_sprite = self.frames_sprite[self.index_frame]

    def moving_frames_sprite(self):
        self.index_frame += 0.15
        if len(self.frames_sprite) > 0:
            if self.index_frame >= len(self.frames_sprite):
                self.index_frame = 0
                self.image = self.frames_sprite[int(self.index_frame)]
            else:
                self.image = self.frames_sprite[int(self.index_frame)]

    def update(self, shift):
        self.moving_frames_sprite()
        self.rect.x += shift


class Coin(Tile_With_Animation):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y, path)
        mid_x = TILE_SIZE // 2 + int(size // 2) + x
        mid_y = TILE_SIZE // 2 + int(size // 2) + y
        self.rect = self.image.get_rect(bottomleft=(mid_x, mid_y))


class Enemy_Only_X(Tile_With_Animation):
    def __init__(self, size, x, y, speed):
        super().__init__(size, x, y, 'images/enemy/enemy_is_running')
        # size // 4 - необходимо для травы
        self.rect.y += (size - self.image.get_size()[1]) + size // 4
        self.speed = speed

    def is_moving(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            # отражаем изображение по горизонтали, по вертикали тоже самое
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.moving_frames_sprite()
        self.is_moving()
        self.reverse_image()


class Enemy_Fighting(Tile_With_Animation):
    def __init__(self, size, x, y, speed=2):
        super().__init__(size, x, y, 'images/enemy/enemy1_is_running/run')
        self.rect = self.image.get_rect(bottomleft=(x - self.rect.width, (y - self.rect.height) + 15))
        self.speed = speed
        self.index_frame_fighting = 0
        path_for_fighting_sprite = 'images/enemy/enemy1_is_running/fight'
        self.fighting_frames_sprite = work_with_many_nestings(path_for_fighting_sprite)
        self.cur_fighting_frame_sprite_ = self.fighting_frames_sprite[self.index_frame_fighting]

    def moving(self):
        self.rect.x += self.speed

    def is_fighting(self):
        self.index_frame_fighting += 0.5
        if self.index_frame_fighting >= len(self.fighting_frames_sprite):
            self.index_frame_fighting = 0
        self.image = self.fighting_frames_sprite[int(self.index_frame_fighting)]

    def reverse_image(self):
        if self.speed < 0:
            # отражаем изображение по горизонтали, по вертикали тоже самое
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.moving_frames_sprite()
        self.moving()
        self.reverse_image()