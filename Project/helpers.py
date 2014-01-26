from constants import *
from imports import *

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
    if event.key == pygame.K_p:
        if g.board.paused:
            g.board.paused = False
        else:
            g.board.paused = True
        g.board.reprint_all()
    elif event.key == pygame.K_q:
        g.stop = True
        pygame.quit()
    elif event.key == pygame.K_RIGHT:
        g.board.pacmanObject.change_dir("right")
    elif event.key == pygame.K_LEFT:
        g.board.pacmanObject.change_dir("left")
    elif event.key == pygame.K_UP:
        g.board.pacmanObject.change_dir("up")
    elif event.key == pygame.K_DOWN:
        g.board.pacmanObject.change_dir("down")
