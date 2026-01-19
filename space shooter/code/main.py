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

    
    def update(self, dt):
        global PLAYER_SPEED
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * PLAYER_SPEED * dt

        recent_keys = pygame.key.get_just_pressed()

        if recent_keys[pygame.K_SPACE]:
            print("fire")

class Stars(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)))

    
# general setup

pygame.init()
screen_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game")


# surface setup

surface = pygame.Surface((100,200))
surface.fill("orange")

#player direction


# import image

clock = pygame.time.Clock()

laser_surface = pygame.image.load(join('space shooter', 'images', 'laser.png')).convert_alpha()
laser_rect = laser_surface.get_frect(bottomleft = (0 + 20, WINDOW_HEIGHT - 20))

meteor_surface = pygame.image.load(join('space shooter', 'images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surface.get_frect(center = (WINDOW_WIDTH /2, WINDOW_HEIGHT /2))

all_sprites = pygame.sprite.Group()
star_surf = pygame.image.load(join('space shooter', 'images', 'star.png')).convert_alpha()
for _ in range(20):
    star = Stars(all_sprites, star_surf)

player = Player(all_sprites)


while running:
    dt = clock.tick() /1000  # delta time in seconds.

    
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update(dt)

    #draw the game
    screen_surface.fill("darkgrey")


    all_sprites.draw(screen_surface)

    pygame.display.update()


pygame.quit()