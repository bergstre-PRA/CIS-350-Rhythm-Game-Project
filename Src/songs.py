import pygame
from charts import *
from game import screen
from note import Note
import time

class Song:
    # variables
    offset = 0
    clock = pygame.time.Clock()

    def _get_current_time(self):
        return time.perf_counter() - self.start_time

    def _initNotes(self, song:str, difficulty:str):
        self.chart_notes = getChartNotes(song, difficulty)
        self.notes: pygame.sprite.Group = pygame.sprite.Group()
        if isinstance(self.chart_notes, bool):
            return False
        for n in self.chart_notes:
            lane = n["lane"]
            hit_time = n.get("hitTime")
            length = n["length"]
            if hit_time is None:
                continue
            note = Note(lane, hit_time, length)
            self.notes.add(note)
        print("initialized.")
        for n in self.notes:
            print(n)


    # initialize
    def __init__(self, song:str="SRGS1", difficulty:str="easy"):
        self.start_time = 0
        self.song = find_song(song)
        self.difficulty = difficulty
        self._initNotes(song, difficulty)

    #check input then start calculating score
    def _check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                     #key pressed
                     pass


    def check_miss(self):
        pass

    def endSong(self):
        pass

    def draw(self):
        screen.fill((30, 30, 30))
        self.active_notes.draw(screen)
        pygame.display.flip()

    def updateNotes(self):
        self.active_notes: pygame.sprite.Group = pygame.sprite.Group()
        for note in self.notes:
            if isinstance(note, Note):
                if note.rect.centery > -1 * note.rect.height and note.rect.y < screen.get_height():
                    note.active = True
                    self.active_notes.add(note)
                else:
                    note.active = False
                note.updatePos(self._get_current_time())
        

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
            self.updateNotes()
            self.draw()
            self.clock.tick(60)
            

        self.endSong()

'''
clock = pygame.time.Clock()
if __name__ == "__main__":
    
    start = time.perf_counter()
    while True:
        current_time = time.perf_counter() - start
        for n in notes:
            n.updatePos(current_time)
        screen.fill((30, 30, 30))
        notes.draw(screen)
        pygame.display.flip()
        clock.tick(60)    
'''