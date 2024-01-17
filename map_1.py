import random
import sqlite3
import time

import pygame.image

from Camera import chase_about_camera
from Constants import *
from Finish_window import Finish
from Tile import StaticTile, Boxes, Coin, Enemy_Only_X, Tile, Enemy_Fighting
from User import Player
from csv_work import import_csv_layout, import_cutting_tiles


class Map:
    def __init__(self, level_data, name, turn, language):
        self.name = name
        self.count_world_shift = -5
        self.world_shift = 0
        self.turning = turn
        self.language = language
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
        self.current_x = None
        self.health_bar = pygame.image.load('images/health_bar.png')
        self.health_bar = pygame.transform.rotozoom(self.health_bar, 0, 0.5)
        self.health_bar_top_left = (145, 137)
        self.health_bar_width = 312
        self.health_bar_hight = 50
        self.max_health = 700
        self.cur_health = self.max_health
        self.one_shout_enemy = 4
        self.one_shout_enemy_fighter = 8
        self.con = sqlite3.connect('database/users.db')
        cur = self.con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS RESULT (
                    name TEXT,
                    coins TEXT,
                    time TEXT
                )""")
        for sprite in self.enemies_sprites:
            x = sprite.rect.x
            y = sprite.rect.y
            enemies_coords_sprites.append((x, y))
        self.enemies_fighters_sprites = self.create_without_tile_group(enemies_coords_sprites)
        self.start_boxes_coords = []
        self.image_background = pygame.image.load("images/terrain/background.jpg")
        self.special_flag = 'Treasure'
        self.count_scores = 0
        self.start_time = time.time()
        self.scores_field = 'Количество очков'
        self.map_1 = 'Карта 1'
        self.you_won = 'Вы выиграли'
        self.you_lost = 'Вы проиграли'
        self.final_window = 'Финальное окно'
        self.final_window_en = 'Final Window'
        self.final_window_de = 'Letztes Fenster'
        self.final_window_fr = 'Fenêtre finale'
        self.map_1_fields = [self.scores_field, self.map_1, self.you_won, self.you_lost, self.final_window]
        self.map_1_fields_en = ['Score amount', 'Map 1', 'You won', 'You lose!']
        self.map_1_fields_fr = ['Nombres de Points crédités', 'Carte 1.', 'Vous avez gagné !', 'Vous avez perdu']
        self.map_1_fields_de = ['Punktestand', 'Karte 1', 'Sie haben gewonnen', 'Sie haben verloren']
        if self.language == 'en':
            self.map_1_fields = self.map_1_fields_en
            self.final_window = self.final_window_en
        elif self.language == 'de':
            self.map_1_fields = self.map_1_fields_de
            self.final_window = self.final_window_de
        elif self.language == 'fr':
            self.map_1_fields = self.map_1_fields_fr
            self.final_window = self.final_window_fr
        self.is_start = False
        self.sound_result = False

    def make_health_bar(self, cur, const, screen):
        screen.blit(self.health_bar, (50, 100))
        cur_health_player = const / cur
        cur_width_bar = self.health_bar_width * cur_health_player
        bar_rect = pygame.Rect(self.health_bar_top_left, (cur_width_bar, self.health_bar_hight))
        pygame.draw.rect(screen, DARK_RED, bar_rect)
        return cur_width_bar

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val == '0':
                    sprite = Player((x, y - 25))
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
            x_coords_boxes.append(x + 5)
            x_coords_boxes.append(x - 5)
        return x_coords_boxes

    def check_box_about_treasure(self):
        if self.turning is True:
            pygame.mixer.music.load(os.path.join('music', 'check_box.mp3'))
            pygame.mixer.music.play()
        for box_count in range(0, len(self.start_boxes_coords) - 1):
            if self.start_boxes_coords[box_count][2] == self.special_flag:
                diff = time.time() - self.start_time
                cur = self.con.cursor()
                cur.execute("INSERT INTO RESULT (name, coins, time) VALUES (?, ?, ?)",
                            (self.name, self.count_scores, int(diff)))
                self.con.commit()
                if self.turning is True and self.sound_result is False:
                    pygame.mixer.music.load(os.path.join('music', 'you_win.mp3'))
                    pygame.mixer.music.play()
                    self.sound_result = True
                finish = Finish(self.count_scores, self.name, self.map_1_fields[2], )
                finish.run()

    def collision(self):
        player = self.player.sprite
        player.rect.x += player.direction_moving.x * player.stamina
        collidable_sprites = self.terrain_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction_moving.x < 0:
                    player.rect.left = sprite.rect.right
                elif player.direction_moving.x > 0:
                    player.rect.right = sprite.rect.left

    def collision_coin(self):
        player = self.player.sprite
        for sprite in self.coins_sprites.sprites():
            if player.rect.colliderect(sprite.rect):
                sprite.kill()
                if self.turning is True:
                    pygame.mixer.music.load(os.path.join('music', 'coin_update.mp3'))
                    pygame.mixer.music.play()
                self.count_scores += 1

    def vertical_collision(self):
        player = self.player.sprite
        if player.rect.y < 8:
            player.rect.y = 8
        elif player.rect.y > 500:
            player.rect.y = 500

    def horizontal_collision(self):
        player = self.player.sprite
        if player.rect.x < 8:
            player.rect.x = 8
        elif player.rect.x > 920:
            player.rect.x = 920

    def check_enemy_collision(self):
        player = self.player.sprite
        enemy_col = pygame.sprite.spritecollide(player, self.enemies_sprites, False)
        if enemy_col:
            for sprite in enemy_col:
                sprite_center = sprite.rect.centery
                sprite_top = sprite.rect.top
                player_bottom = player.rect.bottom
                if sprite_top < player_bottom < sprite_center and player.direction_moving.y > 0 or \
                        player.direction_moving.x > 0:
                    sprite.kill()
                    self.play_sound_death_enemy()
                else:
                    self.enemy_damage()

    def check_enemy_fighters_collision(self):
        player = self.player.sprite
        enemy_fighters_col = pygame.sprite.spritecollide(player, self.enemies_fighters_sprites, False)
        if enemy_fighters_col:
            for sprite in enemy_fighters_col:
                sprite_center = sprite.rect.centery
                sprite_top = sprite.rect.top
                player_bottom = player.rect.bottom
                if sprite_top < player_bottom < sprite_center and player.direction_moving.y > 0 or \
                        player.direction_moving.x > 0:
                    sprite.kill()
                    self.play_sound_death_enemy()
                else:
                    self.enemy_fighers_damage()

    def enemy_damage(self):
        self.cur_health -= self.one_shout_enemy

    def enemy_fighers_damage(self):
        self.cur_health -= self.one_shout_enemy_fighter

    def write_text(self, screen):
        text = FONT_24.render(str(self.count_scores), True, WHITE)
        screen.blit(text, (10, 10))
        text = FONT_24.render(self.scores_field, True, WHITE)
        screen.blit(text, (10, 40))

    def check_loss(self, len_bar):
        if len_bar <= 0:
            if self.turning is True:
                pygame.mixer.music.load(os.path.join('music', 'gameover.mp3'))
                pygame.mixer.music.play()
            finish = Finish(self.count_scores, self.name, self.map_1_fields[3], self.final_window)
            finish.run()
            return True

    def play_sound_death_enemy(self):
        if self.turning is True:
            pygame.mixer.music.load(os.path.join('music', 'death_enemy.mp3'))
            pygame.mixer.music.play()

    def run(self):
        self.start = time.time()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(self.map_1_fields[1])
        clock = pygame.time.Clock()
        running = True
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
            self.terrain_sprites.update(self.world_shift)
            self.terrain_sprites.draw(screen)
            self.player.update(self.terrain_sprites)
            self.world_shift = chase_about_camera(self.player, self.player.sprite.direction_moving)
            self.collision()
            self.vertical_collision()
            self.horizontal_collision()
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

            self.collision_coin()
            self.write_text(screen)

            self.const_blocs_sprites.update(self.world_shift)
            self.enemies_sprites.update(self.world_shift)
            self.enemies_fighters_sprites.update(self.world_shift)
            self.enemy_collision_with_blocks(self.enemies_sprites)
            self.enemy_collision_with_blocks(self.enemies_fighters_sprites)
            self.enemies_sprites.draw(screen)
            self.enemies_fighters_sprites.draw(screen)

            self.check_enemy_collision()
            cur_len_bar = self.make_health_bar(self.max_health, self.cur_health, screen)

            self.check_enemy_fighters_collision()
            cur_len_bar = self.make_health_bar(self.max_health, self.cur_health, screen)
            self.check_loss(cur_len_bar)
            if self.check_loss(cur_len_bar):
                running = False
            pygame.display.update()
