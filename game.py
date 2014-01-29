from constants import *
from imports import *
import helpers

def new_game():
    """
    Sets up all necessary components to start a new game
    """
    g.reset()

    pygame.init() # initialize all imported pygame modules

    pygame.mixer.init()
    
    sounds.init_sounds()

    pygame.display.set_caption("Japanese PacMan") # caption sets title of Window 

    g.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)

    g.path_color = PATH_COLORS[random.randint(0,len(PATH_COLORS)-1)]

    g.font = pygame.font.SysFont("monospace", FONT_SIZE)
    
    g.big_font = pygame.font.SysFont("monospace", FONT_SIZE*4)
    
    g.board = board.Board()

    g.clock = pygame.time.Clock()
    g.clock.tick(FRAMERATE)

    g.score = 0

    setup()

    main_loop()

def setup():
    g.board.reprint_all()
    pygame.display.flip()

def main_loop():
    g.stop = False
    pause_rect = pygame.Rect(4*TEXT_OFFSET_X - g.font.size("Pause")[0], TEXT_OFFSET_Y, g.font.size("Pause")[0], g.font.size("Pause")[1])
    
    g.board.pacmanObject.double_size()
    map(lambda x: x.double_size(),g.board.ghostObjects.values())

    g.board.draw_background()
    g.board.reprint_all()
    pygame.display.flip()
    g.board.toggle_paused(miliseconds=FRAMERATE * 2.7)
    sounds.intro.play()

    while g.stop == False:
        g.clock.tick(FRAMERATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                g.stop = True
                pygame.quit()
            elif event.type==pygame.MOUSEBUTTONUP:
                if pause_rect.collidepoint(event.pos):
                    g.board.toggle_paused()
            elif event.type == pygame.KEYDOWN:
                helpers.check_keydown(event)

        if g.done == True:
            g.screen.fill(BLACK) #clear screen
            helpers.show_game_over()
            pygame.display.flip() #flush to screen

        elif g.board.get_pause_ticks() > 0:
            g.board.decrement_pause()
            if g.played_intro:
                if g.board.pacmanObject.is_dying():
                    g.board.pacmanObject.die()
            else:
                helpers.show_intro()

        elif g.stop == False and not g.board.is_paused(): 
            g.screen.fill(BLACK) #clear screen
            g.board.draw_background()

            g.board.proccess_powerups()

            pacman_collision = pygame.sprite.spritecollideany(g.board.pacmanSprite.sprite, g.board.ghostSprites)
            if pacman_collision != None:
                sounds.dot.stop()
                if g.board.pacmanObject.is_super() and pacman_collision.is_vulnerable():
                    g.score += SUPER_CONSUME_SCORE_INCREMENT
                    pacman_collision.stop_vulnerable()
                    pacman_collision.reset()
                    sounds.consume.play()
                else:
                    g.board.toggle_paused(miliseconds=FRAMERATE)
                    g.board.pacmanObject.die()
                    g.lives -= 1
                    if g.lives < 0:
                        g.done = True
                    g.screen.fill(BLACK) #clear screen
                    g.board.draw_background()
                    g.board.reprint_no_ghosts()
                    pygame.display.flip()
                    time.sleep(1)
                    sounds.die.play()
                    continue

            powerup_collision = pygame.sprite.spritecollideany(g.board.pacmanSprite.sprite, g.board.powerupSprites)
            if powerup_collision != None and not g.board.pacmanObject.is_super():
                g.score += SUPER_SCORE_INCREMENT
                del g.board.powerupObjects[powerup_collision.get_current_pos()]
                g.board.powerupSprites.remove(powerup_collision)
                g.board.pacmanObject.go_super()
                sounds.powerup.play()

            dot_collision = pygame.sprite.spritecollideany(g.board.pacmanSprite.sprite, g.board.dotSprites)
            if dot_collision != None:
                g.board.pacmanObject._dot = True
                g.board.pacmanObject.update()
                sounds.dot.play()
                del g.board.dotObjects[dot_collision.col, dot_collision.row]
                g.board.dotSprites.remove(dot_collision)
                g.score += 1

            ghost_collisions = map(lambda x: pygame.sprite.spritecollide(x, g.board.ghostSprites, False, collided=lambda x,y: x.color != y.color and pygame.Rect.colliderect(x.rect, y.rect)),g.board.ghostObjects.values())
            ghost_collisions = filter(None, ghost_collisions)
            helpers.process_ghost_collisions(ghost_collisions)

            map(lambda x: x.animate(),g.board.ghostObjects.values()) #update ghost animation and move forward
            g.board.pacmanObject.animate() #move pacman forward and play animation
            
            g.board.reprint_no_ghosts() #redraw all sprites
            g.score += TIME_MULTIPLIER
            pygame.display.flip() #flush to screen
    if g.stop == True and g.done == True:
       g.reset()
       pygame.quit()
       new_game()