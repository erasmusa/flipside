import pygame
from pygame.locals import *
import json

class Frame:
	def __init__(self, filename, length):
		if filename not in Frame.loaded:
			Frame.loaded[filename] = pygame.image.load(filename)			
		self.image = Frame.loaded[filename]
		self.rect = self.image.get_rect()
		self.length = length
Frame.loaded = dict()



class Actor:
	state = dict()
	class AnimState:
		def __init__(self, frames):
			self.frame = list()
			for frame in frames:
				self.frame.append(Frame(frame['src'], frame['length'] if 'length' in frame else 1))
	def __init__(self, filename):
		with open(filename) as actor: 
			self.base = json.load(actor)
		for state in self.base['states']:
			self.state[state['name']] = Actor.AnimState(state['frames'])


class Player(Actor):
	"""This class is an object in the game that is directly controlled by the player."""
	x = 0
	y = 0
	speed = [0, 0]
	def __init__(self, filename):
		Actor.__init__(self, filename)
		self.frame = 0;
		self.state = 'stand'
		
	def draw(self, screen):
		#physics
		self.x += self.speed[0]
		self.y += self.speed[1]
		
		#draw	
		self.image = Actor.state[self.state].frame[self.frame].image
		self.rect  = Actor.state[self.state].frame[self.frame].rect
		self.frame += 1
		if self.frame >= len(Actor.state[self.state].frame):
			self.frame = 0
		
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
				self.state = 'walk'
				self.frame = 0
			if event.key == pygame.K_LEFT:
				self.speed[0] = -1
		if event.type == pygame.KEYUP:
			self.state = 'stand'
			self.frame = 0
			if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
				self.speed[1] = 0
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				self.speed[0] = 0
			
		
	