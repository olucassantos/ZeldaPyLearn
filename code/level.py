from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from settings import *
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self):
        # get the display surface
        # self.display_surface = pygame.display.get_surface() # Pega todas as surfaces do código

        # Sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

    def create_map(self):
        # Percorre as linhas do mapa
        for row_index, row in enumerate(WORLD_MAP):
            # Percorre as colunas do mapa
            for col_index, col in enumerate(row):
                # Define a posição do tile na tela
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                # Cria o tile
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])

                elif col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):

        # Pegando o offset do player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Desenhando os sprites e aplicando o offset
        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)