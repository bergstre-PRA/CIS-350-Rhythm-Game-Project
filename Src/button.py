"""Button widget used by the game's menus."""


import pygame


class Button:
    """A clickable UI button."""

    def __init__(self, x, y, width, height, text, color, hover_color, font):
        """creates a button with the given parameters.

        using the set variables you can create a button at a specific location
        with a set size color and text. There is also an variable for the color
        of the button while hovored as well as one for the font of the text.

        x = the horizontal position of the button
        y = the vertical position of the button
        width = the horizontal size of the button
        height = the vertical size of the button
        text = the text that will be displayed on the button
        color = the color of the button when not hovered
        hover_color = the color of the button when hovered
        font = the font of the text
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font

    def draw(self, surface):
        """draws the button on the given surface.

        this function deals with drawing the button on the screen as well as
        determining the color based on cursor location

        surface = the surface to draw the button on
        """
        mouse_pos = pygame.mouse.get_pos()

        current_color = (
            self.hover_color if
            self.rect.collidepoint(mouse_pos)
            else self.color
        )

        pygame.draw.rect(surface, current_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=8)

        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        """Return True when the button is clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
