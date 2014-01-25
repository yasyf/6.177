"""
6.177 Problem Set (IAP 2014)
Completed by Yasyf Mohamedali (yasyf@mit.edu)
"""

"""
*** Warm-up Exercises ***
"""

### 1. Numerical Operations

# Fill in the function below which takes in two positive integers
# and returns either ((a - b) to the power of b) OR ((a + b) modulo 10)
# depending on which formula produces a greater value.
#
# operate(10, 2)
# ==> 64
# operate(2, 3)
# ==> 5

def operate(a, b):
    first = (a-b)**b
    second = (a+b)%10
    return first if first > second else second


### 2. String and list operation

# Fill in the function below. It takes in a list of strings (of length >= 3)
# called myStrings and trims the strings to exclude the first and last
# character of each string. It then returns the list in reverse order
# with *only* the first alphabetical letter of each new string capitalized
# (not always the first character!).
# Do NOT modify the original passed-in list.
#
# myList = ['25maroon', 'ComBInE', 'apple', '0315']
# fix_strings(myList) 
# ==> ['31', 'Ppl', 'Ombin', '5Maroo']
# myList 
# ==> ['25maroon', 'ComBInE', 'apple', '0315']

def ucfirstalpha(string):
    import re
    index = re.search("[a-zA-Z]",string)
    if index:
        return string[:index.start()].lower() + string[index.start()].upper() + string[index.start()+1:].lower()
    return string

def fix_strings(myStrings):
    newList = [x[1:len(x)-1] for x in myStrings]
    newList = list(map(ucfirstalpha,newList))
    newList.reverse()
    return newList



### 3. Class instances and methods

# Using the Car class defined below as reference, 
# fill in the modify() method below so that it takes in a Car instance
# and changes the name of the instance to 'Python' and its color to 'Ruby'.
# Then, pass in parameters into the combineTrips() method
# so that it sums together all weighted trips (miles divided by
# miles per gallon) and stores the decimal value in self.__combination.
# Your function should return True if successful.
#
# class Car(object):
#     def __init__(self, name, color):
#         self.__name = name
#         self.__color = color
#         # This dict saves trips in the format (miles, miles_per_gallon).
#         self.__trips = {
#             "ski trip": (101, 28)
#             "groceries": (15, 18)
#             "leisure": (3, 9)
#             "apple store": (17, 22)
#             "airport": (93, 30)
#             "canada": (1337, 26)
#             "engine check": (0, 0)
#         }
#         self.__combination = None
#
#     def get_color(self):
#         return self.__color
#
#     def change_color(self, color):
#         self.__color = color
#
#     def get_name(self):
#         return self.__name
#
#     def new_name(self, name):
#         self.__name = name
#
#     def get_combination(self):
#         return self.__combination
#
#     def get_miles_per_gallon(self):
#         return self.__mpg
#
#     def combine_trips(self, reduce_function):
#         self.__combination = reduce_function(self.__trips)
#
# myCar = Car('Moriarty', 'Sherlock')
# modify(myCar)
# ==> True
# myCar.get_name()
# ==> 'Python'
# myCar.get_color()
# ==> 'Ruby'
# myCar.get_combination()
# ==> 60.07

def modify(carInstance):
    carInstance.new_name("Python")
    carInstance.change_color("Ruby")
    carInstance.combine_trips(lambda x: reduce(lambda y,z: y+(float(z[0])/float(z[1]) if z[1] != 0 else 0),x.values(),0))
    return True


"""
***** Langton's Ant *****
"""

# Algorithm described at http://en.wikipedia.org/wiki/Langton%27s_ant

import pygame, sys, random, argparse
import tests as T


height = None
width = None
offset = 10

# RGB Color definitions
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)

def get_row_top_loc(rowNum):
    """
    Returns the location of the top pixel in a square in
    row rowNum, given the row height.
    """
    return (rowNum*height) + offset

