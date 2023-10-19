import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # A hitbox é um retângulo que fica dentro do sprite com tamanho menor que o sprite
        self.hitbox = self.rect.inflate(0, -26)

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

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                # Verifica se o player está colidindo com algum obstáculo
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # Movendo para a direita
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0: # Movendo para a esquerda
                        self.hitbox.left = sprite.hitbox.right

        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                # Verifica se o player está colidindo com algum obstáculo
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # Movendo para baixo
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0: # Movendo para cima
                        self.hitbox.top = sprite.hitbox.bottom

    def update(self):
        self.input()
        self.move(self.speed)