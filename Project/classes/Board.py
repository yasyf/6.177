from constants import *
from imports import *
import helpers, path, itertools, Square, PacMan, Ghost, Actor

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
        self.pacmanObject = PacMan.PacMan(self.path[len(self.path)/2])
                          
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
                s = Square.Square(column,row,BLACK)
                self.squareObjects[(column,row)] = s
                self.squareSprites.add(s)

    def update_text(self):
        elapsed = g.font.render("Elapsed: %d Seconds" % ((pygame.time.get_ticks() - g.start)/1000),1,WHITE)
        g.screen.blit(elapsed, (.2*TEXT_OFFSET_X, TEXT_OFFSET_Y))
        score = g.font.render("Score: "+str(int(g.score)),1,WHITE)
        g.screen.blit(score, (1.45*TEXT_OFFSET_X, TEXT_OFFSET_Y))
        score = g.font.render("Pause",1,WHITE)
        g.screen.blit(score, (2.7*TEXT_OFFSET_X, TEXT_OFFSET_Y))

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
                s = Square.Square(p[0],p[1],WHITE)
                self.pathObjects[p] = s
                self.pathSprites.add(s)

    def get_surrounding_path_options(self,p):
        squares = path.get_surrounding_squares(p)
        options = dict(zip(squares, CARDINALS.keys()))
        for k in options.keys():
            if k not in self.path:
                del options[k]
        return options

    def add_ghosts(self):
        colors = ["Red","Pink","Orange","Blue"]
        squares = path.get_surrounding_squares((COLS/2,ROWS/2))

        for pair in zip(colors,squares,CARDINALS.keys()):
            ghost = Ghost.Ghost(pair[1],pair[0],pair[2])
            self.ghostObjects[pair[1]] = ghost
            self.ghostSprites.add(ghost)

    def reprint_all(self):
        self.squareSprites.draw(g.screen)
        self.pathSprites.draw(g.screen)
        #self.draw_grid()
        self.pacmanSprite.draw(g.screen)
        self.ghostSprites.draw(g.screen)
        self.update_text()