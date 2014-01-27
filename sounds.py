import pygame


class Dot():
	def __init__(self):
		self.options =["assets/Dot.wav".format(x) for x in range(1)]
		self.snd = self.options[0]
		self.sound = pygame.mixer.Sound(self.snd)

	def play(self):
		self.stop()
		self.snd = self.options[(self.options.index(self.snd)-1) % len(self.options)]
		self.sound = pygame.mixer.Sound(self.snd)
		pygame.mixer.Sound.play(self.sound)

	def stop(self):
		pygame.mixer.Sound.stop(self.sound)

def init_sounds():
	global dot

	dot = Dot()
	