def get_col_left_loc(colNum):
    """
    Returns the location of the leftmost pixel in a square in
    column colNum, given the column width.
    """
    return (colNum*width) + offset


def draw_pause_button(screen, size, paused=False):
    textSize = height/2
    font = pygame.font.Font(None,textSize)
    if paused:
        pause_text = font.render("Resume", True, green, white)
    else:
        pause_text = font.render("Pause", True, red, white)
    pause_rect = pause_text.get_rect()
    pause_rect.centerx = (size[1] + 1) * width
    pause_rect.centery = (size[0]/2) * height
    screen.blit(pause_text,pause_rect)
    return pause_rect

def draw_quit_button(screen, size):
    textSize = height/2
    font = pygame.font.Font(None,textSize)
    quit_text = font.render("Quit", True, red, white)
    quit_rect = quit_text.get_rect()
    quit_rect.centerx = (size[1] + 1) * width
    quit_rect.centery = (size[0] - 1) * height
    screen.blit(quit_text,quit_rect)
    return quit_rect

def update_text(screen, message, size):
    """
    Used to display the text on the right-hand part of the screen.
    You don't need to code anything, but you may want to read and
    understand this part.
    """
    
    textSize = height/2
    font = pygame.font.Font(None, textSize)
    text = font.render(message, True, black, white)
    textRect = text.get_rect()
    textRect.centerx = (size[1] + 1) * width
    textRect.centery = height
    screen.blit(text, textRect)

def draw_side_bar(screen,size,paused=False):

    pygame.draw.rect(screen, white,((size[1] * width)+offset, offset,((2 * width)-(2*offset)),(size[0] * height)))
    return draw_pause_button(screen,size,paused=paused), draw_quit_button(screen,size)

def new_game():
    """
    Sets up all necessary components to start a new game
    of Langton's Ant.
    """
    global width, height

    parser = argparse.ArgumentParser(description='Langton\'s Ant')
    parser.add_argument('-r','--rows', help='Number of rows', type=int, required=False)
    parser.add_argument('-c','--columns', help='Number of columns', type=int, required=False)
    parser.add_argument('-l','--length', help='Side length of square\'s side', type=int, required=False)
    parser.add_argument('-x','--startx', help='Starting x-position', type=int, required=False)
    parser.add_argument('-y','--starty', help='Starting y-position', type=int, required=False)
    args = vars(parser.parse_args())

    num_rows = args["rows"]
    num_cols = args["columns"]
    width = args["length"]
    height = width
    startx = args["startx"]
    starty = args["starty"]
    
    if args['startx'] and not args['starty']:
        parser.error( '-y is required when -x is set.')
    if args['starty'] and not args['startx']:
        parser.error( '-x is required when -y is set.')

    if startx and startx > num_cols-1:
        parser.error('Starting x-position must be between 0 and ' + str(num_cols-1))
    if starty and starty > num_rows-1:
        parser.error('Starting y-position must be between 0 and ' + str(num_rows-1))

    while num_rows == None:
        num_rows = input("Number of rows?\n")
    while num_cols == None:
        num_cols = input("Number of columns?\n")
    while width == None:
        width = input("Side length of square?\n")
        height = width

    size = (num_rows,num_cols)

    pygame.init() # initialize all imported pygame modules

    window_size = [(size[1] + 2) * width, size[0] * height + 20] # width, height
    screen = pygame.display.set_mode((window_size), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME)
    
    pause_rect, quit_rect = draw_side_bar(screen,size)

    pygame.display.set_caption("Langton's Ant") # caption sets title of Window 

    board = Board(screen, size, startx, starty)

    moveCount = 0

    clock = pygame.time.Clock()

    main_loop(screen, board, moveCount, clock, False, False, pause_rect, quit_rect)

