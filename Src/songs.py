import pygame
from game import screen # type: ignore
from charts import *
from note import Note # type: ignore
import time

class Song:
    # variables
    offset = 0
    active_notes: pygame.sprite.Group = pygame.sprite.Group()

    def _get_current_time(self):
        return time.perf_counter() - self.start_time        

    # initialize
    def __init__(self, song:str="SRGS1", difficulty:str="easy"):
        self.start_time = 0
        self.song = find_song(song)
        self.difficulty = difficulty
        self.chart_notes = getChartNotes(song, difficulty)



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
        if isinstance(self.song, bool) or isinstance(self.chart_notes, bool):
            return
        songSound: pygame.mixer.Sound = pygame.mixer.Sound(self.song)
        self.song_length = songSound.get_length()
        pygame.mixer.Sound.play(songSound)
        self.start_time = time.perf_counter()

        while ((self._get_current_time() + self.offset) < self.song_length):
            self._check_input()
            self.check_miss()
            self.checkNoteSpawn()
            self.draw()
            

        self.endSong()

    