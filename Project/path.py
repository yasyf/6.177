from constants import *
from imports import *
import random, threading

def timeout(func, timeout_duration=0.1, default=None, *args, **kwargs):
    """This function will spawn a thread and run the given function
    using the args, kwargs and return the given default value if the
    timeout_duration is exceeded.
    http://stackoverflow.com/questions/492519/timeout-on-a-python-function-call/494273#494273
    """ 
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = default
            self._die = threading.Event()
        def run(self):
            self.result = func(self._die, *args, **kwargs)
        def kill(self):
            self._die.set()
    it = InterruptableThread()
    it.start()
    it.join(timeout_duration)
    if it.isAlive():
        it.kill()
    return it.result

def get_surrounding_squares_x(p):
    surrounding = [(-1,0), (1,0)]
    return [(x[0]+p[0],x[1]+p[1]) for x in surrounding]

def get_surrounding_squares_y(p):
    surrounding = [(0,1), (0,-1)]
    return [(x[0]+p[0],x[1]+p[1]) for x in surrounding]

def get_surrounding_squares(p):
    surrounding = [(0,1), (-1,0), (0,-1), (1,0)]
    return [(x[0]+p[0],x[1]+p[1]) for x in surrounding]

def gen_skeleton_path():
    path_squares = []

    path_squares += [(x,0) for x in range(COLS)]
    path_squares += [(x,ROWS-1) for x in range(COLS)]
    path_squares += [(0,y) for y in range(ROWS)]
    path_squares += [(COLS-1,y) for y in range(ROWS)]

    path_squares += [(ROWS/2,x) for x in range(COLS)]
    path_squares += [(y,COLS/2) for y in range(ROWS)]

    for i in range(random.randint(1,3)):
        y = random.randint(1,2)*random.randint(1,(ROWS/2)-1)
        if y in [(ROWS/2)-1,ROWS/2,(ROWS/2)+1,ROWS-2]:
            continue
        if random.randint(0,1) == 0:
            path_squares += [(x,y) for x in range(COLS/2)]
        else:
            path_squares += [(x,y) for x in range(COLS/2,COLS)]
    for i in range(random.randint(1,3)):
        x = random.randint(1,2)*random.randint(1,(COLS/2)-1)
        if x in [(COLS/2)-1,COLS/2,(COLS/2)+1,COLS-2]:
            continue
        if random.randint(0,1) == 0:
            path_squares += [(x,y) for y in range(ROWS/2)]
        else:
            path_squares += [(x,y) for y in range(ROWS/2,ROWS)]

    return path_squares


def point_to_vector(p,magnitude,direction):
    path_squares = [(p[0]+(direction[0]*z),p[1]+(direction[1]*z)) for z in range(1,magnitude+1)]
    return path_squares

def get_directions(p):
    directions = {}
    directions[p[1]] = (0,-1) #up
    directions[ROWS-1-p[1]] = (0,1) #down
    directions[p[0]] = (-1,0) #left
    directions[COLS-1-p[0]] = (1,0) #right
    return directions

def gen_closest_wall_path(p):
    directions = get_directions(p)
    magnitude = min(directions.keys())
    direction = directions[magnitude]

    return point_to_vector(p,magnitude,direction)

def away_from_wall(p):
    directions = get_directions(p)
    magnitude = max(directions.keys())
    direction = directions[magnitude]

    return direction 

def gen_connecting_path(_die):
    circled = False
    current = (random.randint(COLS/5,(4*COLS)/5),random.randint(ROWS/5,(4*ROWS)/5))
    g.endpoints = [current]
    last_inc = 0
    path_squares = [current]
    for x in range(500):
        done = False

        while done == False and not _die.is_set():
            temp = current
            x_inc, y_inc = [0,0]

            x_inc = random.randint(0,1)
            y_inc = x_inc^1

            seed = random.randint(0,5)

            if seed < 3:
                if x_inc == 1 and last_inc != 0:
                    x_inc *= -1 if random.randint(0,5) == 0 else 1
                elif y_inc == 1 and last_inc != 1:
                    y_inc *= -1 if random.randint(0,5) == 0 else 1
            elif seed < 5:
                if x_inc == 1 and last_inc != 0:
                    x_inc *= -1 if random.randint(0,3) == 0 else 1
                elif y_inc == 1 and last_inc != 1:
                    y_inc *= -1 if random.randint(0,2) == 0 else 1
            else:
                if x_inc == 1 and last_inc != 0:
                    x_inc *= -1 if random.randint(0,1) == 0 else 1
                elif y_inc == 1 and last_inc != 1:
                    y_inc *= -1 if random.randint(0,2) == 0 else 1

            temp = (current[0]+x_inc,current[1]+y_inc)

            x_surrounding = list(set(path_squares) & set(get_surrounding_squares_x(temp)))
            y_surrounding = list(set(path_squares) & set(get_surrounding_squares_y(temp)))

            if (len(x_surrounding) + len(y_surrounding)) > 2:
                done = False
                continue

            if len(x_surrounding) > 1:
                x_inc = 0
                y_inc = -1 if random.randint(0,1) == 0 else 1
            elif len(y_surrounding) > 1:
                y_inc = 0
                x_inc = -1 if random.randint(0,1) == 0 else 1

            temp = (current[0]+x_inc,current[1]+y_inc)

            if (temp[0] > (COLS-1)) or (temp[0] < 0):
                done = True
                taken_y_vals = [z[1] for z in path_squares if z[0] == 1]
                while y_inc in taken_y_vals:
                    y_inc += 1
                    y_inc = y_inc % (ROWS-1)
                temp = (0,current[1]+y_inc)
                continue 

            temp = (current[0]+x_inc,current[1]+y_inc)

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
    g.endpoints.append(current)
    return path_squares
