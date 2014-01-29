from constants import *
from imports import *
import urllib2

def get_row_top_p(row):
    """
    Returns the location of the top pixel in a square in
    row row, given the row height.
    """
    return (row * HEIGHT) + OFFSET + MARGIN_TOP

def get_col_left_p(col):
    """
    Returns the location of the leftmost pixel in a square in
    column col, given the column width.
    """
    return (col * WIDTH) + OFFSET

def check_keydown(event):
    if event.key == pygame.K_q:
        g.stop = True
        pygame.quit()
    elif g.done == True and g.submitted == False:
        if event.key == pygame.K_BACKSPACE:
            if len(g.name) > 1:
                g.name = g.name[:-1]
        elif event.key == pygame.K_RETURN:
            g.submitted = True
        else:
            g.name = g.name + event.unicode.encode('ascii', errors='ignore')
    elif g.submitted == True:
        if event.key == pygame.K_RETURN:
            g.stop = True
    elif g.played_intro:
        if event.key == pygame.K_p:
            g.board.toggle_paused()
        elif g.handled_direction == False and g.board.paused == False:
            if event.key == pygame.K_RIGHT:
                g.board.pacmanObject.change_dir("right")
            elif event.key == pygame.K_LEFT:
                g.board.pacmanObject.change_dir("left")
            elif event.key == pygame.K_UP:
                g.board.pacmanObject.change_dir("up")
            elif event.key == pygame.K_DOWN:
                g.board.pacmanObject.change_dir("down")

def process_ghost_collisions(ghost_collisions):
    for i in range(0,len(ghost_collisions)-1,2):
        if len(ghost_collisions[i]) > 1 or len(ghost_collisions[i+1]) > 1: #if more than two ghosts colliding, reverse all of them
            for ghost in ghost_collisions[i] + ghost_collisions[i+1]:
                ghost.reverse_dir()
        else:
            if ghost_collisions[i][0].rotation != ghost_collisions[i+1][0].rotation: #only reverse two ghosts colliding if they are not stuck together
                ghost_collisions[i][0].reverse_dir()
                ghost_collisions[i+1][0].reverse_dir()

def show_loading():
    text = "Loading..."
    loading = g.font.render(text,1,WHITE)
    g.screen.blit(loading,(WINDOW_SIZE[0]/2 - g.font.size(text)[0]/2,WINDOW_SIZE[1]/2 + g.font.size(text)[1]/2))

def show_submitted(place):
    text = "You Are In %s Place" % (place)
    position = g.font.render(text,1,WHITE)
    g.screen.blit(position,(WINDOW_SIZE[0]/2 - g.font.size(text)[0]/2,WINDOW_SIZE[1]/2 + g.font.size(text)[1]/2))
    text = "New Game?"
    again = g.font.render(text,1,WHITE)
    g.screen.blit(again,(WINDOW_SIZE[0]/2 - g.font.size(text)[0]/2,WINDOW_SIZE[1]/2 + FONT_SIZE * 2 + g.font.size(text)[1]/2))

def show_game_over():
    if g.submitted:
        response = urllib2.urlopen('http://japanese-pacman-highscores.herokuapp.com/?name=%s&score=%d' % (urllib2.quote(g.name), g.score))
        g.screen.fill(BLACK) #clear screen
        show_submitted(response.read().strip())
        pygame.display.flip()
    else:
        game_over_screen()

def game_over_screen():
    text = "Game Over"
    game_over = g.font.render(text,1,WHITE)
    g.screen.blit(game_over,(WINDOW_SIZE[0]/2 - g.font.size(text)[0]/2,WINDOW_SIZE[1]/2 + g.font.size(text)[1]/2))
    text = "Score: " + str(int(g.score))
    score = g.font.render(text,1,WHITE)
    g.screen.blit(score,(WINDOW_SIZE[0]/2 - g.font.size(text)[0]/2,WINDOW_SIZE[1]/2 + FONT_SIZE * 2 + g.font.size(text)[1]/2))
    text = "Name: " + g.name
    name = g.font.render(text,1,WHITE)
    g.screen.blit(name,(WINDOW_SIZE[0]/2 - g.font.size(text)[0]/2,WINDOW_SIZE[1]/2 + FONT_SIZE * 4 + g.font.size(text)[1]/2))
