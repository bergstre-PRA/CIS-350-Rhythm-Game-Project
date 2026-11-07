"""Main menu for the rhythm game."""

from __future__ import annotations

import pygame

from button import Button

from songs import Song


class Menu:
    """Contains the main menu, settings, and play flow."""

    # Variables for menu states
    MAIN_MENU = "main menu"
    SETTINGS = "settings"
    PLAY_GAME = "play game"

    def __init__(self, screen: pygame.Surface):
        """Initialize the menu with default settings and buttons."""
        self.current_state = self.MAIN_MENU

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gray = (200, 200, 200)
        self.dark_gray = (100, 100, 100)
        self.blue = (65, 105, 225)
        self.green = (46, 139, 87)
        self.red = (178, 34, 34)
        self.light_blue = (70, 130, 180)
        self.light_green = (60, 179, 113)
        self.light_red = (205, 92, 92)

        # Fonts
        self.font_title = pygame.font.Font(None, 64)
        self.font_button = pygame.font.Font(None, 36)

        # Settings variables
        self.volume = 50
        self.offset = 0.0

        # Game variables
        self.screen = screen
        self.screen_width = screen.get_width()
        self.song: Song | None = None
        self.points: int = 0

        # Initialize buttons
        self._init_buttons()

    def _init_buttons(self):
        """Create each menu button used by the game."""
        self.btn_play = Button(
            450,
            220,
            300,
            100,
            "Play Game",
            self.green,
            self.light_green,
            self.font_button,
        )
        self.btn_settings = Button(
            450, 340, 300, 100, "Settings",
            self.blue, self.light_blue, self.font_button,
        )
        self.btn_quit = Button(
            450, 460, 300, 100, "Quit",
            self.red, self.light_red, self.font_button,
        )

        # Settings buttons
        self.btn_vol_up = Button(
            740, 250, 60, 40, "+", self.dark_gray, self.gray, self.font_button,
        )
        self.btn_vol_down = Button(
            400, 250, 60, 40, "-", self.dark_gray, self.gray, self.font_button,
        )
        self.btn_offset_up = Button(
            740, 350, 60, 40, "+", self.dark_gray, self.gray, self.font_button,
        )
        self.btn_offset_down = Button(
            400, 350, 60, 40, "-", self.dark_gray, self.gray, self.font_button,
        )
        self.btn_back_settings = Button(
            450, 500, 300, 100, "Back",
            self.dark_gray, self.gray, self.font_button,
        )

        self.btn_back_play = Button(
            450, 700, 300, 100, "Main Menu",
            self.dark_gray, self.gray, self.font_button,
        )

    def handle_event(self, event):
        """Handle a pygame event based on the current menu state."""
        quit_requested = False

        if self.current_state == self.MAIN_MENU:
            if self.btn_play.is_clicked(event):

                self.current_state = self.PLAY_GAME
                self.song = Song(self.screen)
                self.song.play()
                self.points = self.song.score.points
                self.song = None
            elif self.btn_settings.is_clicked(event):
                self.current_state = self.SETTINGS
            elif self.btn_quit.is_clicked(event):
                quit_requested = True

        elif self.current_state == self.SETTINGS:
            if self.btn_vol_up.is_clicked(event):
                self.volume = min(100, self.volume + 10)
            elif self.btn_vol_down.is_clicked(event):
                self.volume = max(0, self.volume - 10)
            elif self.btn_offset_up.is_clicked(event):
                self.offset = round(min(1.0, self.offset + 0.1), 1)
            elif self.btn_offset_down.is_clicked(event):
                self.offset = round(max(-1.0, self.offset - 0.1), 1)
            elif self.btn_back_settings.is_clicked(event):
                self.current_state = self.MAIN_MENU

        elif self.current_state == self.PLAY_GAME:
            if self.btn_back_play.is_clicked(event):
                self.current_state = self.MAIN_MENU

        return quit_requested

    def draw(self):
        """Draw the current menu screen."""
        self.screen.fill(self.black)

        if self.current_state == self.MAIN_MENU:
            title_surface = self.font_title.render(
                "MAIN MENU", True, self.white
                )
            self.screen.blit(
                title_surface,
                title_surface.get_rect(center=(self.screen_width // 2, 120)),
            )

            self.btn_play.draw(self.screen)
            self.btn_settings.draw(self.screen)
            self.btn_quit.draw(self.screen)

        elif self.current_state == self.SETTINGS:
            title_surface = self.font_title.render(
                "SETTINGS", True, self.white
                )
            self.screen.blit(
                title_surface,
                title_surface.get_rect(center=(self.screen_width // 2, 120)),
            )

            vol_text = self.font_button.render(
                f"Volume: {self.volume}%", True, self.white
            )
            self.screen.blit(
                vol_text,
                vol_text.get_rect(center=(self.screen_width // 2, 270)),
            )

            offset_text = self.font_button.render(
                f"Offset: {self.offset:.1f}", True, self.white
            )
            self.screen.blit(
                offset_text,
                offset_text.get_rect(center=(self.screen_width // 2, 370)),
            )

            self.btn_vol_down.draw(self.screen)
            self.btn_vol_up.draw(self.screen)
            self.btn_offset_down.draw(self.screen)
            self.btn_offset_up.draw(self.screen)
            self.btn_back_settings.draw(self.screen)

        elif self.current_state == self.PLAY_GAME:
            title_surface = self.font_title.render(
                f"Score: {self.points}", True, self.white
            )
            self.screen.blit(
                title_surface,
                title_surface.get_rect(center=(self.screen_width // 2, 100)),
            )
            self.btn_back_play.draw(self.screen)
