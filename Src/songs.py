import pygame
from charts import *
import time

class Song:
    # variables
    offset = 0
    song_length = 0

    def _get_current_time(self):
        return time.perf_counter() - self.start_time

    # initialize
    def __init__(self, song="SRGS1", difficulty="easy"):
        self.start_time = 0
        self.song = song
        self.difficulty = difficulty
        self.chartNotes = getChartNotes(song, difficulty)

#check input then start calculating score
    def _check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                     #key pressed
                     pass


    def check_miss(self):
        pass

    def checkNoteSpawn(self):
        pass

    def endSong(self):
        pass

    def draw(self):
        pass
    def play(self):
        # call and convert chart data
        
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.play()
        self.start_time = time.perf_counter()

        while ((self._get_current_time() + self.offset) < self.song_length):
            self._check_input()
            self.check_miss()
            self.checkNoteSpawn()
            self.draw()

        self.endSong()

    