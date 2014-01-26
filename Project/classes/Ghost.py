from constants import *
from imports import *
from Actor import Actor

class Ghost(Actor):
    def __init__(self,p,color):
        self.img = "{0}Ghost-0.png".format(color)
        self.color = color
        self.transformations = ["{0}Ghost-{1}.png".format(self.color,x) for x in range(5)]
        super(Ghost, self).__init__(self.img)
        self.rotation = (1, 0) #pointing right
        self.degrees = 0 #pointing right
        self.goto(p[0],p[1])