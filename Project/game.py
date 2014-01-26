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
    
    g.board = Board.Board()

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
            g.clock.tick(FRAMERATE)
            g.screen.fill(BLACK) #clear screen
            map(lambda x: x.animate(),g.board.ghostObjects.values()) #update ghost animation and move forward
            g.board.pacmanObject.animate() #move pacman forward and play animation
            g.board.reprint_all() #redraw all sprites
            pygame.display.flip() #flush to screen
            