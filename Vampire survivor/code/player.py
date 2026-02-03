from settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(join('Vampire survivor','images','player','down','0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)

        # movement
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.player_speed = 500

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.rect.center += self.direction * self.player_speed * dt

    def update(self, dt):
        self.input()
        self.move(dt)