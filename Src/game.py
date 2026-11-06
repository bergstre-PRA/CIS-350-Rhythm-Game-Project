import pygame
import sys
from menu import *
from songs import *

class Game:
    def __init__(self, width=1200, height=900):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Rhythm Game")

        self.clock = pygame.time.Clock()
        self.running = True

        # Initialized the Menu class
        self.menu = Menu(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.menu.currentState in (self.menu.SETTINGS, self.menu.PLAY_GAME):
                        self.menu.currentState = self.menu.MAIN_MENU
                    else:
                        self.running = False

            # Event handling to the Menu class
            if self.menu.handle_event(event):
                self.running = False

    def draw(self):
        # Delegate drawing to the Menu class
        self.menu.draw(self.width)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()