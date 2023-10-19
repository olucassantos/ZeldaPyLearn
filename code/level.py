import pygame
from settings import *
from tile import Tile
from player import Player

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface() # Pega todas as surfaces do código

        # Sprite group setup
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()

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
                    Tile((x, y), [self.visible_sprites])

                elif col == 'p':
                    Player((x, y), [self.visible_sprites])

    def run(self):
        # update and draw the game
        self.visible_sprites.draw(self.display_surface)