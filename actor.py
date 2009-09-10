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
				billy = Frame(frame['src'], frame.get('length', 1))
				billy.rect = billy.rect.move( frame.get('x-offset', 0), frame.get('y-offset', 0) )
				self.frame.append(billy)
	def __init__(self, filename):
		with open(filename) as actor: 
			self.base = json.load(actor)
		for state in self.base['states']:
			self.state[state['name']] = Actor.AnimState(state['frames'])
			
class Animation:
	# This class is used by game objects after actors have been loaded. It expects an Actor instance,
	# and will maintain the animation state for that actor by exposing some very handy functions.
	def __init__(self, Actor, State):
		self.actor = Actor
		self.state = State
		self.frame = 0
		self.framepos = 0
	def draw(self, screen, x, y):
		#Pick out the current image, based on the state and frame data
		image = self.actor.state[self.state].frame[self.frame].image
		rect  = self.actor.state[self.state].frame[self.frame].rect
		draw_pos = rect.move(x, y)
		screen.blit(image, draw_pos)
	def update(self):
		#This function advances the frame counter, accounting for any delays.
		self.framepos += 1
		if (self.framepos >= self.actor.state[self.state].frame[self.frame].length):
			self.frame += 1
			self.framepos = 0
			if self.frame >= len(self.actor.state[self.state].frame):
				self.frame = 0
	def setState(self, newstate):
		self.state = newstate
		self.frame = 0
		self.framepos = 0


class Player(Actor):
	"""This class is an object in the game that is directly controlled by the player."""
	x = 0
	y = 0
	speed = [0, 0]
	def __init__(self, filename):
		Actor.__init__(self, filename)
		self.anim = Animation(Actor, 'stand')
		
		
	def draw(self, screen):
		#physics
		self.x += self.speed[0]
		self.y += self.speed[1]
		
		#draw	
		self.anim.draw(screen, self.x, self.y)
		self.anim.update()
		
	def handleKey(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				self.speed[1] = 1
			if event.key == pygame.K_UP:
				self.speed[1] = -1
			if event.key == pygame.K_RIGHT:
				self.speed[0] = 1
				self.anim.setState('walk')
			if event.key == pygame.K_LEFT:
				self.speed[0] = -1
		if event.type == pygame.KEYUP:
			self.anim.setState('stand')
			self.frame = 0
			if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
				self.speed[1] = 0
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				self.speed[0] = 0
			
		
	