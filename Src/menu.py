import pygame
from button import Button
from songs import Song

class Menu:

    # Variables for menu states
    MAIN_MENU = "main menu"
    SETTINGS = "settings"
    PLAY_GAME = "play game"

    def __init__(self, screen):
        """initializes the menu with default settings and buttons."""
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
        self.screen = screen
        self.song: Song | None = None
        self.points: int = 0

        # Initialize buttons
        self._init_buttons()

    def _init_buttons(self):
        """initialized all buttons for the menu"""
        self.btnPlay = Button(
            450, 220, 300, 100,
            "Play Game",
            self.GREEN, self.LIGHT_GREEN, self.fontButton
        )
        self.btnSettings = Button(
            450, 340, 300, 100,
            "Settings",
            self.BLUE, self.LIGHT_BLUE, self.fontButton
        )
        self.btnQuit = Button(
            450, 460, 300, 100,
            "Quit",
            self.RED, self.LIGHT_RED, self.fontButton
        )

        # Settings buttons
        self.btnVolUp = Button(
            740, 250, 60, 40,
            "+",
            self.DARK_GRAY, self.GRAY, self.fontButton
        )
        self.btnVolDown = Button(
            400, 250, 60, 40,
            "-",
            self.DARK_GRAY, self.GRAY, self.fontButton
        )
        self.btnOffsetUp = Button(
            740, 350, 60, 40,
            "+",
            self.DARK_GRAY, self.GRAY, self.fontButton
        )
        self.btnOffsetDown = Button(
            400, 350, 60, 40,
            "-",
            self.DARK_GRAY, self.GRAY, self.fontButton
        )
        self.btnBackSettings = Button(
            450, 500, 300, 100,
            "Back",
            self.DARK_GRAY, self.GRAY, self.fontButton
        )

        # Game buttons
        self.btnBackPlay = Button(
            450, 700, 300, 100,
            "Main Menu",
            self.DARK_GRAY, self.GRAY, self.fontButton
        )

    def handle_event(self, event):
        """handles events based on the current state of the menu
        
        checks between different menu states do determine types of events
        and what to output based on current menu and event type

        event = the event type to be handled
        """
        quit_requested = False

        if self.currentState == self.MAIN_MENU:
            if self.btnPlay.is_clicked(event):
                self.currentState = self.PLAY_GAME
                self.song = Song(self.screen)
                self.song.play()
                self.points = self.song.score.points
                self.song = None
            elif self.btnSettings.is_clicked(event):
                self.currentState = self.SETTINGS
            elif self.btnQuit.is_clicked(event):
                quit_requested = True

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

        return quit_requested

    def draw(self, width):
        """draws the current state of the menu on the given screen
        
        creates and draws the current menu state using buttons and screen size
        to position the elements. All elements are drawn on the specified screen.

        screen = the surface to draw the menu on
        width = the width of the screen to help position elements
        """
        self.screen.fill(self.BLACK)

        if self.currentState == self.MAIN_MENU:
            title_surf = self.fontTitle.render("MAIN MENU", True, self.WHITE)
            self.screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 120)))

            self.btnPlay.draw(self.screen)
            self.btnSettings.draw(self.screen)
            self.btnQuit.draw(self.screen)

        elif self.currentState == self.SETTINGS:
            title_surf = self.fontTitle.render("SETTINGS", True, self.WHITE)
            self.screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 120)))

            vol_text = self.fontButton.render(f"Volume: {self.volume}%", True, self.WHITE)
            self.screen.blit(vol_text, vol_text.get_rect(center=(width // 2, 270)))

            offset_text = self.fontButton.render(f"Offset: {self.offset:.1f}", True, self.WHITE)
            self.screen.blit(offset_text, offset_text.get_rect(center=(width // 2, 370)))

            self.btnVolDown.draw(self.screen)
            self.btnVolUp.draw(self.screen)
            self.btnOffsetDown.draw(self.screen)
            self.btnOffsetUp.draw(self.screen)
            self.btnBackSettings.draw(self.screen)

        elif self.currentState == self.PLAY_GAME:
            title_surf = self.fontTitle.render(f"Score: {self.points}", True, self.WHITE)
            self.screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 100)))
            self.btnBackPlay.draw(self.screen)