from settings import *

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.image = pygame.image.load(join('Vampire survivor','images','player','down','0.png')).convert_alpha()
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-60, -90)

        # movement
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.player_speed = 500

    def load_images(self):
        self.frames = {
            'up': [],
            'down': [],
            'left': [],
            'right': []
        }

        for state in self.frames.keys():
            for foldder_path, sub_folder, file_names in walk(join('Vampire survivor','images','player')):
                if file_names:
                    for file_name in file_names:
                        full_path = join(foldder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha
    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.player_speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.player_speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right

                if direction == 'vertical':
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom

    def update(self, dt):
        self.input()
        self.move(dt)