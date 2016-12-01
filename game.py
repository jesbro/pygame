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

DELAY = 15;
blue = (50, 150, 255)
green = (122, 244, 66)
black = (0,0,0)
white = (255,255,255)

screenx = 900 #leaving room around the edges
screeny = 600

bloons = pygame.sprite.Group()
stars = pygame.sprite.Group()
monkeys = pygame.sprite.Group()

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
        Sprite.__init__(self, monkeys)

        im = image.load(r"media\ninja_monkey.png").convert_alpha()
        self.image = pygame.transform.scale(im, (100, 100))

        self.rect = self.image.get_rect()

    def setpos(self, x, y):
        self.rect.center = (x, y)

    def getpos(self):
        return self.rect.center

class Star(Sprite):

    def __init__(self):
        Sprite.__init__(self, stars)

        im = image.load(r"media\ninja_star.png").convert_alpha()
        self.image = pygame.transform.scale(im, (30, 30))

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += 3
        self.rect.y += 3

    def setpos(self, x, y):
        self.rect.center = (x, y)

class BottomStar(Star):

    def __init__(self):
        Star.__init__(self)
        Sprite.__init__(self, stars)

        im = image.load(r"media\ninja_star.png").convert_alpha()
        self.image = pygame.transform.scale(im, (30, 30))

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x -= 3
        self.rect.y -= 3

class Bloon(Sprite):
    def __init__(self, color="red"):
        Sprite.__init__(self, bloons)

        if color == "red": 
            im = image.load(r"media\bloon_red.png").convert_alpha()
            self.image = pygame.transform.scale(im, (60, 80))
            self.speed = 1

        elif color == "blue": 
            im = image.load(r"media\bloon_blue.png").convert_alpha()
            self.image = pygame.transform.scale(im, (70, 90))
            self.speed = 2

        elif color == "rb":
            im = image.load(r"media\bloon_red.png").convert_alpha()
            self.image = pygame.transform.scale(im, (60, 80))
            self.speed = 2

        self.rect = self.image.get_rect()

    def hit(self, border):
        return self.rect.colliderect(border)

    def setpos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def pop(self):
        self.kill()

    def travel(self, ud):

        if ud:
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed
        self.rect.x += self.speed
        
    def escaped(self):
        if self.rect.center > (screenx, screeny): 
            return True
        return False
        

def stop(gameover=False, pause=False, begin=False):
    t3 = fbig.render(" Game Over ", False, black, white)
    t4 = f.render(" Click anywhere to continue ", False, black, white)
    t5 = fbig.render(" Paused ", False, black, white)
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
            screen.blit(t5, (325, 220))
            screen.blit(t4, (329, 288))

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

def addMonkey():

    t = fmed.render("You earned another monkey! Click to place", False, black)

    while True:
        e = pygame.event.wait()
        screen.blit(t, (15, 220))
        
        if e.type in (pygame.QUIT, pygame.MOUSEBUTTONDOWN): return
        display.update()

#determine bloon/star collision, returns num of hits
def collide():

    temp = 0
    for b in bloons:
        for s in stars:
            if b.hit(s):

                mixer.Sound(r"media\pop.wav").play()
                stars.remove(s)
                s.kill()
                bloons.remove(b)
                b.pop()
                temp += 1
    return temp

def escaped():

    temp = 0
    for b in bloons:
        if b.escaped():
            temp += 1
            bloons.remove(bl)
            bl.pop()
    return temp

def throw():
    for m in monkeys:
        x, y = m.getpos()
        if y < 330: star = Star()
        else: star = BottomStar()
        star.setpos(x+20, y)

def runbloons(times=1):
    for x in range(times):
        if numbloons < 8:
            newbloon = Bloon("red")
            newbloon.setpos(-50, 328)

        elif numbloons < 14:
            nb = Bloon("rb")
            newbloon = Bloon("blue")
            nb.setpos(-50, 328)
            newbloon.setpos(-50, 328)


#main
init()

screen = display.set_mode((900, 600))
display.set_caption("Pop the bloons!")

f = font.Font(None, 30)
fmed = font.Font(None, 60)
fbig = font.Font(None, 100)

b1 = Border() #top border
b2 = Border() #bottom border
monkey = Monkey() #monkey

b1.setpos(0, 228)
b2.setpos(0, 445)

time.set_timer(USEREVENT+ 1, DELAY) #is for timer

bg = image.load(r"media\path_bg.png").convert_alpha()
screen.blit(bg, (0,0)) #sets background image

hits = 0 #bloons hit
health = 10 #health -= 1 for every escaped bloon
temphits = 0 #keep track of when to add monkeys

udtrigger = True #true = need to go up, false = need to go down
stop(begin=True)

#set monkey position
x, y = mouse.get_pos()
monkey.setpos(x, y)

sprites = RenderPlain(monkeys)
loopcounter = 0
numbloons = 0

#game loop
while True:
    e = event.poll()

#determine what to move or to exit game
    if e.type == QUIT:
        quit()
        break

    elif e.type == MOUSEBUTTONDOWN: stop(pause=True)

    #if time has passed, move bloon and if star exists, move that too
    elif e.type == USEREVENT + 1:
        #tells all bloons to move
        for b in bloons:
            #see if bloon needs to move up or down
            if b.hit(b2): udtrigger = False
            elif b.hit(b1): udtrigger = True

            b.travel(udtrigger)

    #sends star to pop bloon
    elif e.type == KEYDOWN:
        throw()        

#if there is a hit, kill the bloon (and star)
    c = collide()
    hits += c
    temphits += c

#if bloon escaped, subtract health. check if health = 0, if true game is over
    health -= escaped()
    if health <= 0: stop(gameover=True)

#sends bloons
    if loopcounter % 200 == 0:
        runbloons(len(monkeys))
        numbloons += 1
    loopcounter += 1     

    if len(bloons) == 0 and temphits >= 10: 
        addMonkey()
        x, y = mouse.get_pos()
        m = Monkey()
        m.setpos(x, y)
        temphits = 0
        numbloons = 0


    if len(stars) > 0: sprites = RenderPlain(bloons, monkeys, stars)
    else: sprites = RenderPlain(bloons, monkeys)

#render and update screen, sprites, and text
    t = f.render("Hits: " + str(hits), False, black)
    t2 = f.render("Health: "+ str(health), False, black)
    screen.blit(bg, [0,0])
    screen.blit(t, (700, 20)) 
    screen.blit(t2, (700, 50))  
    sprites.update()
    sprites.draw(screen)
    display.update()
