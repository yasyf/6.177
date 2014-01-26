from constants import *
from imports import *
import random

def get_surrounding_squares_x(p):
    surrounding = [(-1,0), (1,0)]
    return [(x[0]+p[0],x[1]+p[1]) for x in surrounding]

def get_surrounding_squares_y(p):
    surrounding = [(0,1), (0,-1)]
    return [(x[0]+p[0],x[1]+p[1]) for x in surrounding]

def gen_skeleton_path():
    path_squares = []

    path_squares += [(x,0) for x in range(COLS)]
    path_squares += [(x,ROWS-1) for x in range(COLS)]
    path_squares += [(0,y) for y in range(ROWS)]
    path_squares += [(COLS-1,y) for y in range(ROWS)]

    path_squares += [(ROWS/2,x) for x in range(COLS)]
    path_squares += [(y,COLS/2) for y in range(ROWS)]

    return path_squares


def point_to_vector(p,magnitude,direction):
    path_squares = [(p[0]+(direction[0]*z),p[1]+(direction[1]*z)) for z in range(1,magnitude+1)]
    return path_squares


def gen_closest_wall_path(p):
    directions = {}
    directions[p[1]] = (0,-1) #up
    directions[ROWS-1-p[1]] = (0,1) #down
    directions[p[0]] = (-1,0) #left
    directions[COLS-1-p[0]] = (1,0) #right

    magnitude = min(directions.keys())
    direction = directions[magnitude]

    return point_to_vector(p,magnitude,direction)



def gen_random_path():
    circled = False
    current = (2,2)
    last_inc = 0
    path_squares = [(1,2),current]
    for x in range(400):
        done = False

        while done == False:
            x_inc, y_inc = [0,0]

            x_inc = random.randint(0,1)
            y_inc = x_inc^1

            if x_inc == 1 and last_inc != 0:
                x_inc *= -1 if random.randint(0,1) == 0 else 1
            elif y_inc == 1 and last_inc != 1:
                y_inc *= -1 if random.randint(0,1) == 0 else 1

            temp = (current[0]+x_inc,current[1]+y_inc)

            x_surrounding = len(set(path_squares) & set(get_surrounding_squares_x(temp)))
            y_surrounding = len(set(path_squares) & set(get_surrounding_squares_y(temp)))

            if x_surrounding > 1 or y_surrounding > 1 or (x_surrounding+y_surrounding > 3 and x != ROWS/2 and y != COLS/2):
                #TODO Force one direction to prevent square loop/getting stuck
                done = False
                continue 

            if (temp[0] > (COLS-1)) or (temp[0] < 0):
                done = True
                taken_y_vals = [z[1] for z in path_squares if z[0] == 1]
                while y_inc in taken_y_vals:
                    y_inc += 1
                    y_inc = y_inc % (ROWS-1)
                temp = (0,current[1]+y_inc)
                continue 

            if (temp[1] > (ROWS-1))  or (temp[1] < 0):
                done = True
                taken_x_vals = [z[0] for z in path_squares if z[1] == 1]
                while x_inc in taken_x_vals:
                    x_inc += 1
                    x_inc = x_inc % (COLS-1)
                temp = (current[0]+x_inc,0)
                continue

            temp = (current[0]+x_inc,current[1]+y_inc)

            done = True

        last_inc = abs(y_inc)  
        current = temp
        path_squares.append(current)
    g.current = current
    return path_squares
