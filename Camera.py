from Constants import *


def chase_about_camera(player, direction_of_move):
    player = player.sprite
    coord_x_player = player.rect.centerx
    # если игрок не вышел за шестую часть ширины экрана и он направляется налево, то есть координата x уменьшается
    if coord_x_player < SCREEN_WIDTH / 4 and direction_of_move.x < 0:
        world_shift = 6
        player.stamina = 0
        return world_shift
    # если игрок вышел за шестую часть ширины экрана и он направляется направо, то есть координата x увеличивается
    elif coord_x_player > SCREEN_WIDTH - (SCREEN_WIDTH / 4) and direction_of_move.x > 0:
        world_shift = -6
        player.stamina = 0
        return world_shift
    else:
        world_shift = 0
        player.stamina = 6
        return world_shift
