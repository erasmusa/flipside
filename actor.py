import pygame
from pygame.locals import *

class Actor:
	def __init__(self, filename):
		self.image = pygame.image.load(filename)
		self.rect = self.image.get_rect()

class Player(Actor):
	"""This class is an object in the game that is directly controlled by the player."""
	x = 0
	y = 0
	speed = [0, 0]
	def __init__(self, filename):
		Actor.__init__(self, filename)
		
	def draw(self, screen):
		#physics
		self.x += self.speed[0]
		self.y += self.speed[1]
		
		#draw	
		draw_pos = self.rect.move(self.x, self.y)
		screen.blit(self.image, draw_pos)
		
	def handleKey(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				self.speed[1] = 1
			if event.key == pygame.K_UP:
				self.speed[1] = -1
			if event.key == pygame.K_RIGHT:
				self.speed[0] = 1
			if event.key == pygame.K_LEFT:
				self.speed[0] = -1
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
				self.speed[1] = 0
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				self.speed[0] = 0
			
		
	