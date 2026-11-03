import pygame
import sys
from button import Button
import button


class Game:

    # Game states
    MAIN_MENU = "main menu"
    SETTINGS = "settings"
    PLAY_GAME = "play game"

    def __init__(self, width=1200, height=900):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Menu Demo (Class-Based)")

        self.clock = pygame.time.Clock()
        self.running = True
        self.currentState = self.MAIN_MENU

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.DARK_GRAY = (100, 100, 100)
        self.BLUE = (65, 105, 225)
        self.GREEN = (46, 139, 87)
        self.RED = (178, 34, 34)
        self.LIGHT_BLUE = (70, 130, 180)
        self.LIGHT_GREEN = (60, 179, 113)
        self.LIGHT_RED = (205, 92, 92)

        # Fonts
        self.fontTitle = pygame.font.Font(None, 64)
        self.fontButton = pygame.font.Font(None, 36)

        # Settings variables
        self.volume = 50
        self.offset = 0.0

        # Game variables
        self.score = 0

        # Initialize buttons
        self._init_buttons()

    def _init_buttons(self):
        # Main Menu
        self.btnPlay = button.Button(
            450,
            220,
            300,
            100,
            "Play Game",
            self.GREEN,
            self.LIGHT_GREEN,
            self.fontButton,
        )
        self.btnSettings = button.Button(
            450,
            340,
            300,
            100,
            "Settings",
            self.BLUE,
            self.LIGHT_BLUE,
            self.fontButton,
        )
        self.btnQuit = button.Button(
            450,
            460,
            300,
            100,
            "Quit",
            self.RED,
            self.LIGHT_RED,
            self.fontButton
        )

        # Settings
        self.btnVolUp = button.Button(
            740,
            250,
            60,
            40,
            "+",
            self.DARK_GRAY,
            self.GRAY,
            self.fontButton,
        )
        self.btnVolDown = Button(
            400,
            250,
            60,
            40,
            "-",
            self.DARK_GRAY,
            self.GRAY,
            self.fontButton,
        )
        self.btnOffsetUp = button.Button(
            740,
            350,
            60,
            40,
            "+",
            self.DARK_GRAY,
            self.GRAY,
            self.fontButton,
        )
        self.btnOffsetDown = button.Button(
            400,
            350,
            60,
            40,
            "-",
            self.DARK_GRAY,
            self.GRAY,
            self.fontButton,
        )
        self.btnBackSettings = button.Button(
            450,
            500,
            300,
            100,
            "Back",
            self.DARK_GRAY,
            self.GRAY,
            self.fontButton,
        )

        # Game
        self.btnBackPlay = button.Button(
            450,
            700,
            300,
            100,
            "Main Menu",
            self.DARK_GRAY,
            self.GRAY,
            self.fontButton,
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.currentState in (self.SETTINGS, self.PLAY_GAME):
                        self.currentState = self.MAIN_MENU
                    else:
                        self.running = False

            # State-specific event handling
            if self.currentState == self.MAIN_MENU:
                if self.btnPlay.is_clicked(event):
                    self.currentState = self.PLAY_GAME
                elif self.btnSettings.is_clicked(event):
                    self.currentState = self.SETTINGS
                elif self.btnQuit.is_clicked(event):
                    self.running = False

            elif self.currentState == self.SETTINGS:
                if self.btnVolUp.is_clicked(event):
                    self.volume = min(100, self.volume + 10)
                elif self.btnVolDown.is_clicked(event):
                    self.volume = max(0, self.volume - 10)
                elif self.btnOffsetUp.is_clicked(event):
                    self.offset = round(min(1.0, self.offset + 0.1), 1)
                elif self.btnOffsetDown.is_clicked(event):
                    self.offset = round(max(-1.0, self.offset - 0.1), 1)
                elif self.btnBackSettings.is_clicked(event):
                    self.currentState = self.MAIN_MENU

            elif self.currentState == self.PLAY_GAME:
                if self.btnBackPlay.is_clicked(event):
                    self.currentState = self.MAIN_MENU

    def draw(self):
        self.screen.fill(self.BLACK)

        if self.currentState == self.MAIN_MENU:
            title_surf = self.fontTitle.render("MAIN MENU", True, self.WHITE)
            self.screen.blit(
                title_surf, title_surf.get_rect(center=(self.width // 2, 120))
            )

            self.btnPlay.draw(self.screen)
            self.btnSettings.draw(self.screen)
            self.btnQuit.draw(self.screen)

        elif self.currentState == self.SETTINGS:
            title_surf = self.fontTitle.render("SETTINGS", True, self.WHITE)
            self.screen.blit(
                title_surf, title_surf.get_rect(center=(self.width // 2, 120))
            )

            vol_text = self.fontButton.render(
                f"Volume: {self.volume}%", True, self.WHITE
            )
            self.screen.blit(
                vol_text, vol_text.get_rect(center=(self.width // 2, 270))
            )

            offset_text = self.fontButton.render(
                f"Offset: {self.offset:.1f}", True, self.WHITE
            )
            self.screen.blit(
                offset_text, offset_text.get_rect(center=(self.width // 2, 370))
            )

            self.btnVolDown.draw(self.screen)
            self.btnVolUp.draw(self.screen)
            self.btnOffsetDown.draw(self.screen)
            self.btnOffsetUp.draw(self.screen)
            self.btnBackSettings.draw(self.screen)

        elif self.currentState == self.PLAY_GAME:
            title_surf = self.fontTitle.render(
                f"Score: {self.score}", True, self.WHITE
            )
            self.screen.blit(
                title_surf, title_surf.get_rect(center=(self.width // 2, 100))
            )

            self.btnBackPlay.draw(self.screen)

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