from Constants import *
from Tile import Tile, StaticTile
from csv_work import import_csv_layout, import_cutting_tiles


class Level:
    def __init__(self, name_user, level_data):
        self.name_user = name_user
        self.level_data = level_data
        self.map_shift = 0
        terrain_layout = import_csv_layout(level_data)
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

    def create_tile_group(self, layout, type_layout):
        sprite_group_current_layout = pygame.sprite.Group()
        for index_row, row in enumerate(layout):
            for index_col, id_tile in enumerate(row):
                if id_tile != '0':
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    if type_layout == 'terrain' and id_tile != '' and id_tile:
                        terrain_tile_list = import_cutting_tiles('images/terrain/terrain_tiles.png')
                        if len(terrain_tile_list) - 1 >= int(id_tile):
                            tile_surface = terrain_tile_list[int(id_tile)]
                            sprite = StaticTile(TILE_SIZE, x, y, tile_surface)
                            sprite_group_current_layout.add(sprite)
        return sprite_group_current_layout

    def run(self):
        running = True
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Карта 1')
        clock = pygame.time.Clock()
        while running:
            screen.fill(DARK_GREEN)
            clock.tick(FPS)
            self.terrain_sprites.draw(screen)
            self.terrain_sprites.update(-4)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()
