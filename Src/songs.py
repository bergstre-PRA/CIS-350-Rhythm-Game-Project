"""Song playback and note logic."""

import time

import pygame

from charts import find_song, get_chart_notes
from judgement import JudgementLine
from note import Note
from scoring import Score


class Song:
    """Manage gameplay for a single song track."""

    offset = 0
    clock = pygame.time.Clock()

    def _get_current_time(self):
        """Return the elapsed time in seconds since the song started."""
        return time.perf_counter() - self.start_time

    def _init_notes(self, song: str, difficulty: str):
        """Populate note data for the selected chart and difficulty."""
        self.chart_notes = get_chart_notes(song, difficulty)
        self.notes: pygame.sprite.Group = pygame.sprite.Group()
        self.active_notes: pygame.sprite.Group = pygame.sprite.Group()
        if self.chart_notes is None:
            return False
        for note_data in self.chart_notes:
            lane = note_data["lane"]
            hit_time = note_data.get("hit_time", note_data.get("hitTime"))
            length = note_data["length"]
            if hit_time is None:
                continue
            note = Note(lane, hit_time, length, self.screen)
            self.notes.add(note)
        print("initialized.")
        for note in self.notes:
            print(note)
        return True

    def __init__(
        self,
        screen: pygame.Surface,
        song: str = "SRGS1",
        difficulty: str = "easy",
    ):
        """Set up a song and judgement line."""
        self.start_time = 0
        self.screen = screen
        self.screen_height = self.screen.get_height()
        self.screen_width = self.screen.get_width()
        self.song = find_song(song)
        self.difficulty = difficulty
        self.song_length = 0
        self.chart_notes = None
        self._init_notes(song, difficulty)
        self.score = Score()
        self.active_notes: pygame.sprite.Group = pygame.sprite.Group()
        self.judgement_line: JudgementLine = JudgementLine(
            (255, 255, 255),
            self.screen_width,
            self.screen_height // 8,
            self.screen_width // 2,
            int(self.screen_height * 0.9),
        )

    def _check_input(self):
        """Handle keyboard input for note hits."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                lane: int
                match event.key:
                    case pygame.K_d:
                        lane = 0
                    case pygame.K_f:
                        lane = 1
                    case pygame.K_j:
                        lane = 2
                    case pygame.K_k:
                        lane = 3
                    case _:
                        lane = -1
                if lane != -1:
                    lowest_note = None
                    highest_y = -1
                    for note in self.active_notes:
                        if (
                            isinstance(note, Note)
                            and self.judgement_line.rect.colliderect(note.rect)
                            and lane == note.lane
                        ):
                            if note.rect.y > highest_y:
                                lowest_note = note
                                highest_y = note.rect.y

                    if lowest_note is not None:
                        self.score.score_hit(
                            lowest_note, self._get_current_time()
                            )
                        lowest_note.active = False
                        self.notes.remove(lowest_note)
                        del lowest_note

    def check_miss(self):
        """Miss notes that passed the judgement line without a hit."""
        for note in self.active_notes:
            if isinstance(note, Note):
                if note.rect.y >= self.screen.get_height():
                    self.score.add_hit("miss")
                    note.active = False
                    self.active_notes.remove(note)
                    self.notes.remove(note)

    def draw(self):
        """Draw gameplay screen."""
        self.screen.fill((30, 30, 30))
        self.screen.blit(self.judgement_line.image, self.judgement_line.rect)
        self.active_notes.draw(self.screen)
        pygame.display.flip()

    def check_active_notes(self):
        """Activate notes whose spawn time has passed."""
        self.active_notes.empty()
        for note in self.notes:
            if isinstance(note, Note):
                if note.spawn_time <= self._get_current_time():
                    note.active = True
                    self.active_notes.add(note)
                else:
                    note.active = False

    def update_notes(self):
        """Update each active note position."""
        self.check_active_notes()
        for note in self.notes:
            if isinstance(note, Note) and note.active:
                note.update_pos(self._get_current_time())

    def play(self):
        """Play the selected song until it ends."""
        if self.song is None or self.chart_notes is None:
            return
        song_sound: pygame.mixer.Sound = pygame.mixer.Sound(self.song)
        self.song_length = song_sound.get_length()
        pygame.mixer.Sound.play(song_sound)
        self.start_time = time.perf_counter()

        while (self._get_current_time() + self.offset) < self.song_length:
            self._check_input()
            self.check_miss()
            self.update_notes()
            self.draw()
            self.clock.tick(60)
