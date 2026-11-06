import pygame
from songs import *

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.mixer.pre_init()
pygame.mixer.init()

class Game:

    def __init__(self):
        self.clock = pygame.time.Clock()


    def run(self):
        song = Song()
        song.play()



if __name__ == "__main__":
    game = Game()
    game.run()