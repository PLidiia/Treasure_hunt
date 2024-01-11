import random

from Constants import *
from Tile import StaticTile, Boxes, Coin, Enemy_Only_X, Tile, Enemy_Fighting
from User import Player
from csv_work import import_csv_layout, import_cutting_tiles
from Camera import chase_about_camera

class Level:
    def __init__(self, level_data):
        self.count_world_shift = -5
        self.world_shift = 0
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')
        boxes_with_treasures = import_csv_layout(level_data['boxes'])
        self.boxes_sprites = self.create_tile_group(boxes_with_treasures, 'boxes')
        coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_layout, 'coins')
        enemies_layout = import_csv_layout(level_data['enemies'])
        self.enemies_sprites = self.create_tile_group(enemies_layout, 'enemies')
        const_blocs_layout = import_csv_layout(level_data['const'])
        self.const_blocs_sprites = self.create_tile_group(const_blocs_layout, 'const')
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        enemies_coords_sprites = []
        for sprite in self.enemies_sprites:
            x = sprite.rect.x
            y = sprite.rect.y
            enemies_coords_sprites.append((x, y))
        self.enemies_fighters_sprites = self.create_without_tile_group(enemies_coords_sprites)
        self.start_boxes_coords = []
        self.image_background = pygame.image.load("images/terrain/background.jpg")
        self.special_flag = 'Treasure'


    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val == '0':
                    sprite = Player((x, y))
                    self.player.add(sprite)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if type == 'terrain':
                        terrain_tile_list = import_cutting_tiles('images/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(TILE_SIZE, x, y, tile_surface)

                    if type == 'grass':
                        grass_tile_list = import_cutting_tiles('images/terrain/grass.png')
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(TILE_SIZE, x, y, tile_surface)

                    if type == 'boxes':
                        # тип, который не нужно разрезать так как это не клетка, а просто пиксельное изображение
                        sprite = Boxes(TILE_SIZE, x, y)

                    if type == 'coins':
                        sprite = Coin(TILE_SIZE, x, y, 'images/terrain/coins_frames')

                    if type == 'enemies':
                        sprite = Enemy_Only_X(TILE_SIZE, x, y, 2)

                    if type == 'const':
                        sprite = Tile(TILE_SIZE, x, y)
                    sprite_group.add(sprite)

        return sprite_group

    def create_without_tile_group(self, coords):
        enemies_fighters_sprites = pygame.sprite.Group()
        count_enemies_fighters = 2
        for sprite_coord in coords:
            if count_enemies_fighters > 0:
                x, y = sprite_coord
                sprite = Enemy_Fighting(TILE_SIZE, x, y)
                enemies_fighters_sprites.add(sprite)
                count_enemies_fighters -= 1
        return enemies_fighters_sprites

    def enemy_collision_with_blocks(self, group_sprites):
        for enemy_sprite in group_sprites.sprites():
            # если враги добежали до ограничавающих блоков констант на каждом куске treasure (земли) они расположены
            if pygame.sprite.spritecollide(enemy_sprite, self.const_blocs_sprites, False):
                enemy_sprite.reverse()

    def work_with_coords_sprites_boxes(self):
        boxes_coords = []
        for sprite in self.boxes_sprites:
            x = sprite.rect.x
            y = sprite.rect.y
            boxes_coords.append([x, y, 0])
        return boxes_coords

    def record_secret_box(self):
        special_num = random.randint(0, 9)
        for box_count in range(0, len(self.start_boxes_coords) - 1):
            if box_count == special_num:
                self.start_boxes_coords[box_count][2] = self.special_flag

    def make_list_x_coord_boxes(self):
        x_coords_boxes = []
        for box_info in self.start_boxes_coords:
            x = box_info[0]
            x_coords_boxes.append(x)
            x_coords_boxes.append(x + 10)
            x_coords_boxes.append(x - 10)
        return x_coords_boxes

    def check_box_about_treasure(self):
        for box_count in range(0, len(self.start_boxes_coords) - 1):
            if self.start_boxes_coords[box_count][2] == self.special_flag:
                print('УРААААААА')

    def run(self):
        running = True
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Карта 1')
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.blit(self.image_background, (0, 0))
            clock.tick(FPS)
            if len(self.start_boxes_coords) == 0:
                start_boxes_coords = self.work_with_coords_sprites_boxes()
                self.start_boxes_coords = start_boxes_coords
                self.record_secret_box()
                self.start_boxes_coords = start_boxes_coords
                x_coords = self.make_list_x_coord_boxes()
                for box_count in range(0, len(self.start_boxes_coords) - 1):
                    if self.start_boxes_coords[box_count][2] == self.special_flag:
                        print(self.start_boxes_coords[box_count])
                        print('YES')
            self.terrain_sprites.update(self.world_shift)
            self.terrain_sprites.draw(screen)

            self.player.update()
            self.world_shift = chase_about_camera(self.player, self.player.sprite.direction_moving)
            self.player.draw(screen)
            if self.player.sprite.search_box:
                if self.player.sprite.rect.x in x_coords:
                    self.check_box_about_treasure()



            self.grass_sprites.update(self.world_shift)
            self.grass_sprites.draw(screen)

            self.boxes_sprites.update(self.world_shift)
            self.boxes_sprites.draw(screen)

            self.coins_sprites.update(self.world_shift)
            self.coins_sprites.draw(screen)

            self.const_blocs_sprites.update(self.world_shift)
            self.enemies_sprites.update(self.world_shift)
            self.enemies_fighters_sprites.update(self.world_shift)
            self.enemy_collision_with_blocks(self.enemies_sprites)
            self.enemy_collision_with_blocks(self.enemies_fighters_sprites)
            self.enemies_sprites.draw(screen)
            self.enemies_fighters_sprites.draw(screen)

            pygame.display.update()
