from constants import *
import pygame

def reset():
	global screen, board, clock, stop, done, font, score, lives, path_color, endpoints, name

	screen = None
	board = None
	clock = None
	stop = False
	done = False
	font = None
	score = 0
	name = ""
	lives = LIVES
	path_color = None

	endpoints = []