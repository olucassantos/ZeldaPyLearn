import pygame
from settings import *
from support import import_folder
from debug import debug

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # A hitbox é um retângulo que fica dentro do sprite com tamanho menor que o sprite
        self.hitbox = self.rect.inflate(0, -26)

        # Graphics stuff
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction = pygame.math.Vector2() # Retorna um vetor com a posição do player
        self.speed = 5
        self.attacking = False
        self.attack_colldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = 'graphics/player/'

        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'right_idle': [],
            'left_idle': [],
            'up_idle': [],
            'down_idle': [],
            'up_attack': [],
            'down_attack': [],
            'left_attack': [],
            'right_attack': []
        }

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(character_path + animation)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # Define a direção do player de acordo com as teclas pressionadas
            if keys[pygame.K_LEFT]: 
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]: 
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            if keys[pygame.K_UP]: 
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]: 
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            # Attack
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print('Attack')

            # Magic Input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print('Magic')

    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    # overwriting the idle status
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

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

    def animate(self):
        animation = self.animations[self.status]

        # loop the animation
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # update the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)


    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_colldown:
                self.attacking = False

    def update(self):
        self.input()
        self.move(self.speed)
        self.get_status()
        self.animate()
        self.cooldowns()