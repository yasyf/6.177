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
	global dot, background, die, intro

	intro = Sound("assets/Intro.wav")
	dot = Sound("assets/Dot.wav",volume=0.5)
	die = Sound("assets/Die.wav")
	background = Sound("assets/Background.wav",volume=0.8)
	