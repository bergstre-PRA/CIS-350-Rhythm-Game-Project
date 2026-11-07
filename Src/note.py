"""Note sprite used for rhythm gameplay."""

import pygame

from charts import ASSETS_DIR

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

NOTE_IMAGE = pygame.image.load(
    ASSETS_DIR / "Sprites" / "circl.png"
    ).convert_alpha()
NOTE_RESIZED = pygame.transform.scale(NOTE_IMAGE, (60, 60))


class Note(pygame.sprite.Sprite):
    """A falling note that moves toward the judgement line."""

    SPAWN_OFFSET = 2.5
    SPAWN_Y = -600

    def __init__(
        self, lane: int, hit_time: float, length: float, screen: pygame.Surface
    ):
        """Initialize a note at its spawn location."""
        super().__init__()

        screen_width = screen.get_width()
        screen_height = screen.get_height()

        span = screen_width // 2
        outside = (screen_width - span) // 2

        self.lane_locations = [
            outside + span * 1 // 8,
            outside + span * 3 // 8,
            outside + span * 5 // 8,
            outside + span * 7 // 8,
        ]
        self.judgement_line_y = int(screen_height * 0.9)

        self.image = NOTE_RESIZED
        self.length = length
        self.lane = lane
        self.hit_time = hit_time
        self.spawn_time = hit_time - self.SPAWN_OFFSET
        self.active = False

        self.start_pos = (self.lane_locations[lane], self.SPAWN_Y)
        self.end_pos = (self.lane_locations[lane], self.judgement_line_y)

        self.rect = self.image.get_rect()
        self.rect.center = self.start_pos

    def get_new_position(self, current_time: float) -> int:
        """Return the note's y-position for a given time."""
        total_time = self.hit_time - self.spawn_time
        uptime = current_time - self.spawn_time

        percent_time = uptime / total_time
        y_1 = self.start_pos[1]
        y_2 = self.end_pos[1]
        distance = y_2 - y_1
        position = y_1 + distance * percent_time
        return int(position)

    def update_pos(self, current_time: float):
        """Move the note to its current visual position."""
        pos = self.get_new_position(current_time)
        self.rect.center = (self.rect.centerx, pos)

    def draw(self, screen):
        """Draw the note if it is active."""
        if not self.active:
            return

        screen.blit(self.image, self.rect)
