import pygame
import os
from pygame.locals import *

import actor

#Center the game window, because that just makes more sense to this dev
os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

size = width, height = 640, 480
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

#ball = {}
#ball['image'] = pygame.image.load("ball.bmp")
#ball['rect'] = ball['image'].get_rect()

ball = actor.Player("ball.bmp")

clock = pygame.time.Clock()

running = True

while running:
  screen.fill(black)
  ball.draw(screen)
  pygame.display.flip()
  clock.tick(60)
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT: 
      running = False
    if event.type in (pygame.KEYDOWN, pygame.KEYUP):
      ball.handleKey(event)
  
exit()
