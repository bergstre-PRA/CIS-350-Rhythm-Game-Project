import pygame

class Button:

    def __init__(self, x, y, width, height, text, color, hover_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hoverColor = hover_color
        self.font = font

    def draw(self, surface):
        mousePos = pygame.mouse.get_pos()

        currentColor = (
            self.hoverColor if self.rect.collidepoint(mousePos) else self.color
        )

        pygame.draw.rect(surface, currentColor, self.rect, border_radius=8)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=8)

        textSurf = self.font.render(self.text, True, (255, 255, 255))
        textRect = textSurf.get_rect(center=self.rect.center)
        surface.blit(textSurf, textRect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False