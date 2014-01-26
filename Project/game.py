from constants import *
from imports import *
import helpers

def new_game():
    """
    Sets up all necessary components to start a new game
    """

    pygame.init() # initialize all imported pygame modules
    
    pygame.display.set_caption("Japanese PacMan") # caption sets title of Window 

    g.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
    
    g.board = classes.Board()

    g.clock = pygame.time.Clock()

    setup()

    main_loop()

def setup():
    g.board.reprint_all()
    pygame.display.flip()

def main_loop():
    g.stop = False
    while g.stop == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g.stop = True
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                helpers.check_keydown(event)

        if g.stop == False and g.board.paused == False: 
            g.clock.tick(4)

            g.board.pacmanObject.update()
            map(lambda x: x.update(),g.board.ghostObjects.values())

            g.board.reprint_all()
            pygame.display.flip()
            