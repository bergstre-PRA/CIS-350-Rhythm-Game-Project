"""Main entry point for the rhythm game."""

# pylint: disable=no-member

import sys

import pygame

from menu import Menu


class Game:
    """Core game loop and event handler."""

    def __init__(self, width=1200, height=900):
        """Initialize the display and menu."""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Rhythm Game")

        self.clock = pygame.time.Clock()
        self.running = True

        self.menu = Menu(self.screen)

    def handle_events(self):
        """Process all queued pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.menu.current_state in (
                        self.menu.SETTINGS,
                        self.menu.PLAY_GAME,
                    ):
                        self.menu.current_state = self.menu.MAIN_MENU
                    else:
                        self.running = False

            if self.menu.handle_event(event):
                self.running = False

    def draw(self):
        """Render the current screen."""
        self.menu.draw()
        pygame.display.flip()

    def run(self):
        """Run the main game loop until the user quits."""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
