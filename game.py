'''
Created by Jess Brown, 2016
jesbro@umich.edu
SI 206, Project 4: Pygame
'''

'''
References:
https://books.google.com/books?id=RLU1Gkm1JGoC&pg=PA442&lpg=PA442&dq=pygame+wait+to+start+game&source=bl&ots=pkJHMtgvAC&sig=DHPSwufY7L2XPQoGtY5rYwHM0p8&hl=en&sa=X&ved=0ahUKEwjb3tTZ0czQAhUJbSYKHVGjA_oQ6AEIQzAG#v=onepage&q=pygame%20wait%20to%20start%20game&f=false
http://nullege.com/codes/show/src@g@a@GameDevelopment-HEAD@examples@students_works@pygame@farmyard@FarmyardRoundEmUp.py/861/pygame.event.wait
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

    def setpos(self, x, y):
        self.rect.center = (x, y)

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

class BottomStar(Monkey):

    def __init__(self):
        Monkey.__init__(self)
        Sprite.__init__(self)

        im = image.load(r"media\ninja_star.png").convert_alpha()
        self.image = pygame.transform.scale(im, (30, 30))

        self.rect = self.image.get_rect()

    def move(self):
        self.rect.x -= 3
        self.rect.y -= 3



class Bloon(Sprite):
    def __init__(self):
        Sprite.__init__(self)

        im = image.load(r"media\bloon_blue.png").convert_alpha()
        self.image = pygame.transform.scale(im, (70, 90))

        self.rect = self.image.get_rect()

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
        

def stop(gameover=False, pause=False, begin=False):
    t3 = fbig.render(" Game Over ", False, black, white)
    t4 = f.render(" Click anywhere to continue ", False, black, white)
    t5 = fbig.render(" Paused ", False, black)
    t6 = fmed.render(" Click on the grass to place a monkey! ", False, blue)
    t7 = f.render(" Monkeys on the top shoot down and right ", False, white, black)
    t8 = f.render(" Monkeys on the bottom shoot up and left ", False, white, black)

    if gameover:
        while True:
            e = pygame.event.wait()
            screen.blit(t3, (275, 220))
            screen.blit(t4, (330, 288))

            if e.type in (pygame.QUIT, pygame.MOUSEBUTTONDOWN): return

            display.update()

    elif pause: 
        while True:
            e = pygame.event.wait()
            screen.blit(t5, (275, 220))
            screen.blit(t4, (330, 288))

            if e.type in (pygame.QUIT, pygame.MOUSEBUTTONDOWN): return

            display.update()

    elif begin:
        while True:
            e = pygame.event.wait()
            screen.blit(t6, (80, 220))
            screen.blit(t7, (250, 100))
            screen.blit(t8, (250, 500))

            if e.type in (pygame.QUIT, pygame.MOUSEBUTTONDOWN): return

            display.update()
    
#main
init()

screen = display.set_mode((900, 600))
display.set_caption("Pop the bloons!")

f = font.Font(None, 30)
fmed = font.Font(None, 60)
fbig = font.Font(None, 100)

b1 = Border() #top border
b2 = Border() #bottom border
bloon = Bloon() #balloon
monkey = Monkey() #monkey
# star = Star() #ninja star

time.set_timer(USEREVENT+ 1, DELAY) #is for timer

b1.setpos(0, 228)
b2.setpos(0, 445)
bloon.setpos(0, 328)
# monkey.setpos(50, 228)

bg = image.load(r"media\path_bg.png").convert_alpha()
screen.blit(bg, (0,0)) #sets background image

hits = 0 #bloons hit
health = 10 #health -= 1 for every escaped bloon

udtrigger = True #true = need to go up, false = need to go down
stop(begin=True)

x, y = mouse.get_pos()
monkey.setpos(x, y)

sprites = RenderPlain(bloon, monkey)

#game loop
while True:

    e = event.poll()

#see if bloon needs to move up or down
    if bloon.hit(b2):
        udtrigger = False
    elif bloon.hit(b1):
        udtrigger = True

#determine what to move or to exit game
    if e.type == QUIT:
        quit()
        break

    #if time has passed, move bloon and if star exists, move that too
    elif e.type == USEREVENT + 1:
        bloon.travel(udtrigger)
        try: star.move()
        except: pass

    #sends star to pop bloon
    elif e.type == KEYDOWN:

        if y < 330: star = Star()
        else: star = BottomStar()

        star.setpos(x+20, y)
        sprites = RenderPlain(bloon, monkey, star)
        star.move()

#if there is a hit, kill the bloon (and star)
    if star and bloon.hit(star):
        mixer.Sound(r"media\pop.wav").play()
        bloon.kill()
        star.kill()
        hits += 1
        bloon = Bloon()
        bloon.setpos(0, 328)
        sprites = RenderPlain(bloon, monkey)
        print ("no")


#if bloon escaped, subtract health. check if health = 0, if so game is over
    if bloon.escaped():
        health -= 1
        if health <= 0: stop(True)
        bloon.pop()
        bloon = Bloon()
        bloon.setpos(0, 328)
        sprites = RenderPlain(bloon, monkey)

#render and update screen, sprites, and text
    t = f.render("Hits: " + str(hits), False, black)
    t2 = f.render("Health: "+ str(health), False, black)
    screen.blit(bg, [0,0])
    screen.blit(t, (700, 20)) 
    screen.blit(t2, (700, 50))  
    sprites.update()
    sprites.draw(screen)
    display.update()