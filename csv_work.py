import csv
import pygame
from Constants import *
import os

def import_csv_layout(path):
    terrain_map = []
    with open(path) as layout_csv_file:
        level = csv.reader(layout_csv_file, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map


def import_cutting_tiles(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILE_SIZE)
    tile_num_y = int(surface.get_size()[1] / TILE_SIZE)
    cut_tiles = []
    for row in range(tile_num_x):
        for col in range(tile_num_y):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            new_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), flags=pygame.SRCALPHA)
            new_surface.blit(surface, (0, 0), pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            cut_tiles.append(new_surface)
    return cut_tiles


def work_with_many_nestings(path):
    surface_images = []
    for nesting_count_1, nesting_count_2, images in os.walk(path):
        for image in images:
            to_images_path = path + '/' + image
            surface_image = pygame.image.load(to_images_path).convert_alpha()
            surface_images.append(surface_image)
    return surface_images




