'''
Created by Jess Brown, 2016
jesbro@umich.edu
SI 206, Project 4: Pygame
'''

from pygame import *
import random
from pygame.sprite import *

pygame.init();

DELAY = 8000;
bgcolor = (0,0,255)

class Bloon(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		
		self.image = image.load("bloon.jpg").convert_alpha()#covert vs convert_alpha (make alpha-transparency for png images)
		self.rect = self.image.get_rect()

	def move(self):
		try:
			self.rect.x += 1
			self.rect.y += 1
		except:
			print ("fail")

#def hit(self, target)
	#return self.rect.colliderect(target)
init()

screen = display.set_mode((640, 640))
display.set_caption("Games are fun")

f = font.Font(None, 25)

bloon = Bloon()
sprites = RenderPlain(bloon)

hits = 0
time.set_timer(USEREVENT+ 1, DELAY) #is for timer

while True:
	e = event.poll()

	if e.type == QUIT:
		quit()
		break

	elif e.type == USEREVENT + 1:
		bloon.move()

	screen.fill(bgcolor)
	sprites.update()
	sprites.draw(screen)
	display.update()