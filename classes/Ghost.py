from constants import *
from imports import *
from actor import Actor

class Ghost(Actor):
    def __init__(self,p,color,direction):
        self.color = color
        self.set_normal_transformations()
        super(Ghost, self).__init__(self.img)
        self.vulnerable = False
        self.delay = ANIMATION_DELAY * 2
        self.change_dir(direction)
        self.goto(*p)

    def step_forward(self):
    	next_forward = (self.col + self.rotation[0], self.row + self.rotation[1]) 
    	opposite = (self.col - self.rotation[0], self.row - self.rotation[1]) 
    	options = g.board.get_surrounding_path_options((self.col,self.row)) #dictionary in the form of {SQUARE: DIRECTION}
    	if opposite in options.keys() and len(options) > 1:
    		del options[opposite]
    	if len(options) == 1:
    		self.change_dir(options.values()[0])
    	elif next_forward in options.keys() and random.randint(0,3) != 0:
    		self.change_dir(options[next_forward])
    	else:
    		self.change_dir(options.values()[random.randint(0,len(options)-1)])
    	super(Ghost,self).step_forward()

    def set_normal_transformations(self):
        self.img = "{0}Ghost-0.png".format(self.color)
        self.transformations = ["{0}Ghost-{1}.png".format(self.color,x) for x in range(2)]

    def set_vulnerable_transformations(self):
        self.img = "SpecialGhost-0.png"
        self.transformations = ["SpecialGhost-{0}.png".format(x) for x in range(2)]
  
    def go_vulnerable(self):
        self.vulnerable = True
        self.set_vulnerable_transformations()

    def stop_vulnerable(self):
        self.vulnerable = False
        self.set_normal_transformations()

    def is_vulnerable(self):
        return self.vulnerable
