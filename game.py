from constants import *
from imports import *
import helpers

def new_game():
    """
    Sets up all necessary components to start a new game
    """
    g.reset()

    pygame.init() # initialize all imported pygame modules
    
    pygame.display.set_caption("Japanese PacMan") # caption sets title of Window 

    g.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)

    g.path_color = PATH_COLORS[random.randint(0,len(PATH_COLORS)-1)]

    g.font = pygame.font.SysFont("monospace", FONT_SIZE)
    
    g.board = Board.Board()

    g.clock = pygame.time.Clock()

    g.start = pygame.time.get_ticks()

    g.score = 0

    setup()

    main_loop()

def setup():
    g.board.reprint_all()
    pygame.display.flip()

def main_loop():
    g.stop = False
    pause_rect = pygame.Rect(4*TEXT_OFFSET_X - g.font.size("Pause")[0], TEXT_OFFSET_Y, g.font.size("Pause")[0], g.font.size("Pause")[1])
    while g.stop == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g.stop = True
                pygame.quit()
            elif event.type==pygame.MOUSEBUTTONUP:
                if g.done == True:
                    g.stop = True
                elif pause_rect.collidepoint(event.pos):
                    g.board.toggle_paused()
            elif event.type == pygame.KEYDOWN:
                helpers.check_keydown(event)
        if g.done == True:
            g.clock.tick(FRAMERATE)
            helpers.show_game_over()
            pygame.display.flip() #flush to screen  
        elif g.stop == False and g.board.paused == False: 
            g.clock.tick(FRAMERATE)
            g.screen.fill(BLACK) #clear screen
            map(lambda x: x.animate(),g.board.ghostObjects.values()) #update ghost animation and move forward
            g.board.pacmanObject.animate() #move pacman forward and play animation

            pacman_collision = pygame.sprite.spritecollideany(g.board.pacmanSprite.sprite, g.board.ghostSprites)
            if pacman_collision != None:
                g.board.pacmanObject.reset()
                g.lives -= 1
                if g.lives < 0:
                    g.done = True

            ghost_collisions = map(lambda x: pygame.sprite.spritecollide(x, g.board.ghostSprites, False, collided=lambda x,y: x.color != y.color and pygame.Rect.colliderect(x.rect, y.rect)),g.board.ghostObjects.values())
            ghost_collisions = filter(None, ghost_collisions)
            helpers.process_ghost_collisions(ghost_collisions)
            
            g.board.reprint_all() #redraw all sprites
            g.score += TIME_MULTIPLIER
            pygame.display.flip() #flush to screen
    if g.stop == True and g.done == True:
       g.reset()
       pygame.quit()
       new_game()