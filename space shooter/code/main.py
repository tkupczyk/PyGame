import pygame
from os.path import join
import random

PLAYER_SPEED = 300
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
running = True

class Player(pygame.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('space shooter', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH /2, WINDOW_HEIGHT /2))
        self.direction = pygame.Vector2()

        # cooldown
        self.can_fire = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_fire:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_fire = True

    def update(self, dt):
        global PLAYER_SPEED
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * PLAYER_SPEED * dt

        recent_keys = pygame.key.get_just_pressed()

        if recent_keys[pygame.K_SPACE] and self.can_fire:
            Laser(laser_surface, self.rect.midtop, all_sprites)
            self.can_fire = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

class Stars(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, goups):
        super().__init__(goups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(400, 500)
        
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.creation_time >= self.lifetime:
            self.kill()

# general setup

pygame.init()
screen_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

# import

laser_surface = pygame.image.load(join('space shooter', 'images', 'laser.png')).convert_alpha()
meteor_surface = pygame.image.load(join('space shooter', 'images', 'meteor.png')).convert_alpha()
star_surf = pygame.image.load(join('space shooter', 'images', 'star.png')).convert_alpha()

# Sprites
all_sprites = pygame.sprite.Group()
for _ in range(20):
    star = Stars(all_sprites, star_surf)
player = Player(all_sprites)

# custom events - > meteor timer
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 400)



while running:
    dt = clock.tick() /1000  # delta time in seconds.

    
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor(meteor_surface, (random.randint(0, WINDOW_WIDTH), -100), all_sprites)

    all_sprites.update(dt)

    #draw the game
    screen_surface.fill("darkgrey")


    all_sprites.draw(screen_surface)

    pygame.display.update()


pygame.quit()