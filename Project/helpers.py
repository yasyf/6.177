from constants import *
from imports import *

def get_row_top_p(row):
    """
    Returns the location of the top pixel in a square in
    row row, given the row height.
    """
    return (row * HEIGHT) + OFFSET

def get_col_left_p(col):
    """
    Returns the location of the leftmost pixel in a square in
    column col, given the column width.
    """
    return (col * WIDTH) + OFFSET