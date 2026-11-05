import math
import time
import pygame
from pygame.sprite import Group
from charts import ASSETS_DIR

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

NOTE_IMAGE = pygame.image.load(ASSETS_DIR / "Sprites" / "circl.png").convert_alpha()
NOTE_RESIZED = pygame.transform.scale(NOTE_IMAGE, (60,60))

class Note(pygame.sprite.Sprite):
    LANE_LOCATIONS = [250, 350, 450, 550]
    SPAWN_OFFSET = 2.5
    SPAWN_Y = 50
    JUDGEMENT_LINE_Y = 400
    
    def __init__(self, lane: int, hitTime: float):
        super().__init__()
        self.image = NOTE_RESIZED
        self.lane = lane
        self.hitTime = hitTime
        self.spawnTime = hitTime - self.SPAWN_OFFSET

        self.startPos = (self.LANE_LOCATIONS[lane - 1], self.SPAWN_Y)
        self.endPos = (self.LANE_LOCATIONS[lane - 1], self.JUDGEMENT_LINE_Y)

        self.rect = self.image.get_rect()
        self.rect.center = self.startPos

    #returns position such that it always arrives at the end position at the hitTime, returns y value
    def getNewPosition(self, currentTime:float) -> int:
        totalTime = self.hitTime - self.spawnTime
        uptime = currentTime - self.spawnTime

        percentTime = uptime / totalTime
        y_1 = self.startPos[1]
        y_2 = self.endPos[1]
        distance = y_2 - y_1
        position = y_1 + distance * percentTime
        return int(position)

    def updatePos(self, currentTime:float):
        pos = self.getNewPosition(currentTime)
        self.rect.center = (self.rect.centerx, pos)

    def update(self, currentTime:float):
        self.updatePos(currentTime)


# testing

clock = pygame.time.Clock()
if __name__ == "__main__":
    notes: pygame.sprite.Group = pygame.sprite.Group()
    for i in range(20):
        n = Note(i % 4, i)
        notes.add(n)
    start = time.perf_counter()
    while True:
        current_time = time.perf_counter() - start
        for n in notes:
            n.updatePos(current_time)
        screen.fill((30, 30, 30))
        notes.draw(screen)
        pygame.display.flip()
        clock.tick(60)