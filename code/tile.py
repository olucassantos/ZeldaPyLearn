import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        
        # A hitbox é um retângulo que fica dentro do sprite com tamanho menor que o sprite
        self.hitbox = self.rect.inflate(0, -10)