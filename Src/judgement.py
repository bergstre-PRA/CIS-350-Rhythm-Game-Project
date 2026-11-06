import pygame

class JudgementLine(pygame.sprite.Sprite):
    def __init__(self, color:tuple[int,int,int], width:int, height:int, x:int, y:int):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
