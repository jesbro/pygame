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

class Something(Sprite):
	def __init__(self):
		Sprite.__init__(self)
		self.image = image.load("loco.jpg").convert_alpha()#covert vs convert_alpha (make alpha-transparency for png images)
		self.rect = self.image.get_rect()

#def hit(self, target)
	#return self.rect.colliderect(target)
init()

screen = display.set_mode((640, 480))
display.set_caption("Games are fun")


sp = Something()
sprites = RenderPlain(sp)

time.set_timer(USEREVENT+ 1, DELAY) is for timer

