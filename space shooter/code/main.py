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
            Laser(laser_surface, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_fire = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

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
        self.rotation = 0
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = pos)
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(400, 500)
        self.rotation_speed = random.randint(-100, 100)
        
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.creation_time >= self.lifetime:
            self.kill()
        
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index] 
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index += 50 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)] 
            explosion_sound.play()
        else:
            self.kill()

def collisions():
    global running

    collisions_sprites = pygame.sprite.spritecollide(player, meteor_sprites, False, pygame.sprite.collide_mask)
    if collisions_sprites:
        running = False

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)

def display_score():
    current_time = pygame.time.get_ticks() // 1000
    text_surf = font.render(str(current_time), True, (240,240,240))
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH /2, WINDOW_HEIGHT - 50))
    screen_surface.blit(text_surf, text_rect)
    pygame.draw.rect(screen_surface, (240, 240, 240), text_rect.inflate(30, 20).move(0, -3), 5, 10)


# general setup

pygame.init()
screen_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

# import

laser_surface = pygame.image.load(join('space shooter', 'images', 'laser.png')).convert_alpha()
meteor_surface = pygame.image.load(join('space shooter', 'images', 'meteor.png')).convert_alpha()
star_surf = pygame.image.load(join('space shooter', 'images', 'star.png')).convert_alpha()
font = pygame.font.Font(join('space shooter','images', 'Oxanium-Bold.ttf'), 20)
explosion_frames = [pygame.image.load(join('space shooter','images','explosion',f'{i}.png')).convert_alpha() for i in range(21)]
laser_sound = pygame.mixer.Sound(join('space shooter','audio','laser.wav'))
laser_sound.set_volume(0.3)
explosion_sound = pygame.mixer.Sound(join('space shooter','audio','explosion.wav'))
explosion_sound.set_volume(0.1)
game_music = pygame.mixer.Sound(join('space shooter','audio','game_music.wav'))
game_music.set_volume(0.05)
game_music.play(loops= -1)


# Sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
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
            Meteor(meteor_surface, (random.randint(0, WINDOW_WIDTH), -100), (all_sprites, meteor_sprites))

    all_sprites.update(dt)

    collisions()
    #draw the game
    screen_surface.fill('#3a2e3f')
    display_score()
    all_sprites.draw(screen_surface)

    pygame.display.update()


pygame.quit()