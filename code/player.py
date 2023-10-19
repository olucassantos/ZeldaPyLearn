import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2() # Retorna um vetor com a posição do player
        self.speed = 5

    def input(self):
        keys = pygame.key.get_pressed()

        # Define a direção do player de acordo com as teclas pressionadas
        if keys[pygame.K_LEFT]: self.direction.x = -1
        elif keys[pygame.K_RIGHT]: self.direction.x = 1
        else: self.direction.x = 0

        if keys[pygame.K_UP]: self.direction.y = -1
        elif keys[pygame.K_DOWN]: self.direction.y = 1
        else: self.direction.y = 0

    def move(self, speed):
        # Se o vetor direção não for nulo, normaliza ele (deixa ele com o tamanho 1)
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # O self.rect.center é uma tupla com a posição do player
        # O self.direction é um vetor2 com a direção do player
        # Quando multiplicamos um vetor2 por um número, ele multiplica cada componente do vetor por esse número
        self.rect.center += self.direction * speed

    def update(self):
        self.input()
        self.move(self.speed)