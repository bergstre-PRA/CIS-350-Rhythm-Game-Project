import pygame
from charts import *
from game import screen
from note import Note
from scoring import Score
from judgement import JudgementLine
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
        self.active_notes: pygame.sprite.Group = pygame.sprite.Group()
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
        self.score = Score()
        self.active_notes: pygame.sprite.Group = pygame.sprite.Group()
        self.judgementLine: JudgementLine = JudgementLine((255,255,255), 800, 100, 400, 500)

    #check input then start calculating score
    def _check_input(self):
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
                        if isinstance(note, Note) and self.judgementLine.rect.colliderect(note.rect) and lane == note.lane:
                            if note.rect.y > highest_y:
                                lowest_note = note
                                highest_y = note.rect.y

                    if lowest_note is not None:
                        self.score.scoreHit(lowest_note, self._get_current_time())
                        lowest_note.active = False
                        self.notes.remove(lowest_note)
                        del lowest_note

    def check_miss(self):
        for note in self.active_notes:
            if isinstance(note, Note):
                if note.rect.y >= screen.get_height():
                    self.score.addHit("miss")
                    note.active = False
                    self.active_notes.remove(note)
                    self.notes.remove(note)

    def endSong(self):
        print("end song")

    def draw(self):
        screen.fill((30, 30, 30))
        screen.blit(self.judgementLine.image, self.judgementLine.rect)
        self.active_notes.draw(screen)
        pygame.display.flip()

    def checkActiveNotes(self):
        self.active_notes.empty()
        for note in self.notes:
            if isinstance(note, Note):
                if note.spawnTime <= self._get_current_time():
                    note.active = True
                    self.active_notes.add(note)
                else:
                    note.active = False

    def updateNotes(self):
        self.checkActiveNotes()
        for note in self.notes:
            if isinstance(note, Note) and note.active:
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
            print("time left: " + str(self.song_length - self._get_current_time()))
            

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