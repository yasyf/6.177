from constants import *
from imports import *
import helpers, path, itertools, Square, PacMan, Ghost, Actor, Dot

class Board:
    def __init__(self):
        self.paused = False
        self.pausetime = 0
        self.lastpaused = None
        self.set_path()
        #initialize and populate Squares
        self.squareSprites = pygame.sprite.RenderPlain()
        self.squareObjects = {}

        self.draw_squares()

        #initialize and populate Path
        self.pathSprites = pygame.sprite.RenderPlain()
        self.pathObjects = {}

        self.draw_path()

        self.dotSprites = pygame.sprite.RenderPlain()
        self.dotObjects = {}

        self.draw_dots()

        #initialize and populate PacMan
        self.pacmanObject = PacMan.PacMan(self.path[len(self.path)/2])
                          
        self.pacmanSprite = pygame.sprite.GroupSingle()
        self.pacmanSprite.add(self.pacmanObject)

        self.ghostSprites = pygame.sprite.RenderPlain()
        self.ghostObjects = {}

        self.add_ghosts()

    def toggle_paused(self):
        self.paused = not self.paused
        if self.paused:
            self.lastpaused = pygame.time.get_ticks()
        else:
            self.pausetime += pygame.time.get_ticks() - self.lastpaused
            self.lastpaused = None
        g.screen.fill(BLACK)
        self.reprint_all()
        pygame.display.flip()

    def set_path(self):
        g.screen.fill(BLACK) #clear screen
        helpers.show_loading()
        pygame.display.flip()
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

    def draw_dots(self):
        for p in self.path:
            d = Dot.Dot(*p)
            self.dotObjects[p] = d
            self.dotSprites.add(d)

    def update_text(self):
        text = "Elapsed: %d Seconds" % (int((pygame.time.get_ticks() - g.start - self.pausetime)/1000))
        elapsed = g.font.render(text,1,WHITE)
        g.screen.blit(elapsed, (1*TEXT_OFFSET_X - g.font.size(text)[0], TEXT_OFFSET_Y))

        text = "Score: "+str(int(g.score))
        score = g.font.render(text,1,WHITE)
        g.screen.blit(score, (2*TEXT_OFFSET_X - g.font.size(text)[0], TEXT_OFFSET_Y))

        text = "Lives: "+str(g.lives)
        lives = g.font.render(text,1,WHITE)
        g.screen.blit(lives, (3*TEXT_OFFSET_X - g.font.size(text)[0], TEXT_OFFSET_Y))

        text = "Pause" if self.paused is False else "Resume"
        pause = g.font.render(text,1,WHITE)
        g.screen.blit(pause, (4*TEXT_OFFSET_X - g.font.size(text)[0], TEXT_OFFSET_Y))

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
                s = Square.Square(p[0],p[1],g.path_color)
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
        self.dotSprites.draw(g.screen)
        #self.draw_grid()
        self.pacmanSprite.draw(g.screen)
        self.ghostSprites.draw(g.screen)
        self.update_text()

    def reprint_no_ghosts(self):
        g.screen.fill(BLACK) #clear screen
        self.squareSprites.draw(g.screen)
        self.pathSprites.draw(g.screen)
        self.dotSprites.draw(g.screen)
        self.pacmanSprite.draw(g.screen)
        pygame.display.flip()