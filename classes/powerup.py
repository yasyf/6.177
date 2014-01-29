from constants import *
from imports import *
import helpers

class Powerup(pygame.sprite.Sprite):
    def __init__(self, col, row, width=WIDTH, height=HEIGHT):
        pygame.sprite.Sprite.__init__(self)

        self.width = WIDTH
        self.height = HEIGHT
        self.set_image()
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

    def set_image(self):
        self.image = pygame.image.load("assets/Powerup.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def get_current_pos(self):
        return (self.col,self.row)