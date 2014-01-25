from constants import *
from imports import *
import helpers

class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        pygame.sprite.Sprite.__init__(self)

        self.color = color
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(self.color)

        self.row = row
        self.col = col
        self.rect = self.image.get_rect()
        self.rect.x = helpers.get_col_left_p(self.col)
        self.rect.y = helpers.get_row_top_p(self.row)

    def get_rect(self):
        """
        Returns the rect object that belongs to this Square
        """
        return self.rect
   
class Board:
    def __init__(self):

        self.paused = False
        
        #initialize and populate Squares
        self.squareSprites = pygame.sprite.RenderPlain()
        self.squareObjects = {}
        
        for row in range(ROWS):
            for column in range(COLS):
                s = Square(row,column,WHITE)
                self.squareObjects[(column,row)] = s
                self.squareSprites.add(s)

        #initialize and populate PacMan
        self.pacmanObject = PacMan()
                          
        self.pacmanSprite = pygame.sprite.GroupSingle()
        self.pacmanSprite.add(self.pacmanObject)

    def get_square(self, x, y):
        """
        Given an (x, y) pair, return the Square at that location
        """
        try:
            return self.boardSquares[(x,y)]
        except KeyError:
            x = x % self.size[1]
            y = y % self.size[0]
            return self.boardSquares[(x,y)]

    def get_current_square(self):
        """
        Rotate the ant, depending on the color of the square that it's on,
        and returns the square that the ant is currently on
        """
        square = self.pacmanObject.get_current_square()
        return square

    def draw_grid(self):
        """
        Draw the border grid on the screen.
        """
        for square in range(COLS+1):
            #vertical lines
            start_pos = (helpers.get_col_left_p(square),get_row_top_loc(0))
            end_pos = (helpers.get_col_left_p(square),get_row_top_loc(size[0]))
            pygame.draw.line(g.screen,BLACK,start_pos,end_pos)
        for square in range(ROWS+1):
            #horizontal lines
            start_pos = (helpers.get_col_left_p(0),get_row_top_loc(square))
            end_pos = (helpers.get_col_left_p(size[1]),get_row_top_loc(square))
            pygame.draw.line(g.screen,WHITE,start_pos,end_pos)

class Actor(pygame.sprite.Sprite):
    transformations = [(0,1), (-1,0), (0,-1), (1,0)] #in order going counterclockwise
    def __init__(self, imageFile, width=WIDTH, height=HEIGHT):
        pygame.sprite.Sprite.__init__(self)

        self.width = width
        self.height = height

        self.set_image(imageFile)
        self.rect = self.image.get_rect()

        self.rotation = (0, 1) #pointing up

        self.goto(0,0)
        
    def goto(self, col, row):
        self.col = col
        self.row = row
        self.rect.x = helpers.get_col_left_p(self.col)
        self.rect.y = helpers.get_row_top_p(self.row)

    def get_current_square(self):
        return g.board.get_square(self.col,self.row)
        
    def rotate_left(self):
        """
        Rotate 90 degrees counterclockwise
        """
        self.image = pygame.transform.rotate(self.image, 360/len(Actor.transformations))
        self.rotation = Actor.transformations[(Actor.transformations.index(self.rotation)+1) % len(Actor.transformations)] #next step in transformations

    def rotate_right(self):
        """
        Rotate 90 degrees clockwise
        """
        self.image = pygame.transform.rotate(self.image,-360/len(Actor.transformations))
        self.rotation = Actor.transformations[(Actor.transformations.index(self.rotation)-1) % len(Actor.transformations)] #previous step in transformations
    
    def step_forward(self):
        """
        Step forward in current direction
        """
        self.goto(self.rotation[0],-self.rotation[1])

    def set_image(self, imageFile):
        self.image = pygame.image.load("assets/"+imageFile).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

class PacMan(Actor):
    def __init__(self):
        super(PacMan, self).__init__("PacMan.png")
        self.rotation = (1, 0) #pointing right


