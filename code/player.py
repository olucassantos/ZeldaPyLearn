import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2() # Retorna um vetor com a posição do player
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites

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
        # self.rect.center += self.direction * speed

        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                # Verifica se o player está colidindo com algum obstáculo
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: # Movendo para a direita
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0: # Movendo para a esquerda
                        self.rect.left = sprite.rect.right

        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                # Verifica se o player está colidindo com algum obstáculo
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: # Movendo para baixo
                        self.rect.bottom = sprite.rect.top
                    elif self.direction.y < 0: # Movendo para cima
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.input()
        self.move(self.speed)