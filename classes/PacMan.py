from constants import *
from imports import *
from Actor import Actor

class PacMan(Actor):
	def __init__(self,p):
		self._dot = False
		self.img = "PacMan-0.png"
		self.transformations = ["PacMan-{0}.png".format(x) for x in range(2)]
		super(PacMan, self).__init__(self.img)
		self.goto(*p)

	def animate(self):
		if self._count < self.delay:
			self._count += 1
		else:
			self.update()
			self.step_forward()
			if self._dot:
				self._dot = False

	def update(self):
		self._count = 0
		if self._dot or self.transformations.index(self.img) > 0:
			self.img = self.transformations[(self.transformations.index(self.img)-1) % len(self.transformations)]
		else:
			self.img = self.transformations[self.transformations.index(self.img)]
		self.set_image(self.img)
