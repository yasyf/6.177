import pygame


class Sound():
	def __init__(self,fileName,volume=1.0):
		self.sound = pygame.mixer.Sound(fileName)
		self.sound.set_volume(volume)

	def play(self):
		self.stop()
		self.sound.play()

	def stop(self):
		self.sound.stop()

	def loop(self):
		self.stop()
		self.sound.play(-1)

def init_sounds():
	global dot, background, die, intro, consume, powerup, powerup_background

	intro = Sound("assets/Intro.wav",volume=0.9)
	dot = Sound("assets/Dot.wav",volume=0.5)
	die = Sound("assets/Die.wav",volume=0.9)
	consume = Sound("assets/Consume.wav",volume=1.0)
	powerup = Sound("assets/Powerup.wav",volume=1.0)
	powerup_background = Sound("assets/PowerupBackround.wav",volume=0.8)
	background = Sound("assets/Background.wav",volume=0.8)
	