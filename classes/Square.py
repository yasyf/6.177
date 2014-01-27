from constants import *
from imports import *
import helpers

class Square(pygame.sprite.Sprite):
    def __init__(self, col, row, color):
        pygame.sprite.Sprite.__init__(self)

        self.color = color
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(self.color)

        self.row = row
        self.col = col
        self.rect = self.image.get_rect()
        self.rect.x = helpers.get_col_left_p(self.col)
        self.rect.y = helpers.get_row_top_p(self.row)

    def get_rect(self):
        """
        Returns the rect object that belongs to this Square
        """
        return self.rect