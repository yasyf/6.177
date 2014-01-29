from constants import *
import pygame

name = ""

def reset():
	global screen, board, clock, stop, done, font, score, lives, path_color, endpoints, handled_direction, played_intro, submitted

	screen = None
	board = None
	clock = None
	stop = False
	done = False
	submitted = False
	font = None
	score = 0
	lives = LIVES
	path_color = None
	handled_direction = False
	played_intro = False

	endpoints = []