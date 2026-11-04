import pygame
import sys
from menu import *

class Game:
    def __init__(self, width=1200, height=900):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Rhythm Game")

        self.clock = pygame.time.Clock()
        self.running = True

        # Instantiate the Menu class
        self.menu = Menu()

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

            # Delegate event handling to the Menu class
            if self.menu.handle_event(event):
                self.running = False

    def draw(self):
        # Delegate drawing to the Menu class
        self.menu.draw(self.screen, self.width, self.height)
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



"""import pygame
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
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        running = False



if __name__ == "__main__":
    game = Game()
    game.run()"""