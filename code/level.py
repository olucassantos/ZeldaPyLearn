from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from weapon import Weapon
from ui import UI

class Level:
    def __init__(self):
        # get the display surface
        # self.display_surface = pygame.display.get_surface() # Pega todas as surfaces do código

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map/map_Grass.csv'),
            'object': import_csv_layout('map/map_LargeObjects.csv'),
        }

        graphics = {
            'grass': import_folder('graphics/Grass'),
            'objects': import_folder('graphics/Objects'),
        }

        # Percorre as linhas do mapa
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                # Percorre as colunas do mapa
                for col_index, col in enumerate(row):
                    # Define a posição do tile na tela
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        elif style == 'grass':
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', choice(graphics['grass']))
                        elif style == 'object':
                            object_surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', object_surf)

        self.player = Player(
            (2000, 1430), 
            [self.visible_sprites], 
            self.obstacle_sprites, 
            self.create_attack, 
            self.destroy_attack,
            self.create_magic
        )

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()

        self.current_attack = None

    def create_magic(self, style, strength, cost):
        print(style, strength, cost)

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

    def custom_draw(self, player):

        # Pegando o offset do player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # Desenhando os sprites e aplicando o offset
        # for sprite in self.sprites():
        # Ordena os sprites pelo centro vertical deles (do menor para o maior) usando uma função lambda (função anônima)
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)