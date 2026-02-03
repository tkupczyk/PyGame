from settings import *
from player import Player
from sprites import *

from random import randint

class Game:
    def __init__(self):
        # SetUp
        pygame.init()
        self.screen_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Survivor")
        self.clock = pygame.time.Clock()
        self.running = True

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # Sprites
        self.player = Player((400,300), self.all_sprites, self.collision_sprites)
        for i in range(6):
            x, y = randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
            width, height = randint(50,150), randint(50,150)
            CollisionSprite((x,y),(width,height), (self.all_sprites, self.collision_sprites))

    def run(self):
        while self.running:
            dt = self.clock.tick() /1000  # delta time in seconds.

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)

            # draw
            self.screen_surface.fill('black')
            self.all_sprites.draw(self.screen_surface)

            pygame.display.update()

        pygame.quit()

# SPRITES
game = Game()

if __name__ == '__main__':
    game.run()