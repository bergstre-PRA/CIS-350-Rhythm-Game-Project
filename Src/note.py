import pygame

class Note(pygame.sprite.Sprite):
    spawnOffset = 2.5
    startPos = (-50, 0)
    endPos = (400,0)
    
    def __init__(self, rect: pygame.Rect, lane: int, hitTime: float):
        super().__init__()
        self.rect = rect
        self.lane = lane
        self.hitTime = hitTime
        self.spawnTime = hitTime - self.spawnOffset

    #returns position such that it always arrives at the end position at the hitTime, returns y value
    def getNewPosition(self, currentTime:float) -> float:
        totalTime = self.hitTime - self.spawnTime
        uptime = currentTime - self.spawnTime

        percentTime = uptime / totalTime
        y_1 = self.startPos[1]
        y_2 = self.endPos[1]
        distance = y_2 - y_1
        position = y_1 + distance * percentTime
        return position

