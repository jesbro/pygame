'''
Created by Jess Brown, 2016
jesbro@umich.edu
SI 206, Project 4: Pygame
'''

'''
References:
https://books.google.com/books?id=RLU1Gkm1JGoC&pg=PA442&lpg=PA442&dq=pygame+wait+to+start+game&source=bl&ots=pkJHMtgvAC&sig=DHPSwufY7L2XPQoGtY5rYwHM0p8&hl=en&sa=X&ved=0ahUKEwjb3tTZ0czQAhUJbSYKHVGjA_oQ6AEIQzAG#v=onepage&q=pygame%20wait%20to%20start%20game&f=false
'''

from pygame import *
import random
from pygame.sprite import *

pygame.init();

DELAY = 5;#20;
blue = (127, 174, 249)
green = (122, 244, 66)
black = (0,0,0)
white = (255,255,255)

screenx = 900 #leaving room around the edges
screeny = 600


class Border(Sprite):

    def __init__(self):
        Sprite.__init__(self)

        im = image.load(r"media\path_large.png").convert_alpha()
        self.image = pygame.transform.scale(im, (900, 100))
        
        # self.image = pygame.Surface([900, 100], pygame.SRCALPHA, 32)
        # self.image.fill((255,0,255,50))

        self.rect = self.image.get_rect()

    def setpos(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Monkey(Sprite):

    def __init__(self):
        Sprite.__init__(self)

        im = image.load(r"media\ninja_monkey.png").convert_alpha()
        self.image = pygame.transform.scale(im, (100, 100))

        self.rect = self.image.get_rect()

    # def setpos(self, pos):
        # self.rect.center = pos

    def setpos(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Star(Monkey):

    def __init__(self):
        Monkey.__init__(self)
        Sprite.__init__(self)

        im = image.load(r"media\ninja_star.png").convert_alpha()
        self.image = pygame.transform.scale(im, (30, 30))

        self.rect = self.image.get_rect()

    def move(self):
        self.rect.x += 3
        self.rect.y += 3


class Bloon(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        im = image.load(r"media\bloon_blue.png").convert_alpha()
        self.image = pygame.transform.scale(im, (70, 90))

        self.rect = self.image.get_rect()
        #self.miss = 0 # keeps track of how many bloons get through entire path

    def lmove(self):
        self.rect.x -= 2

    def rmove(self):
        self.rect.x += 2

    def umove(self):
        self.rect.y -= 2

    def dmove(self):
        self.rect.y += 2

    def hit(self, border):
        return self.rect.colliderect(border)

    def setpos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def pop(self):
        self.kill()

    def travel(self, ud):
        if ud:
            bloon.dmove()
            bloon.rmove()
        else:
            bloon.umove()
            bloon.rmove()

    def escaped(self):
        if self.rect.center > (screenx, screeny): 
            return True
        return False
        

#main
init()

screen = display.set_mode((900, 600))
display.set_caption("Pop the bloons!")

f = font.Font(None, 30)
fbig = font.Font(None, 100)

b1 = Border() #top border
b2 = Border() #bottom border
bloon = Bloon() #balloon
monkey = Monkey() #monkey
star = Star() #ninja star

sprites = RenderPlain(bloon, monkey)
time.set_timer(USEREVENT+ 1, DELAY) #is for timer

b1.setpos(0, 228)
b2.setpos(0, 445)
bloon.setpos(0, 328)
monkey.setpos(50, 228)

bg = image.load(r"media\path_bg.png").convert_alpha()
screen.blit(bg, (0,0)) #sets background image

hits = 0 #bloons hit
health = 1 #-1 for every escaped bloon

udtrigger = True #true = need to go up, false = need to go down
place = fbig.render("Click on the grass to place a monkey!", False, black)
screen.blit(place, (450, 300))

e = event.poll()
# if e.type == MOUSEBUTTONDOWN:
#     monkey.setpos(mouse.get_pos())

# while e.type != MOUSEBUTTONDOWN: 
#     event = pygame.event.wait()

while True:
    # event = pygame.event.wait() 

    e = event.poll()
    # e.type = wait()
#see if bloon needs to move up or down
    if bloon.hit(b2):
        udtrigger = False
    elif bloon.hit(b1):
        udtrigger = True

#determine what to move or to exit game
    if e.type == QUIT:
        quit()
        break

    elif e.type == USEREVENT + 1:
        bloon.travel(udtrigger)
        try: star.move()
        except: pass

    elif e.type == KEYDOWN:
        star.setpos(80, 248)
        sprites = RenderPlain(bloon, monkey, star)
        star.move()

    if bloon.hit(star):
        mixer.Sound(r"media\pop.wav").play()
        bloon.kill()
        star.kill()
        hits += 1
        bloon = Bloon()
        bloon.setpos(0, 328)
        sprites = RenderPlain(bloon, monkey)

    if bloon.escaped():
        health -= 1

        if health == 0: 
            t3 = fbig.render("Game Over", False, black)
            screen.blit(t3, (450, 300))
            e.wait()

        bloon.pop()
        bloon = Bloon()
        bloon.setpos(0, 328)
        sprites = RenderPlain(bloon, monkey)


    t = f.render("Hits: " + str(hits), False, black)
    t2 = f.render("Health: "+ str(health), False, black)
    screen.blit(bg, [0,0])
    screen.blit(t, (700, 20)) 
    screen.blit(t2, (700, 50))  
    sprites.update()
    sprites.draw(screen)
    display.update()