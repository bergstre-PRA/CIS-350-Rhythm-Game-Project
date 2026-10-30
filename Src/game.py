import pygame


class Game:

    def __init__(self):
        self.clock = pygame.time.Clock()


    def run(self):
        while True:
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()