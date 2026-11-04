import pygame
from charts import *
import time

class Song:
    # variables
    offset = 0
    


    def _get_current_time(self):
        return time.perf_counter() - self.start_time

    def _initNotes(self, amount: int = 5):
        pass

    # initialize
    def __init__(self, song:str="SRGS1", difficulty:str="easy"):
        self.start_time = 0
        self.song = find_song(song)
        self.difficulty = difficulty
        chart_notes: list[ChartNote] | bool = getChartNotes(song, difficulty)
        if isinstance(chart_notes, bool):
            #failed to load chart
            pass
        self._initNotes()



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
        if isinstance(self.song, bool):
            return
        songSound: pygame.mixer.Sound = pygame.mixer.Sound(self.song)
        self.song_length = songSound.get_length()
        pygame.mixer.Sound.play(songSound)
        self.start_time = time.perf_counter()

        while ((self._get_current_time() + self.offset) < self.start_time + self.song_length):
            self._check_input()
            self.check_miss()
            self.checkNoteSpawn()
            self.draw()

        self.endSong()

    