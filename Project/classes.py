from constants import *
from imports import *
import helpers, path, itertools, math

class Square(pygame.sprite.Sprite):
    def __init__(self, col, row, color):
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
        self.set_path()
        #initialize and populate Squares
        self.squareSprites = pygame.sprite.RenderPlain()
        self.squareObjects = {}

        self.draw_squares()

        #initialize and populate Path
        self.pathSprites = pygame.sprite.RenderPlain()
        self.pathObjects = {}

        self.draw_path()

        #initialize and populate PacMan
        self.pacmanObject = PacMan(self.path[len(self.path)/2])
                          
        self.pacmanSprite = pygame.sprite.GroupSingle()
        self.pacmanSprite.add(self.pacmanObject)

        self.ghostSprites = pygame.sprite.RenderPlain()
        self.ghostObjects = {}

        self.add_ghosts()


    def set_path(self):
        self.path_raw = {BLUE: path.gen_skeleton_path(), GREEN: path.timeout(path.gen_connecting_path), RED: []}
        while self.path_raw[GREEN] == None:
            self.path_raw[GREEN] = path.timeout(path.gen_connecting_path)
        for p in g.endpoints:
            self.path_raw[RED] += path.gen_closest_wall_path(p)
        self.path = list(set(itertools.chain(*self.path_raw.values())))

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

    def draw_squares(self):
        for row in range(ROWS):
            for column in range(COLS):
                s = Square(column,row,BLACK)
                self.squareObjects[(column,row)] = s
                self.squareSprites.add(s)

    def draw_grid(self):
        """
        Draw the border grid on the screen.
        """
        for square in range(COLS+1):
            #vertical lines
            start_pos = (helpers.get_col_left_p(square),helpers.get_row_top_p(0))
            end_pos = (helpers.get_col_left_p(square),helpers.get_row_top_p(ROWS))
            pygame.draw.line(g.screen,WHITE,start_pos,end_pos)
        for square in range(ROWS+1):
            #horizontal lines
            start_pos = (helpers.get_col_left_p(0),helpers.get_row_top_p(square))
            end_pos = (helpers.get_col_left_p(COLS),helpers.get_row_top_p(square))
            pygame.draw.line(g.screen,WHITE,start_pos,end_pos)

    def draw_path(self):
        for k,v in self.path_raw.iteritems():
            for p in v:
                #s = Square(p[0],p[1],k)
                s = Square(p[0],p[1],WHITE)
                self.pathObjects[(p[0],p[1])] = s
                self.pathSprites.add(s)

    def add_ghosts(self):
        colors = ["Red","Pink","Orange","Blue"]
        squares = path.get_surrounding_squares((COLS/2,ROWS/2))

        for pair in zip(colors,squares):
            ghost = Ghost(pair[1],pair[0])
            self.ghostObjects[pair[1]] = ghost
            self.ghostSprites.add(ghost)

    def reprint_all(self):
        self.squareSprites.draw(g.screen)
        self.pathSprites.draw(g.screen)
        #self.draw_grid()
        self.pacmanSprite.draw(g.screen)
        self.ghostSprites.draw(g.screen)

class Actor(pygame.sprite.Sprite):
    directions = [(0,1), (-1,0), (0,-1), (1,0)] #in order going counterclockwise
    def __init__(self, imageFile, width=WIDTH, height=HEIGHT):
        pygame.sprite.Sprite.__init__(self)

        self.width = width
        self.height = height

        self.rotation = (0, 1) #pointing up
        self.degrees = 0 #pointing up

        self.set_image(imageFile)
        self.rect = self.image.get_rect()
        
    def goto(self, col, row):
        if g.board and (col,row) not in g.board.path:
            return
        if col < COLS:
            self.col = col
        if row < ROWS:
            self.row = row
        self.rect.x = helpers.get_col_left_p(self.col)
        self.rect.y = helpers.get_row_top_p(self.row)

    def get_current_square(self):
        return g.board.get_square(self.col,self.row)
    
    def step_forward(self):
        """
        Step forward in current direction
        """
        self.goto(self.col+self.rotation[0],self.row-self.rotation[1])

    def set_image(self, imageFile):
        self.image = pygame.image.load("assets/"+imageFile).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        if self.degrees == 180:
            self.image = pygame.transform.flip(self.image,True,False)
        else:
            self.image = pygame.transform.rotate(self.image,self.degrees)

    def update(self):
        self.img = self.transformations[(self.transformations.index(self.img)-1) % len(self.transformations)]
        self.set_image(self.img)

    def change_dir(self, direction):
        self.rotation = dict(zip(["up","left","down","right"],Actor.directions))[direction]
        self.degrees = math.degrees(math.atan2(self.rotation[1],self.rotation[0]))

class PacMan(Actor):
    def __init__(self,p):
        self.img = "PacMan-0.png"
        self.transformations = ["PacMan-{0}.png".format(x) for x in range(2)]
        super(PacMan, self).__init__(self.img)
        self.rotation = (1, 0) #pointing right
        self.degrees = 0 #pointing right
        self.goto(p[0],p[1])


class Ghost(Actor):
    def __init__(self,p,color):
        self.img = "{0}Ghost-0.png".format(color)
        self.color = color
        self.transformations = ["{0}Ghost-{1}.png".format(self.color,x) for x in range(5)]
        super(Ghost, self).__init__(self.img)
        self.rotation = (1, 0) #pointing right
        self.degrees = 0 #pointing right
        self.goto(p[0],p[1])




