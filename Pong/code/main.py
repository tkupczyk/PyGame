from sprites import Player, Ball
from settings import * 

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.running = True

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        self.all_sprites = pygame.sprite.Group()
        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.ball = Ball(self.all_sprites, self.paddle_sprites)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000  # delta time in seconds.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.all_sprites.update(dt)
            self.screen.fill(COLORS['bg'])
            self.all_sprites.draw(self.screen)

            pygame.display.update()

        pygame.quit()

    def collision(self):
        if pygame.sprite.spritecollide(self.ball, self.paddle_sprites, False):
            self.ball.bounce()

game = Game()

if __name__ == '__main__':
    game.run()