def draw_grid(screen, size, color=black):
    """
    Draw the border grid on the screen.
    """
    for square in range(size[1]+1):
        #vertical lines
        start_pos = (get_col_left_loc(square),get_row_top_loc(0))
        end_pos = (get_col_left_loc(square),get_row_top_loc(size[0]))
        pygame.draw.line(screen,color,start_pos,end_pos)
    for square in range(size[0]+1):
        #horizontal lines
        start_pos = (get_col_left_loc(0),get_row_top_loc(square))
        end_pos = (get_col_left_loc(size[1]),get_row_top_loc(square))
        pygame.draw.line(screen,color,start_pos,end_pos)

# Main program Loop: (called by new_game)
def main_loop(screen, board, moveCount, clock, stop, pause, pause_rect, quit_rect):
    board.squares.draw(screen) # draw Sprites (Squares)
    draw_grid(screen, board.size)
    board.theAnt.draw(screen) # draw ant Sprite
    update_text(screen, "Move #" + str(moveCount), board.size)
    pygame.display.flip() # update screen
    
    if stop == True:
        again = raw_input("Would you like to run the simulation again? If yes, type 'yes'\n")
        if again == 'yes':
            new_game()
    while stop == False:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #user clicks close
                stop = True
                pygame.quit()
            elif event.type==pygame.MOUSEBUTTONUP:
                if pause_rect.collidepoint(event.pos):
                    if board.paused:
                        board.paused = False
                    else:
                        board.paused = True
                    board.reprint_all()
                elif quit_rect.collidepoint(event.pos):
                    top = True
                    pygame.quit()

            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    if board.paused:
                        board.paused = False
                    else:
                        board.paused = True
                    board.reprint_all()
                elif event.key==pygame.K_q:
                    stop = True
                    pygame.quit()

        if stop == False and board.paused == False: 
            pygame.display.flip()
            clock.tick(10)
            #--- Do next move ---#

            # Step 1: Rotate class Ant(pygame.sprite.Sprite):
            square = board.rotate_ant_get_square() #rotate the ant and save it's current square
            board.squares.draw(screen) # draw Sprites (Squares) - they should cover up the ant's previous position
            draw_grid(screen,board.size) #draw the grid
            board.moveCount += 1
            board.theAnt.draw(screen) # draw ant Sprite (rotated)
            
            #pygame.display.flip() # update screen
            clock.tick(5)
            
            # Step 2: Flip color of square:
            square.flip_color() #flip the color of the square
            board.squares.draw(screen) # draw Sprites (Squares) - they should cover up the ant's previous position
            draw_grid(screen,board.size) #draw the grid
            board.theAnt.draw(screen) # draw ant Sprite (rotated)
            
            #pygame.display.flip() #update screen
            clock.tick(5)
            
            # Step 3: Move Ant
            board.ant.step_forward() #make the ant step forward
            board.squares.draw(screen) # draw Sprites (Squares) - they should cover up the ant's previous position
            draw_grid(screen,board.size) #draw the grid
            board.theAnt.draw(screen) # draw ant Sprite (rotated)
            
            #pygame.display.flip() # update screen
            clock.tick(5)

            board.reprint_all()
            # ------------------------

    pygame.quit() # closes things, keeps idle from freezing


