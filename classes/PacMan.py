from constants import *
from imports import *
from Actor import Actor

class PacMan(Actor):
	def __init__(self,p):
		self._dot = False
		self.img = "PacMan-0.png"
		self._die = None
		self.transformations = ["PacMan-{0}.png".format(x) for x in range(2)]
		super(PacMan, self).__init__(self.img)
		self.goto(*p)

	def animate(self):
		if self._count >= self.delay:
			g.handled_direction = False
			if self._dot:
				self._dot = False
		super(PacMan,self).animate()

	def reset(self):
		self.set_image(self.img)
		super(PacMan,self).reset()

	def update(self):
		if self._dot or self.transformations.index(self.img) > 0:
			self.img = self.transformations[(self.transformations.index(self.img)-1) % len(self.transformations)]
		else:
			self.img = self.transformations[self.transformations.index(self.img)]
		self.set_image(self.img)

	def change_dir(self, direction):
		g.handled_direction = True
		super(PacMan,self).change_dir(direction)

	def is_dying(self):
		return self._die > 0 if self._die else False

	def die(self):
		if self._die == None and g.board.is_paused():
			self._die = g.board.get_pause_ticks()
		elif not g.board.is_paused():
			self._die = None
			self.reset()
		else:
			percent = float(g.board.get_pause_ticks())/float(self._die)
			self.image = pygame.transform.rotozoom(self.image, percent*100*4, percent)
			g.board.reprint_no_ghosts()

