from constants import *
from imports import *

def new_game():
    """
    Sets up all necessary components to start a new game
    """

    pygame.init() # initialize all imported pygame modules
    
    pygame.display.set_caption("Japanese PacMan") # caption sets title of Window 

    g.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
    
    g.board = classes.Board()

    g.clock = pygame.time.Clock()