class Square(pygame.sprite.Sprite):
    transformations = {white: grey, grey: white} 
    def __init__(self, row, col, color):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.color = color
        self.image = pygame.Surface([width, height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect() # gets a rect object with width and height specified above
                                            # a rect is a pygame object for handling rectangles
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)
          

    def get_rect_from_square(self):
        """
        Returns the rect object that belongs to this Square
        """
        return self.rect

    def flip_color(self):
        """
        Flips the color of the square (white -> black or 
        black -> white)
        """
        self.color = Square.transformations[self.color]
        self.image.fill(self.color)
   
class Board:
    def __init__(self, screen, size, startx, starty):

        self.size = size
        self.screen = screen
        self.moveCount = 0
        self.paused = False
        
        #---Initializes Squares (the "Board")---#
        self.squares = pygame.sprite.RenderPlain()
        self.boardSquares = {}
        
        #---Populate boardSquares with Squares---#
        for row in range(size[0]):
            for column in range(size[1]):
                s = Square(row,column,white)
                self.boardSquares[(column,row)] = s
                self.squares.add(s)

        #---Initialize the Ant---#
        if startx and starty:
            self.ant = Ant(self, startx, starty)
        else:
            self.ant = Ant(self, random.randint(0,self.size[1]-1), random.randint(0,self.size[0]-1))
                          
        #---Adds Ant to the "theAnt" Sprite List---#
        self.theAnt = pygame.sprite.RenderPlain()
        self.theAnt.add(self.ant)

    def get_square(self, x, y):
        """
        Given an (x, y) pair, return the Square at that location
        """
        try:
            return self.boardSquares[(x,y)]
        except KeyError:
            x = x % self.size[1]
            y = y % self.size[0]
            self.ant.col = x
            self.ant.row = y
            self.ant.rect_to_point()
            self.theAnt.draw(self.screen) # draw ant Sprite
            pygame.display.flip() # update screen
            return self.boardSquares[(x,y)]

    def rotate_ant_get_square(self):
        """
        Rotate the ant, depending on the color of the square that it's on,
        and returns the square that the ant is currently on
        """
        square = self.ant.get_current_square()
        if square.color == white:
            self.ant.rotate_right()
        else:
            self.ant.rotate_left()
        return square

    def reprint_all(self):
        self.squares.draw(self.screen) # draw Sprites (Squares)
        self.theAnt.draw(self.screen) # draw ant Sprite
        draw_side_bar(self.screen,self.size,paused=self.paused)
        draw_grid(self.screen,self.size) #draw the grid
        update_text(self.screen, "Move #" + str(self.moveCount), self.size)
        pygame.display.flip() # update screen
         

class Ant(pygame.sprite.Sprite):
    transformations = [(0,1), (-1,0), (0,-1), (1,0)] #in order going counterclockwise
    def __init__(self, board, col, row):
        pygame.sprite.Sprite.__init__(self)
        self.col = col
        self.row = row
        self.rotation = (0, 1) # pointing up
        self.board = board
        self.set_pic()
        self.rect = self.image.get_rect()
        self.rect_to_point()
        
    def rect_to_point(self):
        self.rect.x = get_col_left_loc(self.col)
        self.rect.y = get_row_top_loc(self.row)

    def get_current_square(self):
        return self.board.get_square(self.col,self.row)
        
    def rotate_left(self):
        """
        Rotates the ant 90 degrees counterclockwise
        """
        self.image = pygame.transform.rotate(self.image,90)
        self.rotation = Ant.transformations[(Ant.transformations.index(self.rotation)+1)%4] #next step in transformations

    def rotate_right(self):
        """
        Rotates the ant 90 degrees clockwise
        """
        self.image = pygame.transform.rotate(self.image,-90)
        self.rotation = Ant.transformations[(Ant.transformations.index(self.rotation)-1)%4] #previous step in transformations
    
    def step_forward(self):
        """
        Make the ant take a step forward in whatever direction it's currently pointing.
        Don't forget - row numbers increase from top to bottom and column numbers
        increase from left to right!
        """
        self.col += self.rotation[0]
        self.row -= self.rotation[1]
        self.rect_to_point()
    
    def set_pic(self):
        """
        Sets the picture that represents our Ant.
        If you want to use a new picture, you'll need to change
        this method.
        """
        self.image = pygame.image.load("ant.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

if __name__ == "__main__":
    # Uncomment this line to test your warmup answers:
    #T.test_warmup()

    # Uncomment this line to test Part 2:
    #T.test_part_two()

    # Uncomment this line to test Part 3:
    #T.test_part_three()

    # Uncomment this line to call new_game when this file is run:
    new_game()
    
    pass
