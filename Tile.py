import pygame
from csv_work import work_with_many_nestings

class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        pygame.sprite.Sprite.__init__(self)
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
        self.factor_for_moving = 0.15
        self.frames_sprite = work_with_many_nestings(path)
        self.default_index_frame = 0
        self.index_frame = 0
        self.cur_image_frame_sprite_ = self.frames_sprite[self.index_frame]

    def moving_frames_sprite(self):
        self.index_frame += self.factor_for_moving
        if self.index_frame < len(self.frames_sprite):
            self.cur_image_frame_sprite_ = self.frames_sprite[int(self.index_frame)]
        else:
            # дошли до конца, значит начинаем сначала менять кадры изображения данного спрайта
            self.index_frame = self.default_index_frame

    def update(self, shift):
        self.moving_frames_sprite()
        self.rect.x += shift
