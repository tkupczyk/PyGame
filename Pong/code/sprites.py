from settings import *
from random import choice, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)     
        self.image = pygame.Surface(SIZE['paddle'])
        self.image.fill(COLORS['paddle'])
        self.rect = self.image.get_frect(center=POS['player'])
        self.old_rect = self.rect.copy()
        self.player_speed = SPEED['player']
        self.direction = pygame.Vector2()

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.y = int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])

    def move(self, dt):
        if self.rect.top <= 0 and self.direction.y < 0:
            self.direction.y = 0
        if self.rect.bottom >= WINDOW_HEIGHT and self.direction.y > 0:
            self.direction.y = 0
        self.rect.y += self.direction.y * self.player_speed * dt

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)

class Ball(pygame.sprite.Sprite):
    def __init__(self, group, paddle_sprites):
        super().__init__(group)  

        self.paddle = paddle_sprites

        # IMAGE AND RECT 
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        pygame.draw.circle(self.image, COLORS['ball'], (SIZE['ball'][0] // 2, SIZE['ball'][1] // 2), SIZE['ball'][0] // 2)
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 ))
        self.old_rect = self.rect.copy()

        # MOVEMENT
        self.ball_speed = SPEED['ball']
        self.direction = pygame.Vector2(choice((1, -1)), uniform(0.7, 0.8) * choice((1, -1)))

    def move(self, dt):
        self.direction.x *= -1 if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH else 1
        self.rect.x += self.direction.x * self.ball_speed * dt
        self.collision('horizontal')
        self.direction.y *= -1 if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT else 1
        self.rect.y += self.direction.y * self.ball_speed * dt
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.paddle:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.rect.right > sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1
                    if self.rect.left < sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1
                else:
                    if self.rect.bottom > sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    if self.rect.top < sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1

                    

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.move(dt)