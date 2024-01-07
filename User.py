import pygame

from csv_work import work_with_many_nestings


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.animations = self.different_animations()
        print(self.animations)
        self.index_frame = 0
        self.image = self.animations['walk'][self.index_frame]
        self.rect = self.image.get_rect(bottomleft=pos)

    def different_animations(self):
        animations = {
            'walk': [],
            'jump': []
        }
        for animation in animations.keys():
            path_to_image = 'images/terrain/player' + '/' + str(animation)
            animations[animation] = work_with_many_nestings(path_to_image)
        return animations

    def moving(self):
        types_of_move = self.animations['walk']
        self.index_frame += 0.15
        if self.index_frame >= len(types_of_move):
            self.index_frame = 0
            self.image = types_of_move[int(self.index_frame)]
        else:
            self.image = types_of_move[int(self.index_frame)]

    def update(self):
        self.moving()
