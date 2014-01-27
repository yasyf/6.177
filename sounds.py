import pygame

def init_sounds():
	global dot
	
	dot = pygame.mixer.Sound("assets/Dot.wav")

def play_dot():
	pygame.mixer.Sound.play(dot)