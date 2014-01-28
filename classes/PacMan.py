from constants import *
from imports import *
from actor import Actor

class PacMan(Actor):
	def __init__(self,p):
		self._dot = False
		self._die = None
		self._super = False
		self.set_normal_transformations()
		super(PacMan, self).__init__(self.img)
		self.goto(*p)

	def set_normal_transformations(self):
		self.img = "PacMan-0.png"
		self.transformations = ["PacMan-{0}.png".format(x) for x in range(2)]

	def set_super_transformations(self):
		self.img = "Poof.png"
		self.transformations = ["Poof.png"]

	def animate(self):
		if self._count >= self.delay:
			g.handled_direction = False
			if self._dot:
				self._dot = False
			if self.is_super():
				self.decrement_super()

		super(PacMan,self).animate()

	def reset(self):
		self.set_image(self.img)
		if self.is_super():
			self.stop_super()
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

	def go_super(self):
		if self.is_super():
			self.stop_super()
		self._super = SUPER_TIME
		self.set_super_transformations()
		map(lambda x: x.go_vulnerable(),g.board.ghostObjects.values())
		sounds.background.stop()
		sounds.powerup_background.loop()

	def stop_super(self):
		self._super = False
		self.set_normal_transformations()
		map(lambda x: x.stop_vulnerable(),g.board.ghostObjects.values())
		sounds.powerup_background.stop()
		sounds.background.loop()

	def decrement_super(self):
		self._super -= 1
		if self._super < 1:
			self.stop_super()

	def is_super(self):
		return self._super

