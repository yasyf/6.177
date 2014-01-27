from constants import *
from imports import *
from Actor import Actor

class PacMan(Actor):
    def __init__(self,p):
        self.img = "PacMan-0.png"
        self.transformations = ["PacMan-{0}.png".format(x) for x in range(2)]
        super(PacMan, self).__init__(self.img)
        self.goto(*p)